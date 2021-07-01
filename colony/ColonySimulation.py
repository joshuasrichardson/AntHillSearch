""" Colony Simulation Environment """
import datetime
import threading

import requests

from colony.Agents import *
from ColonyExceptions import *
from World import *
from command.DrawPhaseGraphCommand import DrawPhaseGraphCommand
from command.DrawStateGraphCommand import DrawStateGraphCommand
from command.DrawWorldObjectsCommand import DrawWorldObjectsCommand
from command.FillCommand import FillCommand
from command.FlipCommand import FlipCommand
from net.SendHubInfoRequest import SendHubInfoRequest
from recording.Recorder import Recorder
from command.DrawAgentCommand import DrawAgentCommand
from command.UpdatePositionCommand import UpdatePositionCommand
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

        self.numAgents = numAgents
        self.numGoodSites = numGoodSites
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
        self.recorder = Recorder(numAgents, self.world.siteList)

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
        connected = True
        previousSendTime = datetime.datetime.now()
        request = SendHubInfoRequest(self.agentList)

        self.timer.start()

        while not foundNewHome and not self.timeRanOut:

            self.userControls.handleEvents()
            self.screen.fill(white)  #
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

            for agent in self.agentList:
                agent.drawAgent(self.screen)  #
                # drawAgentCommand = DrawAgentCommand(agent, self.screen)
                # drawAgentCommand.execute()
                # self.recorder.record(drawAgentCommand)

                # Build adjacency list for observers, assessors, and pipers
                pos = agent.getNewPosition()
                self.recorder.recordPosition(pos)
                agent.updatePosition(pos)  #
                # updatePositionCommand = UpdatePositionCommand(agent, pos)
                # self.recorder.record(updatePositionCommand)
                # updatePositionCommand.execute()

                agentRect = agent.getAgentRect()
                possibleNeighborList = agentRect.collidelistall(agentRectList)
                agentNeighbors = []
                for i in possibleNeighborList:
                    agentNeighbors.append(self.agentList[i])
                agent.changeState(agentNeighbors)

            hubRect = self.world.siteList[len(self.world.siteList) - 1].getAgentRect()
            hubAgentsIndices = hubRect.collidelistall(agentRectList)
            request.numAtHub = 0
            for agentIndex in hubAgentsIndices:
                request.addAgentToSendRequest(self.agentList[agentIndex], agentIndex)
            now = datetime.datetime.now()
            if connected and now > previousSendTime + datetime.timedelta(seconds=SECONDS_BETWEEN_SENDING_REQUESTS):
                previousSendTime = now
                # try:
                thread = threading.Thread(target=request.sendHubInfo)
                thread.start()
                # except:
                #     connected = False
                #     print("Not connected to the Rest API")

            self.world.drawStateGraph(self.states)  #
            # drawSGCommand = DrawStateGraphCommand(self.world, self.states)
            # drawSGCommand.execute()
            # self.recorder.record(drawSGCommand)
            self.world.drawPhaseGraph(self.phases)  #
            # drawPGCommand = DrawPhaseGraphCommand(self.world, self.phases)
            # drawPGCommand.execute()
            # self.recorder.record(drawPGCommand)
            self.world.drawWorldObjects()  #
            # drawWOCommand = DrawWorldObjectsCommand(self.world)
            # drawWOCommand.execute()
            # self.recorder.record(drawWOCommand)

            self.userControls.drawChanges()
            pygame.display.flip()  #
            # flipCommand = FlipCommand()
            # flipCommand.execute()
            # self.recorder.record(flipCommand)

            for site in self.world.siteList:
                if site is not self.world.siteList[len(self.world.siteList) - 1] and site.agentCount == NUM_AGENTS:
                    foundNewHome = True
                    self.chosenHome = site

        # val = input("Replay? (y/n)")
        # if val is "y":
        #     self.recorder.replay()
        self.recorder.save()
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
