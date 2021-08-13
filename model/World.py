""" World class. Stores 2D positions of hub and sites """
import random

import numpy as np
from pygame import Rect

from Constants import *
from display import AgentDisplay, Display
from model.Site import Site


class World:
    """ Represents the world around the ants old home """

    def __init__(self, numSites, hubLocation, hubRadius, hubAgentCount, sitePositions, siteQualities, siteRadii,
                 siteNoCloserThan, siteNoFartherThan, drawEstimates=DRAW_ESTIMATES,
                 hubCanMove=HUB_CAN_MOVE):
        self.hubCanMove = hubCanMove  # Whether the hub can be moved by the user
        self.hubLocation = hubLocation  # Where the agents' original home is located
        if hubLocation is None:
            if Display.shouldDraw:
                x, y = Display.screen.get_size()
            else:
                x, y = 1300, 800
            self.hubLocation = [x / 2, y / 2]
        self.hubRadius = hubRadius  # The radius of the agent's original home
        self.siteNoCloserThan = siteNoCloserThan  # The closest to the hub a site can randomly be generated
        self.siteNoFartherThan = siteNoFartherThan  # The furthest to the hub a site can randomly be generated
        self.initialHubAgentCount = hubAgentCount  # The number of agents at the start of the interface
        self.siteList = []  # The sites in the world
        self.siteRectList = []  # List of site rectangles
        self.sitePositions = sitePositions  # Where the sites are located
        self.siteQualities = siteQualities  # The quality of each site
        self.sitesRadii = siteRadii  # A list of the radius of each site
        self.drawEstimates = drawEstimates  # Whether estimates are drawn (if False, actual values are drawn)
        self.shouldDrawFog = True  # Whether the screen is initially filled with dark gray fog
        self.marker = None  # A marker drawn in the world representing a user's command

        self.createSites(numSites)  # Initializes the site list with sites that match the specified values or random sites by default
        self.normalizeQuality()  # Set the site qualities so that the best is bright green and the worst bright red
        self.agentList = []  # List of all the agents in the world
        self.paths = []  # List of all the positions the agents have been to recently
        self.agentGroups = [[], [], [], [], [], [], [], [], [], []]  # Groups of agents that are selected together and assigned a number 0 - 9.
        self.hub = self.createHub()  # The agents' original home
        if Display.shouldDraw:
            self.fog = self.getInitialFog()  # A list of rectangles where the agents have not yet explored
        self.request = None  # The request, used to sent information to a rest API

        self.states = np.zeros((NUM_POSSIBLE_STATES,))  # List of the number of agents assigned to each state
        self.phases = np.zeros((NUM_POSSIBLE_PHASES,))  # List of the number of agents assigned to each phase

    def randomizeState(self):
        """ Sets all the agents at random sites """
        for agent in self.agentList:
            site = self.siteList[random.randint(0, len(self.siteList) - 1)]
            agent.addToKnownSites(site)
            agent.assignSite(site)
            agent.setPosition(agent.assignedSite.getPosition()[0], agent.assignedSite.getPosition()[1])

    def getSiteList(self):
        return self.siteList

    def getSiteIndex(self, site):
        """ Returns the position of the site in the world's site list """
        return self.siteList.index(site)

    def setSitePosition(self, site, pos):
        siteIndex = self.siteList.index(site)
        self.siteList[siteIndex].setPosition(pos)
        self.siteRectList[siteIndex].centerx = pos[0]
        self.siteRectList[siteIndex].centery = pos[1]

    def createSites(self, numSites):
        """ Create as many sites as required """
        for siteIndex in range(0, numSites):
            try:  # Try setting the position to match the position in the specified positions list
                x = self.sitePositions[siteIndex][0]
                y = self.sitePositions[siteIndex][1]
            except IndexError:  # If the positions are not specified they will be randomized
                x = None
                y = None
            try:  # Try setting the quality to match the quality in the specified qualities list
                quality = self.siteQualities[siteIndex]
            except IndexError:  # If the qualities are not specified they will be randomized
                quality = None
            try:  # Try setting the radius to match the radius in the specified radii list
                radius = self.sitesRadii[siteIndex]
            except IndexError:  # If the radii are not specified they will be randomized
                radius = SITE_RADIUS
            self.createSite(x, y, radius, quality)

    def createSite(self, x, y, radius, quality):
        """ Creates a site with specified values. If values are none, then default values will apply """
        newSite = Site(self.hubLocation, x, y, radius, quality,
                       self.siteNoCloserThan, self.siteNoFartherThan)
        self.siteList.append(newSite)  # Add the site to the world's list of sites
        self.siteRectList.append(newSite.getSiteRect())

    def removeSite(self, site):
        """ Deletes the site unless it is the hub """
        if site.getQuality() == -1 and site.agentCount > 0:
            print("Cannot delete the hub")
        else:
            index = self.siteList.index(site, 0, len(self.siteList))
            self.siteList.pop(index)
            self.siteRectList.pop(index)
            del site

    def getInitialFog(self):
        """ Gets a list of rectangles that cover the entire screen except for the area around the hub """
        rects = []
        w = Display.screen.get_width()
        h = Display.screen.get_height()
        for i in range(NUM_FOG_BLOCKS_X):
            for j in range(NUM_FOG_BLOCKS_Y):
                pos = [int((w / NUM_FOG_BLOCKS_X) * i), int((h / NUM_FOG_BLOCKS_Y) * j)]
                rect = Rect(int(w * i / NUM_FOG_BLOCKS_X),
                            int(h * j / NUM_FOG_BLOCKS_Y),
                            int(w / NUM_FOG_BLOCKS_X + 1),
                            int(h / NUM_FOG_BLOCKS_Y + 1))
                if not self.isClose(self.hub.getSiteRect(), pos):
                    rects.append(rect)
        return rects

    @staticmethod
    def isClose(rect, pos):
        """ Returns whether the position and rectangle are close to each other """
        return rect.colliderect(pos[0] - (rect.width + HUB_OBSERVE_DIST) / 2,
                                pos[1] - (rect.height + HUB_OBSERVE_DIST) / 2,
                                (Display.screen.get_width() / NUM_FOG_BLOCKS_X) + rect.width + HUB_OBSERVE_DIST,
                                (Display.screen.get_height() / NUM_FOG_BLOCKS_Y) + rect.height + HUB_OBSERVE_DIST)

    def addAgent(self, agent):
        self.agentList.append(agent)
        if self.request is not None:
            self.request.addAgent(agent)

    def deleteSelectedAgents(self):
        i = 0
        while i < len(self.agentList):
            agent = self.agentList[i]
            if agent.isSelected:
                self.removeAgent(agent)
                if self.request is not None:
                    self.request.removeAgent(i)
            else:
                i += 1

    def removeAgent(self, agent):
        agent.assignedSite.decrementCount()
        self.agentList.remove(agent)

    def normalizeQuality(self):
        """ Set the site qualities so that the best is bright green and the worst bright red """
        # Normalize quality to be between lower bound and upper bound
        minValue = np.inf
        maxValue = -np.inf
        for siteIndex in range(0, len(self.siteList)):
            quality = self.siteList[siteIndex].getQuality()
            if quality < minValue:
                minValue = quality
            if quality > maxValue:
                maxValue = quality
        zero = minValue
        span = maxValue - minValue
        for siteIndex in range(0, len(self.siteList)):
            self.siteList[siteIndex].normalizeQuality(span, zero, self.siteQualities)

    def createHub(self):
        hubSite = Site(self.hubLocation, self.hubLocation[0], self.hubLocation[1], self.hubRadius, -1,
                       self.siteNoCloserThan, self.siteNoFartherThan)
        hubSite.agentCount = self.initialHubAgentCount
        hubSite.setEstimates([self.hubLocation, -1, hubSite.agentCount, hubSite.radius])
        hubSite.blurAmount = 1
        hubSite.blurRadiusDiff = 0
        self.siteList.append(hubSite)
        self.siteRectList.append(hubSite.getSiteRect())
        return hubSite

    def getHub(self):
        return self.hub

    def updateStateAndPhaseCounts(self):
        """ Counts the phase and state of each agent so they can be displayed to the user """
        self.states = np.zeros((NUM_POSSIBLE_STATES,))
        self.phases = np.zeros((NUM_POSSIBLE_PHASES,))
        if DRAW_FAR_AGENTS:
            for agent in self.agentList:
                st = agent.getState()
                self.states[st] += 1
                ph = agent.getPhaseNumber()
                self.phases[ph] += 1
        else:
            self.states[AT_NEST] = self.request.numAtHub
            self.states[SEARCH] = self.request.numSearch
            self.states[CARRIED] = self.request.numCarried
            self.states[FOLLOW] = self.request.numFollow
            self.states[LEAD_FORWARD] = self.request.numLeadForward
            self.states[REVERSE_TANDEM] = self.request.numReverseTandem
            self.states[TRANSPORT] = self.request.numTransport
            self.states[GO] = self.request.numGo

            self.phases[EXPLORE] = self.request.numExplore
            self.phases[ASSESS] = self.request.numAssess
            self.phases[CANVAS] = self.request.numCanvas
            self.phases[COMMIT] = self.request.numCommit

        if self.states[GO] == 0:  # If all the agents have reached the destination they were commanded to go to,
            self.setMarker(None)  # then the marker should go away.

    def updatePaths(self, agent):
        if Display.shouldDrawPaths and AgentDisplay.drawFarAgents:  # If the paths should be drawn anywhere, the world can keep track of all of them
            self.paths.append(agent.getPosition())
            if len(self.paths) > 50 * len(self.agentList):
                for i in range(len(self.agentList)):
                    self.paths.pop(0)
        else:  # The agents will need to keep track of their paths so they can report it when they get to the hub an no other time.
            agent.updatePath()

    def setMarker(self, marker):
        self.marker = marker

    def eraseFog(self, rect):
        fogIndices = rect.collidelist(self.fog)
        while fogIndices != -1:
            self.fog.pop(fogIndices)
            fogIndices = rect.collidelist(self.fog)

    def updateGroup(self, index, agents):
        """ Sets an easily selectable group of agents to the specified agents """
        self.agentGroups[index] = agents

    def getGroup(self, index):
        """ Gets the group of agents that was set to the specified index """
        return self.agentGroups[index]
