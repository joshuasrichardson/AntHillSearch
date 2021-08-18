""" Colony Simulation Environment """
import datetime
import threading
from abc import ABC

from ColonyExceptions import *
from Constants import *
from display import Display
from interface.Simulation import Simulation
from model.World import World
from model.builder import AgentBuilder
from net.SendHubInfoRequest import SendHubInfoRequest


class LiveSimulation(Simulation, ABC):
    """ A class to run the interface for ants finding their new home after the old one broke """

    def __init__(self, simulationDuration=SIM_DURATION, numHubs=NUM_HUBS, numSites=NUM_SITES, useRestAPI=USE_REST_API,
                 shouldRecord=SHOULD_RECORD, convergenceFraction=CONVERGENCE_FRACTION,
                 hubLocations=HUB_LOCATIONS, hubRadii=HUB_RADII, hubAgentCounts=HUB_AGENT_COUNTS,
                 sitePositions=SITE_POSITIONS, siteQualities=SITE_QUALITIES, siteRadii=SITE_RADII,
                 siteNoCloserThan=SITE_NO_CLOSER_THAN, siteNoFartherThan=SITE_NO_FARTHER_THAN,
                 hubCanMove=HUB_CAN_MOVE, homogenousAgents=HOMOGENOUS_AGENTS, minSpeed=MIN_AGENT_SPEED,
                 maxSpeed=MAX_AGENT_SPEED, minDecisiveness=MIN_DECISIVENESS, maxDecisiveness=MAX_DECISIVENESS,
                 minNavSkills=MIN_NAV_SKILLS, maxNavSkills=MAX_NAV_SKILLS, minEstAccuracy=MIN_QUALITY_MISJUDGMENT,
                 maxEstAccuracy=MAX_QUALITY_MISJUDGMENT, maxSearchDist=MAX_SEARCH_DIST,
                 findSitesEasily=FIND_SITES_EASILY, commitSpeedFactor=COMMIT_SPEED_FACTOR):
        super().__init__(simulationDuration, numHubs, numSites, shouldRecord, convergenceFraction,
                         hubLocations, hubRadii, hubAgentCounts, sitePositions, siteQualities, siteRadii,
                         siteNoCloserThan, siteNoFartherThan, hubCanMove, homogenousAgents, minSpeed,
                         maxSpeed, minDecisiveness, maxDecisiveness, minNavSkills, maxNavSkills, minEstAccuracy,
                         maxEstAccuracy, maxSearchDist, findSitesEasily, commitSpeedFactor)
        self.previousSendTime = datetime.datetime.now()
        self.useRestAPI = useRestAPI

        if simulationDuration < 0 or simulationDuration > MAX_TIME:
            raise InputError("Simulation too short or too long", simulationDuration)
        if numSites < 0 or numSites > MAX_NUM_SITES:
            raise InputError("Can't be more sites than maximum value", numSites)

    def initializeWorld(self, numHubs, numSites, hubLocations, hubRadii, hubAgentCounts, sitePositions,
                        siteQualities, siteRadii):
        world = World(numHubs, numSites, hubLocations, hubRadii, hubAgentCounts, sitePositions,
                      siteQualities, siteRadii)
        world.initSitesAgentsCounts()
        if not SHOULD_DRAW_FOG:
            world.fog = []
        return world

    def initializeRequest(self):
        self.world.request = SendHubInfoRequest(self.world.agentList)

    def randomizeInitialState(self):
        self.world.randomizeState()

    def addAgents(self, numAgents, state, phase, assignedSiteIndex, startingPosition=None):
        if startingPosition is None:
            startingPosition = self.world.siteList[assignedSiteIndex].getPosition()
        for i in range(0, numAgents):
            agent = AgentBuilder.getNewAgent(self.world, self.world.siteList[assignedSiteIndex], startingPosition)
            agent.assignedSite.agentCount += 1
            agent.setState(state(agent))
            agent.setPhase(phase)
            self.world.addAgent(agent)

    def updateSites(self):
        if self.shouldRecord:
            for site in self.world.siteList:
                self.recorder.recordSiteInfo(site)

    def updateAgent(self, agent, agentRectList):
        agent.updatePosition()
        if Display.shouldDraw:
            agent.clearFog()

        agentRect = agent.getAgentRect()
        possibleNeighborList = agentRect.collidelistall(agentRectList)
        agentNeighbors = []
        for i in possibleNeighborList:
            agentNeighbors.append(self.world.agentList[i])
        agent.changeState(agentNeighbors)

        if self.shouldRecord:
            self.recorder.recordAgentInfo(agent)

    def report(self, agentRectList):
        self.setSitesEstimates(agentRectList)
        if self.useRestAPI:
            self.updateRestAPI()

    def setSitesEstimates(self, agentRectList):
        hubRects = self.world.getHubsRects()
        self.world.request.numAtHub = 0
        for hubRect in hubRects:
            hubAgentsIndices = hubRect.collidelistall(agentRectList)
            for agentIndex in hubAgentsIndices:
                agent = self.world.agentList[agentIndex]
                sites = agent.knownSites
                for siteIndex in range(0, len(sites)):
                    if agent.knownSitesPositions[siteIndex] == sites[siteIndex].getPosition():
                        sites[siteIndex].wasFound = True
                        # If the site's estimates were not reported before the agent got assigned to another site, report them here.
                        if sites[siteIndex].estimatedPosition is None and sites[siteIndex].getQuality() != -1:
                            sites[siteIndex].setEstimates([agent.estimateSitePosition(sites[siteIndex]),
                                                           agent.estimateQuality(sites[siteIndex]),
                                                           agent.estimateAgentCount(sites[siteIndex]),
                                                           agent.estimateRadius(sites[siteIndex])])
                agent.assignedSite.setEstimates(self.world.request.addAgentToSendRequest(agent, agentIndex))
                agent.assignedSite.updateBlur()

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

    def sendResults(self, chosenSites, simulationTime):
        """ Tells the rest API which site the agents ended up at and how long it took them to get there """
        if self.useRestAPI:
            positions = []
            qualities = []
            for site in chosenSites:
                positions.append(site.getPosition())
                qualities.append(site.getQuality())
            self.world.request.sendResults(positions, qualities, simulationTime)
