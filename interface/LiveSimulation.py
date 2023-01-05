""" Colony Simulation Environment """
import datetime
import threading
from abc import ABC

from config import Config
from ColonyExceptions import *
from Constants import *
from config.Config import SHOULD_RECORD
from interface.Simulation import Simulation
from model.World import World
from model.builder import AgentBuilder
from net.HubInfoRequest import HubInfoRequest


class LiveSimulation(Simulation, ABC):
    """ A class to run the interface for ants finding their new home after the old one broke.
     This simulation is live (as opposed to a recording player). """

    def __init__(self, numAgents=None, numSites=None, sitePositions=None, siteQualities=None):
        super().__init__(numAgents, numSites, sitePositions, siteQualities)
        self.previousSendTime = datetime.datetime.now()

        if Config.SIM_DURATION < 0 or Config.SIM_DURATION > MAX_TIME:
            raise InputError("Simulation too short or too long", Config.SIM_DURATION)
        if Config.NUM_SITES < 0 or Config.NUM_SITES > MAX_NUM_SITES:
            raise InputError("Can't be more sites than maximum value", Config.NUM_SITES)

    def initializeWorld(self):
        self.world = World(Config.NUM_HUBS, Config.NUM_SITES, Config.HUB_POSITIONS, Config.HUB_RADII,
                           Config.HUB_AGENT_COUNTS, Config.SITE_POSITIONS, Config.SITE_QUALITIES, Config.SITE_RADII,
                           Config.SITE_RADIUS, Config.NUM_PREDATORS, Config.PRED_POSITIONS, Config.NUM_LADYBUGS,
                           Config.LADYBUG_POSITIONS, Config.NUM_OBSTACLES, Config.OBSTACLE_POSITIONS)
        self.initializeAgentList()

        return self.world

    def initializeAgentList(self):
        super().initializeAgentList()
        self.world.request = HubInfoRequest(self.world.agentList, self.world.states, self.world.phases)

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
        """Updates predator locations and attacks neighboring agents"""
        predator.moveForward()
        agentNeighbors = self.getNeighbors(predator.getRect(), agentRectList)
        predator.attack(agentNeighbors)

        if Config.SHOULD_RECORD and Config.RECORD_ALL:
            self.recorder.recordPredatorPosition(predator.pos)
            self.recorder.recordPredatorAngle(predator.angle)

    def updateLadybug(self, ladybug, agentRectList):
        """Updates ladybug locations and helps neighboring agents"""
        ladybug.moveForward()
        agentNeighbors = self.getNeighbors(ladybug.getRect(), agentRectList)
        ladybug.help(agentNeighbors)

        if Config.SHOULD_RECORD and Config.RECORD_ALL:
            self.recorder.recordLadybugPosition(ladybug.pos)
            self.recorder.recordLadybugAngle(ladybug.angle)
            
    def updateObstacle(self, obstacle, agentRectList):
        """Updates obstacles to obstruct any colliding agents"""
        obstacle.setAgentNeighbors(self.getNeighbors(obstacle.getRect(), agentRectList))
        obstacle.obstruct()
        obstacleNeighbors = obstacle.getAgentNeighbors()
        oldNeighbors = obstacle.getOldNeighborList()
        if len(obstacleNeighbors) < len(oldNeighbors):  # If agent is leaving the obstacle
            for agent in oldNeighbors:
                if obstacleNeighbors.count(agent) == 0:  # If agent left this obstacle
                    agent.setAngle(agent.angleBeforeObstacle)  # Set agent angle to original course
        obstacle.setOldNeighborList(obstacleNeighbors)

    def setSitesEstimates(self, agentRectList):
        hubRects = self.world.getHubsRects()
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
                if sites[siteIndex].estimatedPosition is None and not sites[siteIndex].isHub():
                    if SHOULD_RECORD and agent.newReport:
                        self.recorder.recordAgentEstimates(agent, agentIndex)
                    sites[siteIndex].setEstimates(agent.estimateSitePosition(sites[siteIndex]),
                                                  agent.estimateQuality(sites[siteIndex]),
                                                  sites[siteIndex].estimatedAgentCount,
                                                  agent.estimateRadius(sites[siteIndex]))
        try:
            estimates = self.world.request.addAgentToHubInfo(agent, agentIndex)
            if SHOULD_RECORD and agent.newReport:
                agent.newReport = False
                self.recorder.recordAgentEstimates(agent, agentIndex)
            agent.assignedSite.setEstimates(*estimates)
            agent.assignedSite.updateBlur()
        except AttributeError:
            pass  # If the agent is killed by a hub, this exception will be thrown here.
        self.updatePredatorWarnings(agent)

    @staticmethod
    def updateSiteAgentCountEst(agent):
        if agent.prevReportedSite is not None and agent.prevReportedSite is not agent.assignedSite:
            agent.prevReportedSite.estimatedAgentCount -= 1
            if agent.assignedSite is not None:
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
        if not Config.ONLY_RECORD_LAST:
            self.recorder.write()

    def sendResults(self, results):
        """ Tells the rest API which site the agents ended up at and how long it took them to get there,
         and records result information in a .json file"""
        if Config.USE_REST_API:
            self.world.request.sendResultsToAPI(results)
        if Config.SHOULD_RECORD:
            self.recorder.writeResults(results, self.world)
