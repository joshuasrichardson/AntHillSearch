import threading
from abc import ABC, abstractmethod

import pygame

from Constants import *
from display import AgentDisplay, Display, SiteDisplay
from display.WorldDisplay import drawWorldObjects
from model.Agent import Agent
from ColonyExceptions import InputError, GameOver
from display.Graphs import SimulationGraphs
from model.Timer import SimulationTimer
from recording.Recorder import Recorder
from model.states.AtNestState import AtNestState
from user.Controls import Controls


class AbstractColonySimulation(ABC):
    """ Runs most of the colony interface but leaves some details to classes that inherit this class """

    def __init__(self, simulationDuration=SIM_DURATION, numSites=NUM_SITES, useRestAPI=USE_REST_API,
                 shouldRecord=SHOULD_RECORD, convergenceFraction=CONVERGENCE_FRACTION,
                 hubLocation=HUB_LOCATION, hubRadius=SITE_RADIUS, hubAgentCount=NUM_AGENTS, sitePositions=SITE_POSITIONS,
                 siteQualities=SITE_QUALITIES, siteRadii=SITE_RADII, siteNoCloserThan=SITE_NO_CLOSER_THAN,
                 siteNoFartherThan=SITE_NO_FARTHER_THAN, hubCanMove=HUB_CAN_MOVE):
        self.setDisplayVariables()
        if Display.shouldDraw:
            self.graphs = SimulationGraphs()
        else:
            self.graphs = None
        self.recorder = Recorder()  # The recorder that either records a live interface or plays a recorded interface
        self.world = self.initializeWorld(numSites, hubLocation, hubRadius, hubAgentCount, sitePositions,
                                          siteQualities, siteRadii, siteNoCloserThan, siteNoFartherThan,
                                          Display.shouldDraw, hubCanMove)  # The world that has all the sites and agents
        self.chosenHome = None  # The site that most of the agents are assigned to when the interface ends
        self.timeRanOut = False  # Whether there is no more time left in the interface
        self.timer = SimulationTimer(simulationDuration, threading.Timer(simulationDuration, self.timeOut), self.timeOut)  # A timer to handle keeping track of when the interface is paused or ends
        self.userControls = Controls(self.timer, self.world.agentList, self.world, self.graphs)  # And object to handle events dealing with user interactions

        self.useRestAPI = useRestAPI  # Whether the interface should periodically report hub information to the rest API
        self.apiThread = None
        self.shouldRecord = shouldRecord  # Whether the interface should be recorded
        self.onlyDrawExploredArea = True

        self.convergenceFraction = convergenceFraction  # The percentage of agents who need to be assigned to a site before the interface will end

    @abstractmethod
    def initializeWorld(self, numSites, hubLocation, hubRadius, hubAgentCount, sitePositions, siteQualities,
                        siteRadii, siteNoCloserThan, siteNoFartherThan, shouldDraw, hubCanMove):
        pass

    def setAgentList(self, agents):
        self.world.agentList = agents

    def initializeAgentList(self, numAgents=NUM_AGENTS, homogenousAgents=HOMOGENOUS_AGENTS, minSpeed=MIN_AGENT_SPEED,
                            maxSpeed=MAX_AGENT_SPEED, minDecisiveness=MIN_DECISIVENESS, maxDecisiveness=MAX_DECISIVENESS,
                            minNavSkills=MIN_NAV_SKILLS, maxNavSkills=MAX_NAV_SKILLS, minEstAccuracy=MIN_QUALITY_MISJUDGMENT,
                            maxEstAccuracy=MAX_QUALITY_MISJUDGMENT, maxSearchDist=MAX_SEARCH_DIST,
                            findSitesEasily=FIND_SITES_EASILY, commitSpeedFactor=COMMIT_SPEED_FACTOR,
                            drawFarAgents=DRAW_FAR_AGENTS):
        if numAgents < 0 or numAgents > MAX_AGENTS:
            raise InputError("Number of agents must be between 0 and " + str(MAX_AGENTS), numAgents)
        for i in range(0, numAgents):
            agent = Agent(self.world, self.world.getHub(), homogenousAgents, minSpeed, maxSpeed, minDecisiveness, maxDecisiveness,
                          minNavSkills, maxNavSkills, minEstAccuracy, maxEstAccuracy, self.world.hubLocation, maxSearchDist,
                          findSitesEasily, commitSpeedFactor)
            AgentDisplay.drawFarAgents = drawFarAgents
            agent.setState(AtNestState(agent))
            self.world.agentList.append(agent)
            self.world.agentGroups[i % 10].append(agent)

    def runSimulation(self):
        self.initializeRequest()
        foundNewHome = False

        self.timer.start()

        try:
            while not foundNewHome and not self.timeRanOut:
                if Display.shouldDraw:
                    self.userControls.handleEvents()
                    Display.screen.fill(SCREEN_COLOR)
                agentRectList = self.getAgentRectList()
                self.update(agentRectList)
                if Display.shouldDraw:
                    self.draw()
                foundNewHome = self.checkIfSimulationEnded()
        except GameOver:
            pass

        return self.finish()

    def initializeRequest(self):
        pass  # The method is overridden by simulations that send requests to rest APIs

    def getAgentRectList(self):
        agentRectList = []
        for agent in self.world.agentList:
            agentRectList.append(agent.getAgentRect())
        return agentRectList

    def update(self, agentRectList):
        self.setNextRound()
        if Display.shouldDraw:
            self.graphs.setRemainingTime(self.timer.getRemainingTime(None))
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
            try:
                self.updateAgent(agent, agentRectList)
                self.world.updatePaths(agent)
            except IndexError:
                self.world.removeAgent(agent)

    @abstractmethod
    def updateAgent(self, agent, agentRectList):
        pass

    def report(self, agentRectList):
        pass

    def checkIfSimulationEnded(self):
        for site in self.world.siteList:
            if site.getQuality() != -1 and site.agentCount >= len(self.world.agentList) * self.convergenceFraction:
                self.chosenHome = site
                return True
            else:
                self.chosenHome = None
        return False

    def timeOut(self):
        print("The interface time has run out.")
        self.timeRanOut = True

    def finish(self):
        if Display.shouldDraw:
            Display.drawFinish(Display.screen)
            pygame.display.flip()
        if self.shouldRecord:
            self.write()
        self.determineChosenHome()
        return self.printResults()

    def save(self):
        pass

    def write(self):
        pass

    def determineChosenHome(self):
        self.chosenHome = self.world.siteList[0]
        for home in self.world.siteList:
            if home.agentCount > self.chosenHome.agentCount:
                self.chosenHome = home

    def printResults(self):
        print(str(self.chosenHome.agentCount) + " out of " + str(len(self.world.agentList)) + " agents made it to the new home.")
        simulationTime = 10000  # Large number that means the agents did not find the new home in time.
        if not self.timeRanOut:
            simulationTime = self.timer.simulationDuration - self.timer.getRemainingTime(None)
            print("The interface took " + str(simulationTime) + " seconds to complete.")
            pygame.quit()
            self.timer.cancel()
        print("Their home is ranked " + str(self.chosenHome.getQuality()) + "/255.")
        if self.useRestAPI:
            self.sendResults(self.chosenHome, simulationTime)
        return self.chosenHome.getQuality(), simulationTime

    def sendResults(self, chosenSite, simulationTime):
        pass

    def setDisplayVariables(self):
        Display.screen = self.getScreen()
        Display.shouldDraw = self.getShouldDraw()
        SiteDisplay.knowSitePosAtStart = self.getKnowSitePosAtStart()

    @abstractmethod
    def getScreen(self):
        pass

    @abstractmethod
    def getShouldDraw(self):
        pass

    @abstractmethod
    def getKnowSitePosAtStart(self):
        pass

    @abstractmethod
    def getShouldDrawPaths(self):
        pass
