""" Colony Simulation Environment """
import datetime
import threading

from ColonyExceptions import *
from colony.AbstractColonySimulation import AbstractColonySimulation
from colony.Agents import *
from net.SendHubInfoRequest import SendHubInfoRequest
from recording.Recorder import Recorder


class ColonySimulation(AbstractColonySimulation):
    """ A class to run the simulation for ants finding their new home after the old one broke """

    def __init__(self, numAgents, simulationDuration, numGoodSites, numSites):
        self.numAgents = numAgents
        super().__init__(simulationDuration, numGoodSites, numSites)
        self.connected = True
        self.previousSendTime = datetime.datetime.now()
        self.request = None

        if numAgents < 0 or numAgents > MAX_AGENTS:
            raise InputError("Number of agents must be between 1 and 200", numAgents)
        if simulationDuration < 0 or simulationDuration/TIME_STEP > MAX_STEPS:
            raise InputError("Simulation too short or too long", simulationDuration)
        if numGoodSites < 0 or numGoodSites > numSites or numGoodSites > MAX_M:
            raise InputError("Can't be more top sites than sites", numGoodSites)
        if numSites < 0 or numSites > MAX_N:
            raise InputError("Can't be more sites than maximum value", numSites)

    def getRecorder(self):
        return Recorder(self.numAgents, self.world.siteList)

    def getNumAgents(self):
        return self.numAgents

    def initializeRequest(self):
        self.request = SendHubInfoRequest(self.agentList)

    def updateAgent(self, agent, agentRectList):
        # Build adjacency list for observers, assessors, and pipers
        pos = agent.getNewPosition()
        agent.updatePosition(pos)
        self.recorder.recordAgentInfo(agent)

        agentRect = agent.getAgentRect()
        possibleNeighborList = agentRect.collidelistall(agentRectList)
        agentNeighbors = []
        for i in possibleNeighborList:
            agentNeighbors.append(self.agentList[i])
        agent.changeState(agentNeighbors)

    def updateRestAPI(self, agentRectList):
        hubRect = self.world.siteList[len(self.world.siteList) - 1].getAgentRect()
        hubAgentsIndices = hubRect.collidelistall(agentRectList)
        self.request.numAtHub = 0
        for agentIndex in hubAgentsIndices:
            self.request.addAgentToSendRequest(self.agentList[agentIndex], agentIndex)
        now = datetime.datetime.now()
        if now > self.previousSendTime + datetime.timedelta(seconds=SECONDS_BETWEEN_SENDING_REQUESTS):
            self.previousSendTime = now
            thread = threading.Thread(target=self.request.sendHubInfo)
            thread.start()

    def sendResults(self, chosenSite, simulationTime):
        """ Tells the rest API which site the agents ended up at and how long it took them to get there """
        self.request.sendResults(chosenSite.pos, SIM_DURATION - simulationTime)
