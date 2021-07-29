""" Colony Simulation Environment """
import datetime
import threading
import sys
sys.path.append("")
from colony.ColonyExceptions import *
from colony.AbstractColonySimulation import AbstractColonySimulation
from colony.Agents import *
from colony.World import World
from net.SendHubInfoRequest import SendHubInfoRequest


# TODO: Add ability to change parameters such as findSitesEasily during the simulation?
# TODO: Break Agents, Site, and World, into themselves and ""Builder classes


class ColonySimulation(AbstractColonySimulation):
    """ A class to run the simulation for ants finding their new home after the old one broke """

    def __init__(self, simulationDuration=SIM_DURATION, numSites=NUM_SITES, useRestAPI=USE_REST_API,
                 shouldRecord=SHOULD_RECORD, shouldDraw=SHOULD_DRAW, convergenceFraction=CONVERGENCE_FRACTION,
                 hubLocation=HUB_LOCATION, hubRadius=SITE_RADIUS, hubAgentCount=NUM_AGENTS,
                 sitePositions=SITE_POSITIONS, siteQualities=SITE_QUALITIES, siteRadii=SITE_RADII,
                 siteNoCloserThan=SITE_NO_CLOSER_THAN, siteNoFartherThan=SITE_NO_FARTHER_THAN,
                 knowSitePosAtStart=KNOW_SITE_POS_AT_START, canSelectAnywhere=CAN_SELECT_ANYWHERE, hubCanMove=HUB_CAN_MOVE):
        super().__init__(simulationDuration, numSites, useRestAPI, shouldRecord, shouldDraw, convergenceFraction,
                         hubLocation, hubRadius, hubAgentCount, sitePositions, siteQualities, siteRadii,
                         siteNoCloserThan, siteNoFartherThan, knowSitePosAtStart, canSelectAnywhere, hubCanMove)
        self.previousSendTime = datetime.datetime.now()

        if simulationDuration < 0 or simulationDuration > MAX_TIME:
            raise InputError("Simulation too short or too long", simulationDuration)
        if numSites < 0 or numSites > MAX_NUM_SITES:
            raise InputError("Can't be more sites than maximum value", numSites)

    def initializeWorld(self, numSites, hubLocation, hubRadius, hubAgentCount, sitePositions,
                        siteQualities, siteRadii, siteNoCloserThan, siteNoFartherThan, shouldDraw=True,
                        knowSitePosAtStart=KNOW_SITE_POS_AT_START, hubCanMove=HUB_CAN_MOVE):
        world = World(numSites, self.screen, hubLocation, hubRadius, hubAgentCount, sitePositions,
                      siteQualities, siteRadii, siteNoCloserThan, siteNoFartherThan, shouldDraw, knowSitePosAtStart,
                      hubCanMove)
        return world

    def initializeRequest(self):
        self.world.request = SendHubInfoRequest(self.world.agentList)

    def randomizeInitialState(self):
        self.world.randomizeState()

    def addAgents(self, numAgents, state, phase, assignedSiteIndex, startingPosition=None):
        if startingPosition is None:
            startingPosition = self.world.siteList[assignedSiteIndex].getPosition()
        for i in range(0, numAgents):
            agent = Agent(self.world, self.world.siteList[assignedSiteIndex], startingPosition=startingPosition)
            agent.assignedSite.agentCount += 1
            agent.setState(state(agent))
            agent.setPhase(phase)
            self.world.addAgent(agent)

    def updateSites(self):
        if self.shouldRecord:
            for site in self.world.siteList:
                self.recorder.recordSiteInfo(site)

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

    def report(self, agentRectList):
        hubRect = self.world.getHub().getSiteRect()
        hubAgentsIndices = hubRect.collidelistall(agentRectList)
        self.world.request.numAtHub = 0
        for agentIndex in hubAgentsIndices:
            agent = self.world.agentList[agentIndex]
            sites = agent.knownSites
            for siteIndex in range(0, len(sites)):
                if agent.knownSitesPositions[siteIndex] == sites[siteIndex].getPosition():
                    sites[siteIndex].wasFound = True
            agent.assignedSite.setEstimates(self.world.request.addAgentToSendRequest(agent, agentIndex))
        if self.useRestAPI:
            self.updateRestAPI()

    def updateRestAPI(self):
        now = datetime.datetime.now()
        if now > self.previousSendTime + datetime.timedelta(seconds=SECONDS_BETWEEN_SENDING_REQUESTS):
            self.previousSendTime = now
            thread = threading.Thread(target=self.world.request.sendHubInfo)
            thread.start()

    def save(self):
        if self.shouldRecord:
            self.recorder.save()

    def write(self):
        if self.shouldRecord:
            self.recorder.write()

    def sendResults(self, chosenSite, simulationTime):
        """ Tells the rest API which site the agents ended up at and how long it took them to get there """
        self.world.request.sendResults(chosenSite, simulationTime)
