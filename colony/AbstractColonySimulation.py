import threading
from abc import ABC, abstractmethod

import numpy as np
import pygame

from Constants import *
from colony.Agents import Agent
from colony.ColonyExceptions import InputError, GameOver
from colony.SimulationTimer import SimulationTimer
from colony.myPygameUtils import createScreen
from recording.Recorder import Recorder
from states.AtNestState import AtNestState
from user.Controls import Controls


class AbstractColonySimulation(ABC):
    """ Runs most of the colony simulation but leaves some details to classes that inherit this class """

    def __init__(self, simulationDuration=SIM_DURATION, numSites=NUM_SITES, shouldReport=SHOULD_REPORT,
                 shouldRecord=SHOULD_RECORD, shouldDraw=SHOULD_DRAW, convergenceFraction=CONVERGENCE_FRACTION,
                 hubLocation=HUB_LOCATION, hubRadius=SITE_RADIUS, hubAgentCount=NUM_AGENTS, sitePositions=SITE_POSITIONS,
                 siteQualities=SITE_QUALITIES, siteRadii=SITE_RADII, siteNoCloserThan=SITE_NO_CLOSER_THAN,
                 siteNoFartherThan=SITE_NO_FARTHER_THAN):

        self.screen = createScreen(shouldDraw)  # The screen that the simulation is drawn on
        self.recorder = Recorder()  # The recorder that either records a live simulation or plays a recorded simulation
        self.world = self.initializeWorld(numSites, hubLocation, hubRadius, hubAgentCount, sitePositions,
                                          siteQualities, siteRadii, siteNoCloserThan, siteNoFartherThan, shouldDraw)  # The world that has all the sites and agents
        self.states = np.zeros((NUM_POSSIBLE_STATES,))  # List of the number of agents assigned to each state
        self.phases = np.zeros((NUM_POSSIBLE_PHASES,))  # List of the number of agents assigned to each phase
        self.chosenHome = None  # The site that most of the agents are assigned to when the simulation ends
        self.timeRanOut = False  # Whether there is no more time left in the simulation
        self.timer = SimulationTimer(simulationDuration, threading.Timer(simulationDuration, self.timeOut), self.timeOut)  # A timer to handle keeping track of when the simulation is paused or ends
        self.userControls = Controls(self.timer, self.world.agentList, self.world)  # And object to handle events dealing with user interactions

        self.shouldReport = shouldReport  # Whether the simulation should periodically report hub information to the rest API
        self.shouldRecord = shouldRecord  # Whether the simulation should be recorded
        self.shouldDraw = shouldDraw  # Whether the simulation should be drawn on the screen

        self.convergenceFraction = convergenceFraction  # The percentage of agents who need to be assigned to a site before the simulation will end

    @abstractmethod
    def initializeWorld(self, numSites, hubLocation, hubRadius, hubAgentCount, sitePositions,
                        siteQualities, siteRadii, siteNoCloserThan, siteNoFartherThan, shouldDraw):
        pass

    def setAgentList(self, agents):
        self.world.agentList = agents

    def initializeAgentList(self, numAgents=NUM_AGENTS, homogenousAgents=HOMOGENOUS_AGENTS, minSpeed=MIN_AGENT_SPEED,
                            maxSpeed=MAX_AGENT_SPEED, minDecisiveness=MIN_DECISIVENESS, maxDecisiveness=MAX_DECISIVENESS,
                            minNavSkills=MIN_NAV_SKILLS, maxNavSkills=MAX_NAV_SKILLS,
                            minEstAccuracy=MIN_QUALITY_MISJUDGMENT, maxEstAccuracy=MAX_QUALITY_MISJUDGMENT):
        if numAgents < 0 or numAgents > MAX_AGENTS:
            raise InputError("Number of agents must be between 1 and 200", numAgents)
        for i in range(0, numAgents):
            agent = Agent(self.world, self.world.hub, homogenousAgents, minSpeed, maxSpeed, minDecisiveness, maxDecisiveness,
                          minNavSkills, maxNavSkills, minEstAccuracy, maxEstAccuracy, self.world.hubLocation)
            agent.setState(AtNestState(agent))
            self.world.agentList.append(agent)

    def runSimulation(self):
        self.initializeRequest()
        white = 255, 255, 255
        foundNewHome = False

        self.timer.start()

        try:
            while not foundNewHome and not self.timeRanOut:
                if self.shouldDraw:
                    self.userControls.handleEvents()
                    self.screen.fill(white)
                agentRectList = self.getAgentRectList()
                self.update(agentRectList)
                if self.shouldDraw:
                    self.draw()
                foundNewHome = self.checkIfSimulationEnded()
        except GameOver:
            pass

        self.finish()

    def initializeRequest(self):
        pass  # The method is overridden by simulations that send requests to rest APIs

    def getAgentRectList(self):
        agentRectList = []
        for agent in self.world.agentList:
            agentRectList.append(agent.getAgentRect())
        return agentRectList

    def update(self, agentRectList):
        self.setNextRound()
        self.updateStateAndPhaseCounts()
        self.updateSites()
        self.updateAgents(agentRectList)
        self.save()
        self.updateRestAPI(agentRectList)

    def draw(self):
        self.world.drawStateGraph(self.states)
        self.world.drawPhaseGraph(self.phases)
        self.world.drawWorldObjects()
        self.userControls.drawChanges()
        pygame.display.flip()

    def setNextRound(self):
        pass

    def updateStateAndPhaseCounts(self):
        self.states = np.zeros((NUM_POSSIBLE_STATES,))
        self.phases = np.zeros((NUM_POSSIBLE_PHASES,))
        for agent in self.world.agentList:
            st = agent.getState()
            self.states[st] += 1
            ph = agent.phase
            self.phases[ph] += 1

    def updateSites(self):
        pass

    def updateAgents(self, agentRectList):
        for agent in self.world.agentList:
            try:
                self.updateAgent(agent, agentRectList)
                if self.shouldDraw:
                    agent.drawAgent(self.screen)
            except IndexError:
                self.world.removeAgent(agent)

    @abstractmethod
    def updateAgent(self, agent, agentRectList):
        pass

    def updateRestAPI(self, agentRectList):
        pass

    def checkIfSimulationEnded(self):
        for site in self.world.siteList:
            if site.getQuality() != -1 and site.agentCount == len(self.world.agentList) * self.convergenceFraction:
                self.chosenHome = site
                return True
            else:
                self.chosenHome = None
        return False

    def timeOut(self):
        print("The simulation time has run out.")
        self.timeRanOut = True

    def finish(self):
        if self.shouldDraw:
            self.world.drawFinish()
            pygame.display.flip()
        if self.shouldRecord:
            self.write()
        self.determineChosenHome()
        self.printResults()

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
            print("The simulation took " + str(simulationTime) + " seconds to complete.")
            pygame.quit()
            self.timer.cancel()
        print("Their home is ranked " + str(self.chosenHome.getQuality()) + "/255.")
        if self.shouldReport:
            self.sendResults(self.chosenHome, simulationTime)

    def sendResults(self, chosenSite, simulationTime):
        pass
