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

    def __init__(self, numAgents, simulationDuration, numSites):
        self.numAgents = numAgents
        super().__init__(simulationDuration, numSites)
        self.connected = True
        self.previousSendTime = datetime.datetime.now()
        self.request = None

        if numAgents < 0 or numAgents > MAX_AGENTS:
            raise InputError("Number of agents must be between 1 and 200", numAgents)
        if simulationDuration < 0 or simulationDuration / TIME_STEP > MAX_STEPS:
            raise InputError("Simulation too short or too long", simulationDuration)
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
        agent.updatePosition(None)
        # self.recorder.recordAgentInfo(agent)

        agentRect = agent.getAgentRect()
        possibleNeighborList = agentRect.collidelistall(agentRectList)
        agentNeighbors = []
        for i in possibleNeighborList:
            agentNeighbors.append(self.agentList[i])
        agent.changeState(agentNeighbors)
        self.recorder.recordAgentInfo(agent)

    def updateRestAPI(self, agentRectList):
        hubRect = self.world.siteList[len(self.world.siteList) - 1].getSiteRect()
        hubAgentsIndices = hubRect.collidelistall(agentRectList)
        self.request.numAtHub = 0
        for agentIndex in hubAgentsIndices:
            self.request.addAgentToSendRequest(self.agentList[agentIndex], agentIndex)
        now = datetime.datetime.now()
        if now > self.previousSendTime + datetime.timedelta(seconds=SECONDS_BETWEEN_SENDING_REQUESTS):
            self.previousSendTime = now
            thread = threading.Thread(target=self.request.sendHubInfo)
            thread.start()

    def save(self):
        self.recorder.save()

    def sendResults(self, chosenSite, simulationTime):
        """ Tells the rest API which site the agents ended up at and how long it took them to get there """
        self.request.sendResults(chosenSite.pos, simulationTime)
