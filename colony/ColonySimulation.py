""" Swarm Simulation Environment """
import threading
import time

import pygame

from colony.Agents import *
from ColonyExceptions import *
from World import *
from myPygameUtils import *
from states.AtNestState import AtNestState


class ColonySimulation:
    def __init__(self, numAgents, simulationDuration, numGoodSites, numSites):
        """ numAgents is the number of agents in the simulation.
        simulationDuration is the amount of time in seconds that the simulation can last
        numGoodSites is the number of top sites
        numSites number of total sites
        """
        # TODO: allow input files to be read and used instead of values and randomization

        self.numAgents = numAgents
        self.simulationDuration = simulationDuration
        self.numGoodSites = numGoodSites
        self.numSites = numSites
        self.agentList = []
        self.screen = create_screen()
        self.world = World(numSites, self.screen)
        self.states = np.zeros((NUM_POSSIBLE_STATES,))
        self.phases = np.zeros((NUM_POSSIBLE_PHASES,))
        self.chosenHome = None
        self.timeRanOut = False
        self.clickedAgents = []
        self.clickedSites = []
        self.dragSite = None
        self.timer = None
        self.pauseTime = 0

        if numAgents < 0 or numAgents > MAX_AGENTS:
            raise InputError("Number of agents must be between 1 and 200", numAgents)
        if simulationDuration < 0 or simulationDuration/TIME_STEP > MAX_STEPS:
            raise InputError("Simulation too short or too long", simulationDuration)
        if numGoodSites < 0 or numGoodSites > numSites or numGoodSites > MAX_M:
            raise InputError("Can't be more top sites than sites", numGoodSites)
        if numSites < 0 or numSites > MAX_N:
            raise InputError("Can't be more sites than maximum value", numSites)

    def runSimulation(self):
        # creates the number of agents specified by main
        for i in range(0, self.numAgents):
            agent = Agent(self.world)
            state = AtNestState(agent)
            agent.setState(state)
            self.agentList.append(agent)

        white = 255, 255, 255

        foundNewHome = False
        startTime = time.time()
        self.timer = threading.Timer(self.simulationDuration, self.timeOut)
        self.timer.start()

        while not foundNewHome and not self.timeRanOut:

            for event in pyg.event.get():
                if event.type == pyg.KEYDOWN and event.key == pyg.K_p:
                    self.pause(startTime)
                else:
                    self.handleEvent(event)
                if self.dragSite is not None:
                    self.dragSite.pos = pygame.mouse.get_pos()
            self.screen.fill(white)
            self.states = np.zeros((NUM_POSSIBLE_STATES,))
            self.phases = np.zeros((NUM_POSSIBLE_PHASES,))
            # Get list of agent rectangles
            agentRectList = []
            for agent in self.agentList:
                agentRectList.append(agent.getAgentRect())

            for agent in self.agentList:
                st = agent.getState()
                self.states[st] += 1
                ph = agent.phase
                self.phases[ph] += 1

            for agent in self.agentList:
                agent.drawAgent(self.screen)

                # Build adjacency list for observers, assessors, and pipers
                agent.updatePosition()

                agentRect = agent.getAgentRect()
                possibleNeighborList = agentRect.collidelistall(agentRectList)
                agentNeighbors = []
                for i in possibleNeighborList:
                    agentNeighbors.append(self.agentList[i])
                agent.changeState(agentNeighbors)

                if agent.assignedSite is not agent.hub and agent.assignedSite.agentCount == NUM_AGENTS:
                    foundNewHome = True
                    self.chosenHome = agent.assignedSite

            self.world.drawStateGraph(self.states)
            self.world.drawPhaseGraph(self.phases)
            self.world.drawWorldObjects()

            if len(self.clickedAgents) > 0:
                self.world.drawSelectedAgentInfo(self.clickedAgents[0])
            if len(self.clickedSites) > 0:
                agentsPositions = []
                for agent in self.agentList:
                    if agent.assignedSite is self.clickedSites[0]:
                        agentsPositions.append(agent.pos)
                        agent.select()
                self.world.drawSelectedSiteInfo(self.clickedSites[0], len(self.clickedAgents) > 0, agentsPositions)

            pygame.display.flip()

        if not self.timeRanOut:
            print("The agents found their new home!")
            pygame.quit()
            self.timer.cancel()
        print("Their home is ranked " + str(self.chosenHome.getQuality()) + "/255")

    def handleEvent(self, event):
        if event.type == pyg.MOUSEBUTTONUP:
            self.dragSite = None
            self.select(pygame.mouse.get_pos())
        if event.type == pyg.MOUSEBUTTONDOWN:
            self.drag(pygame.mouse.get_pos())
        if event.type == pyg.KEYDOWN and event.key == pyg.K_SPACE:
            self.go(pygame.mouse.get_pos())
        if event.type == pyg.KEYDOWN and event.key == pyg.K_a:
            self.go(pygame.mouse.get_pos())
            self.assignSelectedAgents(pygame.mouse.get_pos())
        if event.type == pyg.KEYDOWN and event.key == pyg.K_f:
            self.speedUp()
        if event.type == pyg.KEYDOWN and event.key == pyg.K_s:
            self.slowDown()
        if event.type == pyg.QUIT:
            pygame.quit()
            self.timer.cancel()
            raise GameOver("Exited Successfully")

    def select(self, mousePos):
        # Unselect all agents and sites
        for a in self.agentList:
            a.unselect()
        for s in self.world.siteList:
            s.unselect()
        # get a list of all sprites that are under the mouse cursor
        self.clickedAgents = [s for s in self.agentList if s.agentRect.collidepoint(mousePos)]
        self.clickedSites = [s for s in self.world.siteList if s.siteRect.collidepoint(mousePos)]
        if len(self.clickedAgents) > 0:      # for a in self.clickedAgents:
            self.clickedAgents[0].select()   # a.select()
        if len(self.clickedSites) > 0:       # for s in self.clickedSites:
            self.clickedSites[0].select()    # s.select()

    def drag(self, mousePos):
        self.clickedSites = [s for s in self.world.siteList if s.siteRect.collidepoint(mousePos)]
        if len(self.clickedSites) > 0:
            self.dragSite = self.clickedSites[0]

    def go(self, mousePos):
        print(str(mousePos))
        for a in self.agentList:
            if a.isSelected:
                a.target = mousePos
                from states.GoState import GoState
                a.setState(GoState(a))

    def assignSelectedAgents(self, mousePos):
        sitesUnderMouse = [s for s in self.world.siteList if s.siteRect.collidepoint(mousePos)]
        if len(sitesUnderMouse) > 0:
            for a in self.agentList:
                if a.isSelected:
                    a.assignSite(sitesUnderMouse[0])

    def speedUp(self):
        for a in self.agentList:
            a.speed *= 1.2
            a.speedCoefficient *= 1.2

    def slowDown(self):
        for a in self.agentList:
            a.speed /= 1.2
            a.speedCoefficient /= 1.2

    def pause(self, startTime):
        self.world.drawPause()
        pygame.display.flip()
        startPauseTime = time.time()
        runTime = startPauseTime - self.pauseTime - startTime
        remainingTime = self.simulationDuration - runTime
        print("Remaining time: " + str(remainingTime))
        self.timer.cancel()
        paused = True
        while paused:
            for event in pyg.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    paused = False
                else:
                    self.handleEvent(event)
        self.pauseTime += time.time() - startPauseTime
        self.timer = threading.Timer(remainingTime, self.timeOut)
        self.timer.start()

    def timeOut(self):
        print("The simulation time has run out.")
        self.chosenHome = self.world.siteList[0]
        for home in self.world.siteList:
            if home.agentCount > self.chosenHome.agentCount:
                self.chosenHome = home
        print(str(self.chosenHome.agentCount) + " out of " + str(NUM_AGENTS) + " agents made it to the new home.")
        self.timeRanOut = True
