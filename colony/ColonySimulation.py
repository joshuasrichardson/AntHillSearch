""" Colony Simulation Environment """
import datetime
import threading

from ColonyExceptions import *
from colony.AbstractColonySimulation import AbstractColonySimulation
from colony.Agents import *
from colony.World import World
from net.SendHubInfoRequest import SendHubInfoRequest
from recording.Recorder import Recorder


class ColonySimulation(AbstractColonySimulation):
    """ A class to run the simulation for ants finding their new home after the old one broke """

    def __init__(self, simulationDuration=SIM_DURATION, numSites=NUM_SITES,
                 shouldRecord=SHOULD_RECORD, shouldDraw=SHOULD_DRAW, convergenceFraction=CONVERGENCE_FRACTION,
                 hubLocation=HUB_LOCATION, hubRadius=DEFAULT_SITE_SIZE, hubAgentCount=NUM_AGENTS,
                 sitePositions=SITE_POSITIONS, siteQualities=SITE_QUALITIES, siteRadii=SITE_RADII,
                 siteNoCloserThan=SITE_NO_CLOSER_THAN, siteNoFartherThan=SITE_NO_FARTHER_THAN):
        super().__init__(simulationDuration, numSites, shouldRecord, shouldDraw, convergenceFraction,
                         hubLocation, hubRadius, hubAgentCount, sitePositions, siteQualities,
                         siteRadii, siteNoCloserThan, siteNoFartherThan)
        self.previousSendTime = datetime.datetime.now()
        self.request = None

        if simulationDuration < 0 or simulationDuration > MAX_TIME:
            raise InputError("Simulation too short or too long", simulationDuration)
        if numSites < 0 or numSites > MAX_NUM_SITES:
            raise InputError("Can't be more sites than maximum value", numSites)

    def initializeWorldAndRecorder(self, numSites, hubLocation, hubRadius, hubAgentCount, sitePositions,
                                   siteQualities, siteRadii, siteNoCloserThan, siteNoFartherThan):
        world = World(numSites, self.screen, hubLocation, hubRadius, hubAgentCount, sitePositions,
                      siteQualities, siteRadii, siteNoCloserThan, siteNoFartherThan)
        recorder = Recorder(len(world.agentList), world.siteList)
        return world, recorder

    def initializeRequest(self):
        self.request = SendHubInfoRequest(self.world.agentList)

    def updateAgent(self, agent, agentRectList):
        agent.updatePosition(None)

        agentRect = agent.getAgentRect()
        possibleNeighborList = agentRect.collidelistall(agentRectList)
        agentNeighbors = []
        for i in possibleNeighborList:
            agentNeighbors.append(self.world.agentList[i])
        agent.changeState(agentNeighbors)

        if self.shouldRecord:
            self.recorder.recordAgentInfo(agent)

    def updateRestAPI(self, agentRectList):
        hubRect = self.world.hub.getSiteRect()
        hubAgentsIndices = hubRect.collidelistall(agentRectList)
        self.request.numAtHub = 0
        for agentIndex in hubAgentsIndices:
            self.request.addAgentToSendRequest(self.world.agentList[agentIndex], agentIndex)
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
