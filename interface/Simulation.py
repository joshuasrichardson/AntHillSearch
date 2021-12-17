import json
from abc import ABC, abstractmethod

import pygame

from Constants import *
from display import Display, SiteDisplay, AgentDisplay
from display.WorldDisplay import drawWorldObjects
from ColonyExceptions import GameOver
from model.Timer import SimulationTimer
from model.builder import AgentBuilder, AgentSettings, SiteSettings
from recording.Recorder import Recorder
from model.states.AtNestState import AtNestState
from user.Controls import Controls


class Simulation(ABC):
    """ Runs most of the colony interface but leaves some details to classes that inherit this class """

    def __init__(self, simulationDuration=SIM_DURATION, numHubs=NUM_HUBS, numSites=NUM_SITES,
                 shouldRecord=SHOULD_RECORD, convergenceFraction=CONVERGENCE_FRACTION, hubLocations=HUB_LOCATIONS,
                 hubRadii=HUB_RADII, hubAgentCounts=HUB_AGENT_COUNTS, sitePositions=SITE_POSITIONS,
                 siteQualities=SITE_QUALITIES, siteRadii=SITE_RADII, siteNoCloserThan=SITE_NO_CLOSER_THAN,
                 siteNoFartherThan=SITE_NO_FARTHER_THAN, hubCanMove=HUB_CAN_MOVE, homogenousAgents=HOMOGENOUS_AGENTS,
                 minSpeed=MIN_AGENT_SPEED, maxSpeed=MAX_AGENT_SPEED, minDecisiveness=MIN_DECISIVENESS,
                 maxDecisiveness=MAX_DECISIVENESS, minNavSkills=MIN_NAV_SKILLS, maxNavSkills=MAX_NAV_SKILLS,
                 minEstAccuracy=MIN_QUALITY_MISJUDGMENT, maxEstAccuracy=MAX_QUALITY_MISJUDGMENT,
                 maxSearchDist=MAX_SEARCH_DIST, findSitesEasily=FIND_SITES_EASILY,
                 commitSpeedFactor=COMMIT_SPEED_FACTOR, agentImage=AGENT_IMAGE, siteRadius=SITE_RADIUS,
                 numPredators=NUM_PREDATORS, fontSize=FONT_SIZE, largeFontSize=LARGE_FONT_SIZE, useJson=False):
        # If the the settings in the display/mainmenu/settings.json file should override the values passed in,
        # update all the settings.
        convergenceFraction, simulationDuration, fontSize, largeFontSize, numHubs, hubLocations, \
            hubRadii, hubAgentCounts, numSites, sitePositions, siteQualities, siteRadii, shouldRecord, recordAll, \
            siteRadius, siteNoCloserThan, siteNoFartherThan, agentImage, maxSearchDist, numPredators, predPositions = \
            self.applyUserSettings(
                [convergenceFraction, simulationDuration, fontSize, largeFontSize, numHubs, hubLocations,
                 hubRadii, hubAgentCounts, numSites, sitePositions, siteQualities, siteRadii, shouldRecord,
                 RECORD_ALL, siteRadius, siteNoCloserThan, siteNoFartherThan, agentImage, maxSearchDist, numPredators,
                 PRED_POSITIONS], useJson)
        self.recordAll = recordAll
        # Set up the screen, agent image, and important boolean variables
        self.setDisplayVariables(agentImage)
        self.recorder = Recorder()  # The recorder that either records a live interface or plays a recorded interface
        # Set whether the hubs can move and how far away sites can be from the hubs.
        SiteSettings.setSettings(siteNoCloserThan, siteNoFartherThan, hubCanMove)
        self.timeRanOut = False  # Whether there is no more time left in the interface
        self.simulationDuration = simulationDuration  # Time of the simulation if agents don't converge to a site
        self.timer = SimulationTimer(self.simulationDuration, self.timeOut)  # A timer to handle keeping track of when the interface is paused or ends
        self.world = self.initializeWorld(numHubs, numSites, hubLocations, hubRadii, hubAgentCounts, sitePositions,
                                          siteQualities, siteRadii, siteRadius, numPredators, predPositions)  # The world that has all the sites and agents
        self.graphs = self.getGraphs(self.calcNumAgents(hubAgentCounts), fontSize, largeFontSize)
        self.chosenHomes = self.initChosenHomes(numHubs)  # The site that most of the agents are assigned to when the interface ends
        AgentSettings.setSettings(homogenousAgents, minSpeed, maxSpeed, minDecisiveness, maxDecisiveness, minNavSkills,
                                  maxNavSkills, minEstAccuracy, maxEstAccuracy, maxSearchDist, findSitesEasily,
                                  commitSpeedFactor)

        self.userControls = self.getControls()

        self.shouldRecord = shouldRecord  # Whether the interface should be recorded
        self.convergenceFraction = convergenceFraction  # The percentage of agents who need to be assigned to a site before the interface will end
        self.initializeAgentList()  # Create the agents that will be used in the interface
        self.remainingTime = self.simulationDuration  # Time left in the simulation

    @abstractmethod
    def initializeWorld(self, numHubs, numSites, hubLocation, hubRadius, hubAgentCount, sitePositions, siteQualities,
                        siteRadii, siteRadius=SITE_RADIUS, numPredators=NUM_PREDATORS, predPositions=PRED_POSITIONS):
        pass

    @staticmethod
    def calcNumAgents(hubAgentCounts):
        total = 0
        for num in hubAgentCounts:
            total += num
        return total

    def setAgentList(self, agents):
        self.world.agentList = agents

    def initializeAgentList(self):
        hubIndex = 0
        for count in self.world.initialHubAgentCounts:
            for i in range(count):
                agent = AgentBuilder.getNewAgent(self.world, self.world.getHubs()[hubIndex])
                agent.setState(AtNestState(agent))
                self.world.agentList.append(agent)
                self.world.agentGroups[i % 10].append(agent)
            hubIndex += 1
            if hubIndex >= len(self.world.getHubs()):
                break
        self.initializeRequest()

    def initChosenHomes(self, numHubs):
        chosenHomes = []
        for i in range(numHubs):
            chosenHomes.append(self.world.siteList[0])
        return chosenHomes

    def runSimulation(self):
        foundNewHome = False
        self.timer.start()

        try:
            while not foundNewHome and not self.timeRanOut:
                self.runNextRound()
                foundNewHome = self.checkIfSimulationEnded()
        except GameOver:
            pass

        self.stopTimer()

        return self.finish()

    def stopTimer(self):
        self.remainingTime = self.timer.getRemainingTime()
        self.timer.cancel()

    def initializeRequest(self):
        pass  # The method is overridden by simulations that send requests to rest APIs

    def runNextRound(self):
        agentRectList = self.getAgentRectList()
        self.update(agentRectList)

    def getAgentRectList(self):
        agentRectList = []
        for agent in self.world.agentList:
            agentRectList.append(agent.getRect())
        return agentRectList

    def update(self, agentRectList):
        self.setNextRound()
        self.world.updateStateAndPhaseCounts()
        self.updateSites()
        self.updateAgents(agentRectList)
        self.updatePredators(agentRectList)
        self.recordDisplays()
        self.save()
        self.report(agentRectList)

    def draw(self):
        drawWorldObjects(self.world)
        self.drawGraphs()
        self.userControls.drawChanges()
        pygame.display.flip()

    def drawGraphs(self):
        self.graphs.drawStateGraph(self.world.states)
        self.graphs.drawPhaseGraph(self.world.phases)
        self.graphs.drawPredictionsGraph(self.world.siteList)
        self.graphs.drawExecutedCommands()
        self.graphs.drawRemainingTime()
        self.graphs.drawPauseButton()
        self.graphs.drawStateNumbers()

    def setNextRound(self):
        pass

    def updateSites(self):
        pass

    def updateAgents(self, agentRectList):
        for agent in self.world.agentList:
            self.updateAgent(agent, agentRectList)
            self.world.updatePaths(agent)

    def updatePredators(self, agentRectList):
        for predator in self.world.predatorList:
            self.updatePredator(predator, agentRectList)

    def recordDisplays(self):
        if self.shouldRecord:
            self.recorder.recordExecutedCommands(self.graphs.executedCommands)
            if self.recordAll:
                self.recorder.recordAgentsToDelete(self.world.getDeletedAgentsIndexes())
                self.recorder.recordTime(self.timer.getRemainingTime())
                self.recorder.recordShouldDrawGraphs(self.graphs.shouldDrawGraphs)
                self.recorder.recordScreenBorder(Display.displacementX, Display.displacementY,
                                                 Display.origWidth * Display.origWidth / Display.newWidth,
                                                 Display.origHeight * Display.origHeight / Display.newHeight)

    @abstractmethod
    def updateAgent(self, agent, agentRectList):
        pass

    @abstractmethod
    def updatePredator(self, predator, agentRectList):
        pass

    def report(self, agentRectList):
        pass

    def checkIfSimulationEnded(self):
        numConverged = 0
        for siteIndex in range(len(self.world.getHubs()), len(self.world.siteList)):
            site = self.world.siteList[siteIndex]
            for hubIndex in range(len(self.world.getHubs())):
                if site.agentCounts[hubIndex] >= int((self.world.initialHubAgentCounts[hubIndex] -
                                                      self.world.numDeadAgents[
                                                          hubIndex]) * self.convergenceFraction) > 0:
                    self.chosenHomes[hubIndex] = site
                    self.chosenHomes[hubIndex].chosen = True
                    numConverged += 1
        for hubIndex in range(len(self.world.getHubs())):
            if self.world.initialHubAgentCounts[hubIndex] == 0:
                self.chosenHomes[hubIndex] = self.world.siteList[hubIndex]
                numConverged += 1
                self.chosenHomes[hubIndex].chosen = True
        return numConverged >= len(self.world.getHubs())

    def timeOut(self):
        print("The simulation time has run out.")
        self.timeRanOut = True

    def finish(self):
        if self.shouldRecord:
            self.write(self.recordAll)
        self.determineChosenHomes()
        results = self.printResults()
        if Display.shouldDraw:
            Display.drawFinish(Display.screen, results)
            pygame.display.flip()
            self.userControls.waitForUser()
        return results

    def save(self):
        pass

    def write(self, recordAll):
        pass

    def determineChosenHomes(self):
        for i in range(len(self.world.getHubs())):
            for home in self.world.siteList:
                if self.chosenHomes[i] is None or home.agentCounts[i] > self.chosenHomes[i].agentCounts[i]:
                    self.chosenHomes[i] = home

    def printResults(self):
        self.printNumAgentsResults()
        results = {"simulationTime": self.printTimeResults(),
                   "qualities": self.printHomeQualities(),
                   "deadAgents": self.getNumDeadAgents(),
                   "chosenHomes": self.chosenHomes,
                   "initialHubAgentCounts": self.world.initialHubAgentCounts}
        self.sendResults(self.chosenHomes, results["simulationTime"], results["deadAgents"])
        return results

    def getNumDeadAgents(self):
        return self.world.numDeadAgents

    def printNumAgentsResults(self):
        for i in range(len(self.chosenHomes)):
            print(f"{self.chosenHomes[i].agentCounts[i]}/{self.world.initialHubAgentCounts[i]} agents from "
                  f"colony {i + 1} made it to the new home.")
        for hubIndex in range(len(self.world.hubs)):
            print(f"{self.world.initialHubAgentCounts[hubIndex] - self.world.numDeadAgents[hubIndex]}/"
                  f"{self.world.initialHubAgentCounts[hubIndex]} agents from colony {hubIndex} survived.")

    def printTimeResults(self):
        simulationTime = 10000  # Large number that means the agents did not find the new home in time.
        if not self.timeRanOut:
            simulationTime = self.simulationDuration - self.remainingTime
            print(f"The simulation took {simulationTime} seconds to complete.")
        return simulationTime

    def printHomeQualities(self):
        qualities = []
        print("Their homes are ranked: ")
        for i, home in enumerate(self.chosenHomes):
            qualities.append(home.getQuality())
            print(f"Colony {i + 1} - {home.getQuality()}/255.")

        return qualities

    def sendResults(self, chosenSite, simulationTime, deadAgents):
        pass

    def setDisplayVariables(self, agentImage):
        Display.screen = self.getScreen()
        Display.shouldDraw = self.getShouldDraw()
        Display.drawFarAgents = self.getDrawFarAgents()
        AgentDisplay.agentImage = agentImage
        SiteDisplay.knowSitePosAtStart = self.getKnowSitePosAtStart()

    @abstractmethod
    def getScreen(self):
        pass

    @abstractmethod
    def getShouldDraw(self):
        pass

    @abstractmethod
    def getDrawFarAgents(self):
        pass

    @abstractmethod
    def getKnowSitePosAtStart(self):
        pass

    @abstractmethod
    def getShouldDrawPaths(self):
        pass

    @abstractmethod
    def getGraphs(self, numAgents, fontSize, largeFontSize):
        pass

    def getControls(self):
        return Controls(self.timer, self.world.agentList, self.world,
                        self.graphs)  # An object to handle events dealing with user interactions

    @staticmethod
    def applyUserSettings(retValues, useJson):
        if useJson:
            try:
                with open(SETTINGS_FILE_NAME, 'r') as file:
                    data = json.load(file)
                for i, key in enumerate(SETTING_KEYS):
                    if key in data:
                        try:
                            exec(f"global {SETTING_NAMES[i]}\n{SETTING_NAMES[i]} = {data[key]}")
                        except NameError:
                            exec(f"{SETTING_NAMES[i]} = \"{data[key]}\"")
                        retValues[i] = data[key]
            except FileNotFoundError:
                print(f"File '{SETTINGS_FILE_NAME}' Not Found")
                with open('display/mainmenu/settings.json', 'w'):
                    print("Created 'mainmenu/settings.json'")
            except json.decoder.JSONDecodeError:
                print(f"File '{SETTINGS_FILE_NAME}' is empty")
        return retValues
