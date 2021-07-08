import threading
from abc import ABC, abstractmethod

import numpy as np
import pygame

from Constants import *
from colony.Agents import Agent
from colony.SimulationTimer import SimulationTimer
from colony.World import World
from colony.myPygameUtils import createScreen
from states.AtNestState import AtNestState
from user.Controls import Controls


class AbstractColonySimulation(ABC):
    """ Runs most of the colony simulation but leaves some details to classes that inherit this class """

    def __init__(self, simulationDuration, numSites):
        """ numAgents is the number of agents in the simulation.
        simulationDuration is the amount of time in seconds that the simulation can last
        numGoodSites is the number of top sites
        numSites number of total sites """

        self.numSites = numSites
        self.agentList = []
        self.screen = createScreen()
        self.world = World(numSites, self.screen)
        self.states = np.zeros((NUM_POSSIBLE_STATES,))
        self.phases = np.zeros((NUM_POSSIBLE_PHASES,))
        self.chosenHome = None
        self.timeRanOut = False
        self.timer = SimulationTimer(simulationDuration, threading.Timer(simulationDuration, self.timeOut), self.timeOut)
        self.userControls = Controls(self.timer, self.agentList, self.world)
        self.recorder = self.getRecorder()
        self.numAgents = self.getNumAgents()

    @abstractmethod
    def getRecorder(self):
        pass

    @abstractmethod
    def getNumAgents(self):
        pass

    def runSimulation(self):
        self.initializeAgentList()
        self.initializeRequest()
        white = 255, 255, 255
        foundNewHome = False

        self.timer.start()

        while not foundNewHome and not self.timeRanOut:
            self.userControls.handleEvents()
            self.screen.fill(white)
            agentRectList = self.getAgentRectList()

            # try:
            self.updateStateAndPhaseCounts()
            self.updateAgents(agentRectList)
            self.updateRestAPI(agentRectList)
            # except:
            #     break

            self.world.drawStateGraph(self.states)
            self.world.drawPhaseGraph(self.phases)
            self.world.drawWorldObjects()
            self.userControls.drawChanges()
            pygame.display.flip()

            foundNewHome = self.checkIfSimulationEnded()

        self.finish()

    def initializeAgentList(self):
        for i in range(0, self.numAgents):
            agent = Agent(self.world)
            state = AtNestState(agent)
            agent.setState(state)
            self.agentList.append(agent)

    def initializeRequest(self):
        pass  # The method is overridden by simulations that send requests to rest APIs

    def getAgentRectList(self):
        agentRectList = []
        for agent in self.agentList:
            agentRectList.append(agent.getAgentRect())
        return agentRectList

    def updateStateAndPhaseCounts(self):
        self.states = np.zeros((NUM_POSSIBLE_STATES,))
        self.phases = np.zeros((NUM_POSSIBLE_PHASES,))
        for agent in self.agentList:
            st = agent.getState()
            self.states[st] += 1
            ph = agent.phase
            self.phases[ph] += 1

    def updateAgents(self, agentRectList):
        for agent in self.agentList:
            agent.drawAgent(self.screen)
            self.updateAgent(agent, agentRectList)

    @abstractmethod
    def updateAgent(self, agent, agentRectList):
        pass

    def updateRestAPI(self, agentRectList):
        pass

    def checkIfSimulationEnded(self):
        for site in self.world.siteList:
            if site is not self.world.siteList[len(self.world.siteList) - 1]\
                    and site.agentCount == NUM_AGENTS * CONVERGENCE_FRACTION:
                self.chosenHome = site
                return True
            else:
                self.chosenHome = self.world.siteList[len(self.world.siteList) - 1]
        return False

    def timeOut(self):
        print("The simulation time has run out.")
        self.timeRanOut = True

    def finish(self):
        self.world.drawFinish()
        pygame.display.flip()
        self.recorder.save()
        self.determineChosenHome()
        self.printResults()

    def determineChosenHome(self):
        self.chosenHome = self.world.siteList[0]
        for home in self.world.siteList:
            if home.agentCount > self.chosenHome.agentCount:
                self.chosenHome = home
        print(str(self.chosenHome.agentCount) + " out of " + str(NUM_AGENTS) + " agents made it to the new home.")

    def printResults(self):
        simulationTime = 10000  # Large number that means the agents did not find the new home in time.
        if not self.timeRanOut:
            simulationTime = SIM_DURATION - self.timer.getRemainingTime(None)
            print("The agents found their new home!")
            pygame.quit()
            self.timer.cancel()
        print("Their home is ranked " + str(self.chosenHome.getQuality()) + "/255")
        self.sendResults(self.chosenHome, simulationTime)

    def sendResults(self, chosenSite, simulationTime):
        pass
