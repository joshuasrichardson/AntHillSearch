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
        AgentSettings.setSettings(homogenousAgents, minSpeed, maxSpeed, minDecisiveness, maxDecisiveness, minNavSkills,
                                  maxNavSkills, minEstAccuracy, maxEstAccuracy, maxSearchDist, findSitesEasily,
                                  commitSpeedFactor)
        self.world = self.initializeWorld(numHubs, numSites, hubLocations, hubRadii, hubAgentCounts, sitePositions,
                                          siteQualities, siteRadii, siteRadius, numPredators, predPositions)  # The world that has all the sites and agents
        self.graphs = self.getGraphs(self.calcNumAgents(hubAgentCounts), fontSize, largeFontSize)
        self.chosenHomes = self.initChosenHomes(numHubs)  # The site that most of the agents are assigned to when the interface ends
        self.userControls = self.getControls()
        self.shouldRecord = shouldRecord  # Whether the interface should be recorded
        self.convergenceFraction = convergenceFraction  # The percentage of agents who need to be assigned to a site before the interface will end

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
        for hubIndex, count in enumerate(self.world.initialHubAgentCounts):
            if hubIndex >= len(self.world.getHubs()):
                break
            for i in range(count):
                agent = AgentBuilder.getNewAgent(self.world, self.world.getHubs()[hubIndex])
                agent.setState(AtNestState(agent))
                self.world.agentList.append(agent)
                self.world.agentGroups[i % 10].append(agent)

    def initChosenHomes(self, numHubs):
        chosenHomes = []
        for i in range(numHubs):
            chosenHomes.append(self.world.siteList[0])
        return chosenHomes

    def runSimulation(self):
        foundNewHome = False
        self.timer.start()
        numRounds = 0

        try:
            while not foundNewHome and not self.timeRanOut:
                self.runNextRound()
                numRounds += 1
                foundNewHome = self.checkIfSimulationEnded()
        except GameOver:
            pass

        print(f"Number of Rounds: {numRounds}")

        self.stopTimer()

        return self.finish()

    def stopTimer(self):
        self.timer.cancel()

    def runNextRound(self):
        self.userControls.handleEvents()
        agentRectList = self.getAgentRectList()
        self.update(agentRectList)
        Display.screen.fill(SCREEN_COLOR)
        self.draw()

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

    def draw(self):
        drawWorldObjects(self.world)
        self.drawGraphs()
        self.userControls.drawChanges()
        self.drawBorder()
        pygame.display.flip()

    def drawGraphs(self):
        self.graphs.drawStateGraph(self.world.states)
        self.graphs.drawPhaseGraph(self.world.phases)
        self.graphs.drawPredictionsGraph(self.world.siteList)
        self.graphs.drawExecutedCommands()
        self.graphs.drawRemainingTime()
        self.graphs.drawPauseButton()
        self.graphs.drawStateNumbers()

    @staticmethod
    def drawBorder():
        Display.drawBorder()

    def setNextRound(self):
        pass

    def updateSites(self):
        pass

    def updateAgents(self, agentRectList):
        for agent in self.world.agentList:
            self.updateAgent(agent, agentRectList)
            self.world.updatePaths(agent)

    @abstractmethod
    def updateAgent(self, agent, agentRectList):
        pass

    def updatePredators(self, agentRectList):
        for predator in self.world.predatorList:
            self.updatePredator(predator, agentRectList)

    @abstractmethod
    def updatePredator(self, predator, agentRectList):
        pass

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

    def checkIfSimulationEnded(self):
        """ Compare the number of agents at each site from each hub to the number of agents initially at each hub
        times the convergence fraction to see if the the agents from all hubs have converged to a new site. """
        numConverged = 0
        for siteIndex in range(len(self.world.getHubs()), len(self.world.siteList)):
            site = self.world.siteList[siteIndex]
            for hubIndex in range(len(self.world.getHubs())):
                if site.agentCounts[hubIndex] >= int((self.world.initialHubAgentCounts[hubIndex] -
                                                      self.world.numDeadAgents[
                                                          hubIndex]) * self.convergenceFraction) > 0:
                    self.chosenHomes[hubIndex] = site
                    numConverged += 1
                    hub = self.world.getHubs()[hubIndex]
                    if hub.time == 0:
                        hub.time = self.timer.getRemainingTime()
        for hubIndex in range(len(self.world.getHubs())):
            if self.world.initialHubAgentCounts[hubIndex] == 0:
                self.chosenHomes[hubIndex] = self.world.siteList[hubIndex]
                numConverged += 1
                hub = self.world.getHubs()[hubIndex]
                if hub.time == 0:
                    hub.time = self.timer.getRemainingTime()
        return numConverged >= len(self.world.getHubs())

    def timeOut(self):
        """ Method to be called when the simulation timer runs out. sets timeRanOut to True to break the main loop. """
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
        numArrivals, numDeaths = self.printNumAgentsResults()
        positions = []
        for site in self.chosenHomes:
            positions.append(site.getPosition())
        results = {SIM_TIMES_NAME: self.printTimeResults(),
                   HOME_QUALITIES_NAME: self.printHomeQualities(),
                   HOME_POSITIONS_NAME: positions,
                   NUM_ARRIVALS_NAME: numArrivals,
                   NUM_DEAD_NAME: numDeaths,
                   TOTAL_NAME: self.world.initialHubAgentCounts}
        self.sendResults(results)
        return results

    def getNumDeadAgents(self):
        return self.world.numDeadAgents

    def printNumAgentsResults(self):
        numArrived = []
        numDead = self.getNumDeadAgents()
        for i in range(len(self.chosenHomes)):
            numArrived.append(self.chosenHomes[i].agentCounts[i])
            print(f"{self.chosenHomes[i].agentCounts[i]}/{self.world.initialHubAgentCounts[i]} agents from "
                  f"colony {i + 1} made it to the new home.")
        for hubIndex in range(len(self.world.hubs)):
            print(f"{numDead[hubIndex]}/"
                  f"{self.world.initialHubAgentCounts[hubIndex]} agents from colony {hubIndex + 1} died.")
        return numArrived, numDead

    def printTimeResults(self):
        times = []
        for i, hub in enumerate(self.world.getHubs()):
            if hub.time == 0:
                simulationTime = self.simulationDuration
            else:
                simulationTime = self.simulationDuration - hub.time
            times.append(simulationTime)
            print(f"Colony {i + 1} took {simulationTime} seconds to finish.")
        return times

    def printHomeQualities(self):
        qualities = []
        print("Their homes are ranked: ")
        for i, home in enumerate(self.chosenHomes):
            qualities.append(home.getQuality())
            print(f"Colony {i + 1}: {home.getQuality()}/255.")

        return qualities

    def sendResults(self, results):
        pass

    def setDisplayVariables(self, agentImage):
        Display.screen = self.getScreen()
        Display.shouldDraw = self.getShouldDraw()
        Display.drawFarAgents = self.getDrawFarAgents()
        AgentDisplay.agentImage = agentImage
        SiteDisplay.knowSitePosAtStart = self.getKnowSitePosAtStart()

    def getScreen(self):
        """ Gets the screen to draw the simulation on (or None if the simulation will not be drawn) """
        return Display.createScreen()

    @abstractmethod
    def getShouldDraw(self):
        """ Gets a boolean deciding whether the simulation will be drawn on the screen """
        pass

    @abstractmethod
    def getDrawFarAgents(self):
        """ Gets a boolean deciding whether the agents outside the view of the hub should be drawn """
        pass

    @abstractmethod
    def getKnowSitePosAtStart(self):
        """ Gets a boolean deciding whether the user knows where the sites are to begin """
        pass

    @abstractmethod
    def getShouldDrawPaths(self):
        """ Gets a boolean deciding whether ants paths should be drawn """
        pass

    @abstractmethod
    def getGraphs(self, numAgents, fontSize, largeFontSize):
        """ Gets the graphs used to display information on the screen """
        pass

    def getControls(self):
        """ Initializes and returns an object to handle user input """
        return Controls(self.timer, self.world.agentList, self.world,
                        self.graphs)  # An object to handle events dealing with user interactions

    @staticmethod
    def applyUserSettings(retValues, useJson):
        """ Sets the simulation values to match the values in {SETTINGS_FILE_NAME} """
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
                with open(f'{SETTINGS_FILE_NAME}', 'w'):
                    print(f"Created '{SETTINGS_FILE_NAME}'")
            except json.decoder.JSONDecodeError:
                print(f"File '{SETTINGS_FILE_NAME}' is empty")
        return retValues
