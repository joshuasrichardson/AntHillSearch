""" Colony Simulation Environment """
import datetime
import threading
from abc import ABC

from config import Config
from ColonyExceptions import *
from Constants import *
from display import WorldDisplay
from interface.Simulation import Simulation
from model.World import World
from model.builder import AgentBuilder
from net.HubInfoRequest import HubInfoRequest


class LiveSimulation(Simulation, ABC):
    """ A class to run the interface for ants finding their new home after the old one broke """

    def __init__(self):
        super().__init__()
        self.previousSendTime = datetime.datetime.now()

        if Config.SIM_DURATION < 0 or Config.SIM_DURATION > MAX_TIME:
            raise InputError("Simulation too short or too long", Config.SIM_DURATION)
        if Config.NUM_SITES < 0 or Config.NUM_SITES > MAX_NUM_SITES:
            raise InputError("Can't be more sites than maximum value", Config.NUM_SITES)

    def initializeWorld(self):
        self.world = World(Config.NUM_HUBS, Config.NUM_SITES, Config.HUB_LOCATIONS, Config.HUB_RADII,
                           Config.HUB_AGENT_COUNTS, Config.SITE_POSITIONS, Config.SITE_QUALITIES, Config.SITE_RADII,
                           Config.SITE_RADIUS, Config.NUM_PREDATORS, Config.PRED_POSITIONS)
        self.initializeAgentList()
        if Config.SHOULD_DRAW and Config.SHOULD_DRAW_FOG:
            WorldDisplay.initFog(self.world.hubs)

        return self.world

    def initializeAgentList(self):
        super().initializeAgentList()
        self.world.request = HubInfoRequest(self.world.agentList)

    def randomizeInitialState(self):
        self.world.randomizeState()

    def addAgents(self, numAgents, state, phase, assignedSiteIndex, startingPosition=None):
        if startingPosition is None:
            startingPosition = self.world.siteList[assignedSiteIndex].getPosition()
        for i in range(0, numAgents):
            agent = AgentBuilder.getNewAgent(self.world, self.world.siteList[assignedSiteIndex], startingPosition)
            agent.prevReportedSite = agent.assignedSite
            agent.assignedSite.agentCount += 1
            agent.assignedSite.estimatedAgentCount += 1
            agent.assignedSite.agentCounts[agent.getHubIndex()] += 1
            agent.setState(state(agent))
            agent.setPhase(phase)
            self.world.addAgent(agent)

    def update(self, agentRectList):
        super().update(agentRectList)
        self.setSitesEstimates(agentRectList)
        if Config.USE_REST_API:
            self.updateRestAPI()

    def updateSites(self):
        if Config.SHOULD_RECORD and Config.RECORD_ALL:
            for site in self.world.siteList:
                self.recorder.recordSiteInfo(site)

    def getNeighbors(self, bugRect, agentRectList):
        possibleNeighborList = bugRect.collidelistall(agentRectList)
        agentNeighbors = []
        for i in possibleNeighborList:
            agentNeighbors.append(self.world.agentList[i])
        return agentNeighbors

    def updateAgent(self, agent, agentRectList):
        if agent.getStateNumber() != DEAD:
            agent.moveForward()
            if Config.SHOULD_DRAW:
                agent.clearFog()

            agentNeighbors = self.getNeighbors(agent.getRect(), agentRectList)
            agent.doStateActions(agentNeighbors)

        if Config.SHOULD_RECORD and Config.RECORD_ALL:
            self.recorder.recordAgentInfo(agent)

    def updatePredator(self, predator, agentRectList):
        predator.moveForward()
        agentNeighbors = self.getNeighbors(predator.getRect(), agentRectList)
        predator.attack(agentNeighbors)

        if Config.SHOULD_RECORD and Config.RECORD_ALL:
            self.recorder.recordPredatorPosition(predator.pos)
            self.recorder.recordPredatorAngle(predator.angle)

    def setSitesEstimates(self, agentRectList):
        hubRects = self.world.getHubsRects()
        self.world.request.numAtHub = 0
        for hubRect in hubRects:  # For each hub
            hubAgentsIndices = hubRect.collidelistall(agentRectList)
            try:
                for agentIndex in hubAgentsIndices:  # For each agent currently at that hub
                    self.estimateAgentsSites(agentIndex)
            except IndexError:
                print("IndexError in LiveSimulation.setSitesEstimates. ")

    def estimateAgentsSites(self, agentIndex):
        agent = self.world.agentList[agentIndex]
        self.updateSiteAgentCountEst(agent)
        sites = agent.knownSites
        for siteIndex in range(len(sites)):  # For each site that the agent knows about
            if agent.knownSitesPositions[siteIndex] == sites[siteIndex].getPosition():
                sites[siteIndex].wasFound = True
                # If the site's estimates were not reported before the agent got assigned to another site, report them here.
                if sites[siteIndex].estimatedPosition is None and sites[siteIndex].getQuality() != -1:
                    sites[siteIndex].setEstimates(agent.estimateSitePosition(sites[siteIndex]),
                                                  agent.estimateQuality(sites[siteIndex]),
                                                  sites[siteIndex].estimatedAgentCount,
                                                  agent.estimateRadius(sites[siteIndex]))
        try:
            estimates = self.world.request.addAgentToHubInfo(agent, agentIndex)
            agent.assignedSite.setEstimates(*estimates)
            agent.assignedSite.updateBlur()
        except AttributeError:
            pass  # If the agent is killed by a hub, this exception will be thrown here.
        self.updatePredatorWarnings(agent)

    @staticmethod
    def updateSiteAgentCountEst(agent):
        if agent.prevReportedSite is not agent.assignedSite:
            agent.prevReportedSite.estimatedAgentCount -= 1
            agent.assignedSite.estimatedAgentCount += 1
            agent.prevReportedSite = agent.assignedSite

    @staticmethod
    def updatePredatorWarnings(agent):
        if len(agent.recentlySeenPredatorPositions) > 0:
            for pos in agent.recentlySeenPredatorPositions:
                agent.world.addDangerZone(pos)
            agent.recentlySeenPredatorPositions.clear()

    def updateRestAPI(self):
        now = datetime.datetime.now()
        if now > self.previousSendTime + datetime.timedelta(seconds=Config.SECONDS_BETWEEN_SENDING_REQUESTS):
            self.previousSendTime = now
            thread = threading.Thread(target=self.world.request.sendHubInfo)
            thread.start()

    def save(self):
        if Config.SHOULD_RECORD:
            self.recorder.save()

    def write(self):
        self.recorder.write()

    def sendResults(self, results):
        """ Tells the rest API which site the agents ended up at and how long it took them to get there,
         and records result information in a .json file"""
        if Config.USE_REST_API:
            self.world.request.sendResultsToAPI(results)
        if Config.SHOULD_RECORD:
            self.recorder.writeResults(results)
