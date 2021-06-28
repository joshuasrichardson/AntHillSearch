import threading

from colony.Agents import *
from colony.World import *

from colony.World import World
from command.DrawPhaseGraphCommand import DrawPhaseGraphCommand
from command.DrawStateGraphCommand import DrawStateGraphCommand
from command.DrawWorldObjectsCommand import DrawWorldObjectsCommand
from command.FillCommand import FillCommand
from command.FlipCommand import FlipCommand
from recording.Recorder import Recorder
from command.DrawAgentCommand import DrawAgentCommand
from command.UpdatePositionCommand import UpdatePositionCommand
from colony.myPygameUtils import *
from states.AtNestState import AtNestState
from user.Controls import Controls
from colony.SimulationTimer import SimulationTimer


class RecordingPlayer:
    def __init__(self, simulationDuration, numGoodSites, numSites):
        """ numAgents is the number of agents in the simulation.
        simulationDuration is the amount of time in seconds that the simulation can last
        numGoodSites is the number of top sites
        numSites number of total sites
        """
        # TODO: allow input files to be read and used instead of values and randomization

        self.numGoodSites = numGoodSites
        self.numSites = numSites
        self.agentList = []
        self.screen = createScreen()
        self.world = World(numSites, self.screen)
        self.recorder = Recorder(None, None)
        self.recorder.read()
        self.numAgents = self.recorder.numAgents
        for i in range(0, len(self.recorder.sites)):
            self.world.siteList[i].pos = self.recorder.sites[i].pos
            self.world.siteList[i].radius = self.recorder.sites[i].radius
            self.world.siteList[i].quality = self.recorder.sites[i].quality
            self.world.siteList[i].setPosition(self.recorder.sites[i].pos)
            if self.world.siteList[i].quality != -1:
                self.world.siteList[i].color = (255 - self.world.siteList[i].quality, self.world.siteList[i].quality, 0)
        self.states = np.zeros((NUM_POSSIBLE_STATES,))
        self.phases = np.zeros((NUM_POSSIBLE_PHASES,))
        self.chosenHome = None
        self.timeRanOut = False
        self.timer = SimulationTimer(simulationDuration, threading.Timer(simulationDuration, self.timeOut), self.timeOut)
        self.userControls = Controls(self.timer, self.agentList, self.world)

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
            # fillCommand = FillCommand(white, self.screen)
            # fillCommand.execute()
            # self.recorder.record(fillCommand)
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

            pos = -1
            for agent in self.agentList:
                agent.drawAgent(self.screen)
                # drawAgentCommand = DrawAgentCommand(agent, self.screen)
                # drawAgentCommand.execute()
                # self.recorder.record(drawAgentCommand)

                # Build adjacency list for observers, assessors, and pipers
                pos = self.recorder.getNextPosition()
                if pos == -1:
                    break
                updatePositionCommand = UpdatePositionCommand(agent, pos)
                updatePositionCommand.execute()

                agentRect = agent.getAgentRect()
                possibleNeighborList = agentRect.collidelistall(agentRectList)
                agentNeighbors = []
                for i in possibleNeighborList:
                    agentNeighbors.append(self.agentList[i])
                agent.changeState(agentNeighbors)

            if pos == -1:
                break

            self.world.drawStateGraph(self.states)
            # drawSGCommand = DrawStateGraphCommand(self.world, self.states)
            # drawSGCommand.execute()
            # self.recorder.record(drawSGCommand)
            self.world.drawPhaseGraph(self.phases)
            # drawPGCommand = DrawPhaseGraphCommand(self.world, self.phases)
            # drawPGCommand.execute()
            # self.recorder.record(drawPGCommand)
            self.world.drawWorldObjects()
            # drawWOCommand = DrawWorldObjectsCommand(self.world)
            # drawWOCommand.execute()
            # self.recorder.record(drawWOCommand)

            self.userControls.drawChanges()
            pygame.display.flip()
            # flipCommand = FlipCommand()
            # flipCommand.execute()
            # self.recorder.record(flipCommand)

            for site in self.world.siteList:
                if site is not self.world.siteList[len(self.world.siteList) - 1] and site.agentCount == NUM_AGENTS:
                    foundNewHome = True
                    self.chosenHome = site

        if not self.timeRanOut:
            print("The agents found their new home!")
            pygame.quit()
            self.timer.cancel()
        if self.chosenHome is not None:
            print("Their home is ranked " + str(self.chosenHome.getQuality()) + "/255")

    def timeOut(self):
        print("The simulation time has run out.")
        self.chosenHome = self.world.siteList[0]
        for home in self.world.siteList:
            if home.agentCount > self.chosenHome.agentCount:
                self.chosenHome = home
        print(str(self.chosenHome.agentCount) + " out of " + str(NUM_AGENTS) + " agents made it to the new home.")
        self.timeRanOut = True
