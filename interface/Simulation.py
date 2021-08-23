import threading
from abc import ABC, abstractmethod

import pygame

from Constants import *
from display import Display, SiteDisplay
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
        self.setDisplayVariables()
        self.graphs = self.getGraphs()
        self.recorder = Recorder()  # The recorder that either records a live interface or plays a recorded interface
        SiteSettings.setSettings(siteNoCloserThan, siteNoFartherThan, hubCanMove)
        self.world = self.initializeWorld(numHubs, numSites, hubLocations, hubRadii, hubAgentCounts, sitePositions,
                                          siteQualities, siteRadii)  # The world that has all the sites and agents
        self.chosenHomes = self.initChosenHomes(len(hubLocations))  # The site that most of the agents are assigned to when the interface ends
        self.timeRanOut = False  # Whether there is no more time left in the interface
        self.timer = SimulationTimer(simulationDuration, threading.Timer(simulationDuration, self.timeOut), self.timeOut)  # A timer to handle keeping track of when the interface is paused or ends
        AgentSettings.setSettings(homogenousAgents, minSpeed, maxSpeed, minDecisiveness, maxDecisiveness, minNavSkills,
                                  maxNavSkills, minEstAccuracy, maxEstAccuracy, maxSearchDist, findSitesEasily, commitSpeedFactor)
        self.userControls = Controls(self.timer, self.world.agentList, self.world, self.graphs)  # And object to handle events dealing with user interactions

        self.shouldRecord = shouldRecord  # Whether the interface should be recorded
        self.convergenceFraction = convergenceFraction  # The percentage of agents who need to be assigned to a site before the interface will end

    @abstractmethod
    def initializeWorld(self, numHubs, numSites, hubLocation, hubRadius, hubAgentCount, sitePositions, siteQualities,
                        siteRadii):
        pass

    def setAgentList(self, agents):
        self.world.agentList = agents

    def initializeAgentList(self, hubAgentCounts=HUB_AGENT_COUNTS):
        hubIndex = 0
        for count in hubAgentCounts:
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

    def setNextRound(self):
        pass

    def updateSites(self):
        pass

    def updateAgents(self, agentRectList):
        for agent in self.world.agentList:
            try:  # If the following block is executed after an agent is deleted in the RecordingPlayer, it will break.
                self.updateAgent(agent, agentRectList)
                self.world.updatePaths(agent)
            except IndexError:  # So we need to remove the agent here too if that happens.
                self.world.removeAgent(agent)

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
                if site.agentCounts[hubIndex] >= self.world.initialHubAgentCounts[hubIndex] * self.convergenceFraction:
                    self.chosenHomes[hubIndex] = site
                    numConverged += 1
                    print(str(site.agentCounts))
                    print(str(self.world.initialHubAgentCounts[hubIndex]))
                    print(str(self.convergenceFraction))
                    break
        return numConverged == len(self.world.getHubs())

    def timeOut(self):
        print("The simulation time has run out.")
        self.timeRanOut = True

    def finish(self):
        if Display.shouldDraw:
            Display.drawFinish(Display.screen)
            pygame.display.flip()
        if self.shouldRecord:
            self.write()
        self.determineChosenHomes()
        return self.printResults()

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
        for i in range(len(self.chosenHomes)):
            print(str(self.chosenHomes[i].agentCounts[i]) + " out of " + str(self.world.initialHubAgentCounts[i]) +
                  " agents from hub " + str(i + 1) + " made it to the new home.")
        simulationTime = 10000  # Large number that means the agents did not find the new home in time.
        if not self.timeRanOut:
            simulationTime = self.timer.simulationDuration - self.timer.getRemainingTime()
            print("The simulation took " + str(simulationTime) + " seconds to complete.")
            pygame.quit()
            self.timer.cancel()
        qualities = []
        print("Their homes are ranked: ")
        for home in self.chosenHomes:
            qualities.append(home.getQuality())
            print(str(home.getQuality()) + "/255.")
        self.sendResults(self.chosenHomes, simulationTime)
        return qualities, simulationTime

    def sendResults(self, chosenSite, simulationTime):
        pass

    def setDisplayVariables(self):
        Display.screen = self.getScreen()
        Display.shouldDraw = self.getShouldDraw()
        Display.drawFarAgents = self.getDrawFarAgents()
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
    def getGraphs(self):
        pass
