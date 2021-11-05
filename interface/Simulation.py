import json
from abc import ABC, abstractmethod

import pygame

import Constants
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

    def __init__(self, simulationDuration=SIM_DURATION, numHubs=NUM_HUBS, numSites=NUM_SITES, shouldRecord=SHOULD_RECORD,
                 convergenceFraction=CONVERGENCE_FRACTION, hubLocations=HUB_LOCATIONS, hubRadii=HUB_RADII,
                 hubAgentCounts=HUB_AGENT_COUNTS, sitePositions=SITE_POSITIONS, siteQualities=SITE_QUALITIES,
                 siteRadii=SITE_RADII, siteNoCloserThan=SITE_NO_CLOSER_THAN, siteNoFartherThan=SITE_NO_FARTHER_THAN,
                 hubCanMove=HUB_CAN_MOVE, homogenousAgents=HOMOGENOUS_AGENTS, minSpeed=MIN_AGENT_SPEED,
                 maxSpeed=MAX_AGENT_SPEED, minDecisiveness=MIN_DECISIVENESS, maxDecisiveness=MAX_DECISIVENESS,
                 minNavSkills=MIN_NAV_SKILLS, maxNavSkills=MAX_NAV_SKILLS, minEstAccuracy=MIN_QUALITY_MISJUDGMENT,
                 maxEstAccuracy=MAX_QUALITY_MISJUDGMENT, maxSearchDist=MAX_SEARCH_DIST, findSitesEasily=FIND_SITES_EASILY,
                 commitSpeedFactor=COMMIT_SPEED_FACTOR):
        convergenceFraction, simulationDuration, fontSize, largeFontSize, numHubs, hubLocations, \
            hubRadii, hubAgentCounts, numSites, sitePositions, siteQualities, siteRadii, shouldRecord, siteRadius, \
            siteNoCloserThan, siteNoFartherThan, agentImage, maxSearchDist = \
            self.applyUserSettings(convergenceFraction, simulationDuration, FONT_SIZE, LARGE_FONT_SIZE, numHubs, hubLocations,
                                   hubRadii, hubAgentCounts, numSites, sitePositions, siteQualities, siteRadii, shouldRecord, SITE_RADIUS,
                                   siteNoCloserThan, siteNoFartherThan, AGENT_IMAGE, maxSearchDist)
        self.setDisplayVariables(agentImage)
        self.recorder = Recorder()  # The recorder that either records a live interface or plays a recorded interface
        SiteSettings.setSettings(siteNoCloserThan, siteNoFartherThan, hubCanMove)
        self.timeRanOut = False  # Whether there is no more time left in the interface
        self.simulationDuration = simulationDuration
        self.timer = SimulationTimer(self.simulationDuration, self.timeOut)  # A timer to handle keeping track of when the interface is paused or ends
        self.world = self.initializeWorld(numHubs, numSites, hubLocations, hubRadii, hubAgentCounts, sitePositions,
                                          siteQualities, siteRadii, siteRadius)  # The world that has all the sites and agents
        self.graphs = self.getGraphs(self.calcNumAgents(hubAgentCounts), fontSize, largeFontSize)
        self.chosenHomes = self.initChosenHomes(numHubs)  # The site that most of the agents are assigned to when the interface ends
        AgentSettings.setSettings(homogenousAgents, minSpeed, maxSpeed, minDecisiveness, maxDecisiveness, minNavSkills,
                                  maxNavSkills, minEstAccuracy, maxEstAccuracy, maxSearchDist, findSitesEasily, commitSpeedFactor)

        self.userControls = self.getControls()

        self.shouldRecord = shouldRecord  # Whether the interface should be recorded
        self.convergenceFraction = convergenceFraction  # The percentage of agents who need to be assigned to a site before the interface will end
        self.initializeAgentList()  # Create the agents that will be used in the interface

    @abstractmethod
    def initializeWorld(self, numHubs, numSites, hubLocation, hubRadius, hubAgentCount, sitePositions, siteQualities,
                        siteRadii, siteRadius=SITE_RADIUS):
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

        return self.finish()

    def initializeRequest(self):
        pass  # The method is overridden by simulations that send requests to rest APIs

    def runNextRound(self):
        agentRectList = self.getAgentRectList()
        self.update(agentRectList)

    def getAgentRectList(self):
        agentRectList = []
        for agent in self.world.agentList:
            agentRectList.append(agent.getAgentRect())
        return agentRectList

    def update(self, agentRectList):
        self.setNextRound()
        self.world.updateStateAndPhaseCounts()
        self.updateSites()
        self.updateAgents(agentRectList)
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

    def recordDisplays(self):
        if self.shouldRecord:
            self.recorder.recordAgentsToDelete(self.world.getDeletedAgentsIndexes())
            self.recorder.recordTime(self.timer.getRemainingTime())
            self.recorder.recordShouldDrawGraphs(self.graphs.shouldDrawGraphs)
            self.recorder.recordExecutedCommands(self.graphs.executedCommands)
            self.recorder.recordScreenBorder(Display.displacementX, Display.displacementY, Display.origWidth * Display.origWidth / Display.newWidth, Display.origHeight * Display.origHeight / Display.newHeight)

    @abstractmethod
    def updateAgent(self, agent, agentRectList):
        pass

    def report(self, agentRectList):
        pass

    def checkIfSimulationEnded(self):
        numConverged = 0
        for siteIndex in range(len(self.world.getHubs()), len(self.world.siteList)):
            site = self.world.siteList[siteIndex]
            for hubIndex in range(len(self.world.getHubs())):
                if site.agentCounts[hubIndex] >= int(self.world.initialHubAgentCounts[hubIndex] * self.convergenceFraction):
                    self.chosenHomes[hubIndex] = site
                    numConverged += 1
                    break
        for hubIndex in range(len(self.world.getHubs())):
            if self.world.initialHubAgentCounts[hubIndex] == 0:
                self.chosenHomes[hubIndex] = self.world.siteList[hubIndex]
                numConverged += 1
        return numConverged >= len(self.world.getHubs())

    def timeOut(self):
        print("The simulation time has run out.")
        self.timeRanOut = True

    def finish(self):
        if self.shouldRecord:
            self.write()
        self.determineChosenHomes()
        results = self.printResults()
        if Display.shouldDraw:
            Display.drawFinish(Display.screen, results)
            pygame.display.flip()
            self.userControls.waitForUser()
        return results

    def save(self):
        pass

    def write(self):
        pass

    def determineChosenHomes(self):
        for i in range(len(self.world.getHubs())):
            for home in self.world.siteList:
                if self.chosenHomes[i] is None or home.agentCounts[i] > self.chosenHomes[i].agentCounts[i]:
                    self.chosenHomes[i] = home

    def printResults(self):
        self.printNumAgentsResults()
        simulationTime = self.printTimeResults()
        qualities = self.printHomeQualities()
        self.sendResults(self.chosenHomes, simulationTime)
        return qualities, simulationTime

    def printNumAgentsResults(self):
        for i in range(len(self.chosenHomes)):
            print(str(self.chosenHomes[i].agentCounts[i]) + " out of " + str(self.world.initialHubAgentCounts[i]) +
                  " agents from hub " + str(i + 1) + " made it to the new home.")

    def printTimeResults(self):
        simulationTime = 10000  # Large number that means the agents did not find the new home in time.
        if not self.timeRanOut:
            simulationTime = self.getRemainingTime()
            self.timer.cancel()
            print("The simulation took " + str(simulationTime) + " seconds to complete.")
        return simulationTime

    def getRemainingTime(self):
        return self.timer.simulationDuration - self.timer.getRemainingTime()

    def printHomeQualities(self):
        qualities = []
        print("Their homes are ranked: ")
        for home in self.chosenHomes:
            qualities.append(home.getQuality())
            print(str(home.getQuality()) + "/255.")
        return qualities

    def sendResults(self, chosenSite, simulationTime):
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
        return Controls(self.timer, self.world.agentList, self.world, self.graphs)  # An object to handle events dealing with user interactions

    @staticmethod
    def applyUserSettings(cf, sd, fs, lfs, nh, hl, hr, hac, ns, sp, sq, sr, sRec, sRadius, snct, snft, ai, msd):
        try:
            with open('display/mainmenu/settings.json', 'r') as file:
                data = json.load(file)
            if 'convergenceFraction' in data:
                cf = data['convergenceFraction']
                Constants.CONVERGENCE_FRACTION = cf
            if 'simDuration' in data:
                sd = data['simDuration']
                Constants.SIM_DURATION = sd
            if 'fontSize' in data:
                fs = data['fontSize']
                Constants.FONT_SIZE = fs
            if 'largeFontSize' in data:
                lfs = data['largeFontSize']
                Constants.LARGE_FONT_SIZE = lfs
            if 'numHubs' in data:
                nh = data['numHubs']
                Constants.NUM_HUBS = nh
            if 'hubLocations' in data:
                hl = data['hubLocations']
                Constants.HUB_LOCATIONS = hl
            if 'hubRadii' in data:
                hr = data['hubRadii']
                Constants.HUB_RADII = hr
            if 'hubAgentCounts' in data:
                hac = data['hubAgentCounts']
                Constants.HUB_AGENT_COUNTS = hac
            if 'numSites' in data:
                ns = data['numSites']
                Constants.NUM_SITES = ns
            if 'sitePositions' in data:
                sp = data['sitePositions']
                Constants.SITE_POSITIONS = sp
            if 'siteQualities' in data:
                sq = data['siteQualities']
                Constants.SITE_QUALITIES = sq
            if 'siteRadii' in data:
                sr = data['siteRadii']
                Constants.SITE_RADII = sr
            if 'shouldRecord' in data:
                sRec = data['shouldRecord']
                Constants.SHOULD_RECORD = sRec
            if 'siteRadius' in data:
                sRadius = data['siteRadius']
                Constants.SITE_RADIUS = sRadius
            if 'siteNoCloserThan' in data:
                snct = data['siteNoCloserThan']
                Constants.SITE_NO_CLOSER_THAN = snct
            if 'siteNoFartherThan' in data:
                snft = data['siteNoFartherThan']
                Constants.SITE_NO_FARTHER_THAN = snft
            if 'agentImage' in data:
                ai = data['agentImage']
                Constants.AGENT_IMAGE = ai
            if 'maxSearchDist' in data:
                msd = data['maxSearchDist']
                Constants.MAX_SEARCH_DIST = msd
        except FileNotFoundError:
            print("File 'mainmenu/settings.json' Not Found")
            with open('display/mainmenu/settings.json', 'w'):
                print("Created 'mainmenu/settings.json'")
        except json.decoder.JSONDecodeError:
            print("File 'mainmenu/settings.json' is empty")
        return cf, sd, fs, lfs, nh, hl, hr, hac, ns, sp, sq, sr, sRec, sRadius, snct, snft, ai, msd
