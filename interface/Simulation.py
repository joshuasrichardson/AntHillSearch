from abc import ABC, abstractmethod

import pygame

import Utils
from config import Config
from Constants import *
from display import Display
from display.buttons.PlayButton import PlayButton
from display.simulation.SimulationDisplay import SimulationDisplay
from display.simulation.WorldDisplay import drawWorldObjects
from ColonyExceptions import GameOver
from model.Timer import Timer
from model.builder import AgentBuilder
from model.states.simplified.Rest import RestState
from recording.Recorder import Recorder
from model.states.AtNestState import AtNestState
from user.Controls import Controls
from user.LimitedControls import LimitedControls
from user.NoControls import NoControls


class Simulation(ABC):
    """ An abstract class to run the simulation for ants finding their new home after the old one broke.
    Runs most of the colony simulation but leaves some details to classes that inherit this class """

    def __init__(self, numAgents=None, numSites=None, sitePositions=None, siteQualities=None):
        self.applyConfiguration(numAgents, numSites, sitePositions, siteQualities)  # update all the settings with the configuration file.
        Display.screen = self.getScreen()  # Set up the screen.
        self.recorder = Recorder()  # The recorder that either records a live interface or plays a recorded interface
        self.timeRanOut = False  # Whether there is no more time left in the interface
        self.timer = Timer(self.timeOut)  # A timer to handle keeping track of when the interface is paused or ends
        self.world = self.initializeWorld()  # The world that has all the sites and agents
        self.chosenHomes = self.initChosenHomes()  # The site that most of the agents are assigned to when the interface ends
        self.initialState = RestState if SIMPLIFY_STATES else AtNestState
        if Config.INTERFACE_NAME != "Empirical_Testing":
            self.simDisp = SimulationDisplay(self.world, self.timer)
            self.userControls = self.getControls()
            pauseButton = PlayButton(self.userControls, Display.screen.get_width() - 60, GRAPHS_TOP_LEFT[1])
            self.simDisp.setPauseButton(pauseButton)
        self.numRounds = 0

    @abstractmethod
    def initializeWorld(self):
        pass

    def initializeAgentList(self):
        self.initialState = RestState if SIMPLIFY_STATES else AtNestState
        for hubIndex, count in enumerate(self.world.initialHubAgentCounts):
            if hubIndex >= len(self.world.getHubs()):
                break
            for i in range(count):
                agent = AgentBuilder.getNewAgent(self.world, self.world.getHubs()[hubIndex])
                agent.setState(self.initialState(agent))
                self.world.agentList.append(agent)
                self.world.agentGroups[i % 10].append(agent)

    def initChosenHomes(self):
        chosenHomes = []
        for i in range(Config.NUM_HUBS):
            chosenHomes.append(self.world.siteList[0])
        return chosenHomes

    def runSimulation(self):
        foundNewHome = False
        self.timer.start()

        try:
            while not foundNewHome and not self.timeRanOut:
                self.runNextRound()
                foundNewHome = self.checkIfSimulationEnded()

        except GameOver as e:
            self.stopTimer()
            self.gameOver(e.message)

        self.stopTimer()
        return self.finish()

    def gameOver(self, errMessage):
        self.stopTimer()
        if errMessage == "Exiting":
            raise GameOver("Exited Successfully")

    def printNumRounds(self):
        roundCounts = []
        for i, hub in enumerate(self.world.getHubs()):
            if hub.roundCount == 0:
                rounds = self.timer.rounds
            else:
                rounds = hub.roundCount
            roundCounts.append(rounds)
            print(f"Colony {i + 1} took {rounds} rounds to finish.")
        return roundCounts

    def stopTimer(self):
        self.timer.cancel()

    def runNextRound(self):
        self.userControls.handleEvents()
        self.update(self.getAgentRectList())
        self.simDisp.displayScreen()
        self.timer.nextRound()

    def getAgentRectList(self):
        agentRectList = []
        for agent in self.world.agentList:
            agentRectList.append(agent.getRect())
        return agentRectList

    def update(self, agentRectList):
        self.setNextRound()
        self.world.updateStateAndPhaseCounts()
        self.world.updateDangerZones()
        self.updateSites()
        self.updateAgents(agentRectList)
        self.updatePredators(agentRectList)
        self.updateLadybugs(agentRectList)
        self.updateObstacles(agentRectList)
        self.recordDisplays()
        self.save()

    def setNextRound(self):
        pass

    def updateSites(self):
        pass

    def updateAgents(self, agentRectList):
        for i, agent in enumerate(self.world.agentList):
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

    def updateLadybugs(self, agentRectList):
        for ladybug in self.world.ladybugList:
            self.updateLadybug(ladybug, agentRectList)

    @abstractmethod
    def updateLadybug(self, ladybug, agentRectList):
        pass

    def updateObstacles(self, agentRectList):
        for obstacle in self.world.obstacleList:
            self.updateObstacle(obstacle, agentRectList)

    @abstractmethod
    def updateObstacle(self, obstacle, agentRectList):
        pass

    def recordDisplays(self):
        self.recorder.record(self)

    def checkIfSimulationEnded(self):
        """ Compare the number of agents at each site from each hub to the number of agents initially at each hub
        times the convergence fraction to see if the the agents from all hubs have converged to a new site. """
        numConverged = 0
        for siteIndex in range(len(self.world.getHubs()), len(self.world.siteList)):  # For each site that is not a hub,
            site = self.world.siteList[siteIndex]
            for hubIndex in range(len(self.world.getHubs())):  # For each hub,
                # If the number of agents assigned to the site is greater than or equal to the number needed to converge,
                if site.agentCounts[hubIndex] >= (self.world.initialHubAgentCounts[hubIndex] -
                                                  self.world.numDeadAgents[hubIndex]) * Config.CONVERGENCE_FRACTION > 0:
                    self.chosenHomes[hubIndex] = site  # Choose the site as a new home for the colony
                    numConverged += 1  # Increment the number of colonies converged
                    self.convergeHub(hubIndex)  # Save data about the converged colony
        for hubIndex in range(len(self.world.getHubs())):  # For each hub,
            if self.world.initialHubAgentCounts[hubIndex] == 0:  # If it didn't start with any agents,
                self.chosenHomes[hubIndex] = self.world.siteList[hubIndex]  # the chosen home for that colony is just its hub
                numConverged += 1  # Increment the number of colonies converged
                self.convergeHub(hubIndex)  # Save data about the converged colony
        return numConverged >= len(self.world.getHubs())  # If all the colonies have converged, the simulation is over

    def convergeHub(self, hubIndex):
        hub = self.world.getHubs()[hubIndex]
        if hub.time == 0:
            hub.time = self.timer.getRemainingTime()
            hub.roundCount = self.timer.rounds

    def timeOut(self):
        """ Method to be called when the simulation timer runs out. sets timeRanOut to True to break the main loop. """
        # print("The simulation time has run out.")
        self.timeRanOut = True

    def finish(self):
        if Config.SHOULD_RECORD:
            self.write()
        self.determineChosenHomes()
        results = self.printResults()
        self.sendResults(results)
        self.recorder.deleteExcessRecordings()
        if Config.SHOULD_DRAW:
            self.drawFinish(results)
        return results

    def drawFinish(self, results):
        done = False
        while not done:
            drawWorldObjects(self.world)
            Display.drawFinish(Display.screen, results)
            pygame.display.flip()
            done = self.userControls.handleLastEvents()

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
        numArrivals, numDeaths = self.printNumAgentsResults()
        positions = []
        for site in self.chosenHomes:
            positions.append(site.getPosition())
        results = {NUM_ROUNDS_NAME: self.printNumRounds(),
                   SIM_TIMES_NAME: self.printTimeResults(),
                   HOME_QUALITIES_NAME: self.printHomeQualities(),
                   HOME_POSITIONS_NAME: positions,
                   NUM_ARRIVALS_NAME: numArrivals,
                   NUM_DEAD_NAME: numDeaths,
                   TOTAL_NAME: self.world.initialHubAgentCounts,
                   IN_FLOOD_ZONE_NAME: self.areInFloodZone(self.chosenHomes)}
        return results

    def getNumDeadAgents(self):
        return self.world.numDeadAgents

    def printNumAgentsResults(self):
        numArrived = []
        numDead = self.getNumDeadAgents()
        for i in range(len(self.chosenHomes)):
            numArrived.append(self.chosenHomes[i].agentCounts[i])
            # print(f"{self.chosenHomes[i].agentCounts[i]}/{self.world.initialHubAgentCounts[i]} agents from "
            #       f"colony {i + 1} made it to the new home.")
        # for hubIndex in range(len(self.world.hubs)):
        #     print(f"{numDead[hubIndex]}/"
        #           f"{self.world.initialHubAgentCounts[hubIndex]} agents from colony {hubIndex + 1} died.")
        return numArrived, numDead

    def printTimeResults(self):
        times = []
        for i, hub in enumerate(self.world.getHubs()):
            simulationTime = round(Config.SIM_DURATION - self.timer.getRemainingTime())
            times.append(simulationTime)
            print(f"Colony {i + 1} took {simulationTime} seconds to finish.")
        return times

    def printHomeQualities(self):
        qualities = []
        # print("Their homes are ranked: ")
        for i, home in enumerate(self.chosenHomes):
            qualities.append(home.getQuality())
            # print(f"Colony {i + 1}: {home.getQuality()}/255.")
        return qualities

    def areInFloodZone(self, sites):
        inZone = []
        for site in sites:
            inZone.append(self.world.floodZone.overlaps(site.getSiteRect(), site.radius))
        return inZone

    def sendResults(self, results):
        pass

    def getScreen(self):
        """ Gets the screen to draw the simulation on (or None if the simulation will not be drawn) """
        return Display.createScreen()

    def getControls(self):
        """ Initializes and returns an object to handle user input """
        if SIMPLIFY_STATES:
            return NoControls(self.world.agentList, self.world, self.simDisp)
        if Config.FULL_CONTROL:
            return Controls(self.world.agentList, self.world, self.simDisp)
        return LimitedControls(self.world.agentList, self.world, self.simDisp)

    def applyConfiguration(self, numAgents=None, numSites=None, sitePositions=None, siteQualities=None):
        """ Sets the simulation values to match the values in {CONFIG_FILE_NAME} """
        Utils.copyJsonToConfig()
