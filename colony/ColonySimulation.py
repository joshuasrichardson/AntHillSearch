""" Swarm Simulation Environment """
import threading

from colony.Agents import *
from ColonyExceptions import *
from World import *
from myPygameUtils import *
from states.AtNestState import AtNestState
from user.Controls import Controls
from colony.SimulationTimer import SimulationTimer


class ColonySimulation:
    def __init__(self, numAgents, simulationDuration, numGoodSites, numSites):
        """ numAgents is the number of agents in the simulation.
        simulationDuration is the amount of time in seconds that the simulation can last
        numGoodSites is the number of top sites
        numSites number of total sites
        """
        # TODO: allow input files to be read and used instead of values and randomization

        self.numAgents = numAgents
        self.numGoodSites = numGoodSites
        self.numSites = numSites
        self.agentList = []
        self.screen = create_screen()
        self.world = World(numSites, self.screen)
        self.states = np.zeros((NUM_POSSIBLE_STATES,))
        self.phases = np.zeros((NUM_POSSIBLE_PHASES,))
        self.chosenHome = None
        self.timeRanOut = False
        self.timer = SimulationTimer(simulationDuration, threading.Timer(simulationDuration, self.timeOut), self.timeOut)
        self.userControls = Controls(self.timer, self.agentList, self.world)

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

        self.timer.start()

        while not foundNewHome and not self.timeRanOut:

            self.userControls.handleEvents()
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
            self.userControls.drawChanges()
            pygame.display.flip()

        if not self.timeRanOut:
            print("The agents found their new home!")
            pygame.quit()
            self.timer.cancel()
        print("Their home is ranked " + str(self.chosenHome.getQuality()) + "/255")

    def timeOut(self):
        print("The simulation time has run out.")
        self.chosenHome = self.world.siteList[0]
        for home in self.world.siteList:
            if home.agentCount > self.chosenHome.agentCount:
                self.chosenHome = home
        print(str(self.chosenHome.agentCount) + " out of " + str(NUM_AGENTS) + " agents made it to the new home.")
        self.timeRanOut = True
