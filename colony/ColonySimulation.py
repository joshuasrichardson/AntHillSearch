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

    def __init__(self, numAgents=NUM_AGENTS, simulationDuration=SIM_DURATION, numSites=NUM_SITES,
                 shouldRecord=SHOULD_RECORD, shouldDraw=SHOULD_DRAW, convergenceFraction=CONVERGENCE_FRACTION,
                 hubLocation=HUB_LOCATION, hubRadius=DEFAULT_SITE_SIZE, hubAgentCount=NUM_AGENTS,
                 sitePositions=SITE_POSITIONS, siteQualities=SITE_QUALITIES, siteRadii=SITE_RADII,
                 siteNoCloserThan=SITE_NO_CLOSER_THAN, siteNoFartherThan=SITE_NO_FARTHER_THAN):
        self.numAgents = numAgents
        super().__init__(simulationDuration, numSites, shouldRecord, shouldDraw, convergenceFraction,
                         hubLocation, hubRadius, hubAgentCount, sitePositions, siteQualities,
                         siteRadii, siteNoCloserThan, siteNoFartherThan)
        self.previousSendTime = datetime.datetime.now()
        self.request = None

        if numAgents < 0 or numAgents > MAX_AGENTS:
            raise InputError("Number of agents must be between 1 and 200", numAgents)
        if simulationDuration < 0 or simulationDuration > MAX_TIME:
            raise InputError("Simulation too short or too long", simulationDuration)
        if numSites < 0 or numSites > MAX_NUM_SITES:
            raise InputError("Can't be more sites than maximum value", numSites)

    def getRecorder(self):
        return Recorder(self.numAgents, self.world.siteList)

    def getNumAgents(self):
        return self.numAgents

    def initializeRequest(self):
        self.request = SendHubInfoRequest(self.agentList)

    def updateAgent(self, agent, agentRectList):
        agent.updatePosition(None)

        agentRect = agent.getAgentRect()
        possibleNeighborList = agentRect.collidelistall(agentRectList)
        agentNeighbors = []
        for i in possibleNeighborList:
            agentNeighbors.append(self.agentList[i])
        agent.changeState(agentNeighbors)

        if self.shouldRecord:
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
