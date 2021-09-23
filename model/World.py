""" World class. Stores 2D positions of hub and sites """
import random

import numpy as np
from pygame import Rect

import ColonyExceptions
from Constants import *
from display import Display
from model.builder import SiteBuilder


class World:
    """ Represents the world around the ants old home """

    def __init__(self, numHubs, numSites, hubLocations, hubRadii, hubAgentCounts, sitePositions, siteQualities, siteRadii, siteRadius=SITE_RADIUS):
        self.hubLocations = hubLocations  # Where the agents' original homes are located
        self.hubRadii = hubRadii  # The radii of the agent's original homes
        self.initialHubAgentCounts = hubAgentCounts  # The number of agents at the hubs at the start of the simulation
        self.checkHubs(numHubs, siteRadius)
        self.siteList = []  # The sites in the world
        self.siteRectList = []  # List of site rectangles
        self.sitePositions = sitePositions  # Where the sites are located
        self.siteQualities = siteQualities  # The quality of each site
        self.sitesRadii = siteRadii  # A list of the radius of each site

        self.hubsRects = []
        self.hubsObserveRects = []
        self.hubs = self.createHubs(numHubs, self.hubLocations, self.hubRadii, self.initialHubAgentCounts)  # The agents' original home
        self.createSites(numSites, numHubs, siteRadius)  # Initializes the site list with sites that match the specified values or random sites by default
        self.normalizeQuality()  # Set the site qualities so that the best is bright green and the worst bright red
        self.agentList = []  # List of all the agents in the world
        self.paths = []  # List of all the positions the agents have been to recently
        self.agentGroups = [[], [], [], [], [], [], [], [], [], []]  # Groups of agents that are selected together and assigned a number 0 - 9.
        self.request = None  # The request, used to sent information to a rest API
        self.agentsToDeleteIndexes = []

        self.states = np.zeros((NUM_POSSIBLE_STATES,))  # List of the number of agents assigned to each state
        self.phases = np.zeros((NUM_POSSIBLE_PHASES,))  # List of the number of agents assigned to each phase

    def checkHubs(self, numHubs, siteRadius):
        """ Ensure that hubs have all necessary attributes. If they aren't preassigned, assign them randomly. """
        if len(self.hubLocations) == 0 and numHubs == 1:
            self.hubLocations.append([650, 325])
        while len(self.hubLocations) < numHubs:
            nextPos = [random.randint(HUB_MIN_X, HUB_MAX_X), random.randint(HUB_MIN_Y, HUB_MAX_Y)]
            tries = 0
            while self.tooCloseToOtherHubs(nextPos):
                nextPos = [random.randint(HUB_MIN_X, HUB_MAX_X), random.randint(HUB_MIN_Y, HUB_MAX_Y)]
                tries += 1
                if tries > 200:
                    raise ColonyExceptions.InputError("The hub boundaries are too small for the search distance. "
                                                      "Either Increase the difference between (HUB_MAX_X and HUB_MIN_X) "
                                                      "and (HUB_MAX_Y and HUB_MIN_Y) or decrease the MAX_SEARCH_DIST. "
                                                      "[HUB_MAX_X, HUB_MIN_X, HUB_MAX_Y, HUB_MIN_Y, MAX_SEARCH_DIST]: ",
                                                      [HUB_MAX_X, HUB_MIN_X, HUB_MAX_Y, HUB_MIN_Y, MAX_SEARCH_DIST])
            self.hubLocations.append(nextPos)
        while len(self.hubRadii) < numHubs:
            self.hubRadii.append(siteRadius)
        while len(self.initialHubAgentCounts) < numHubs:
            self.initialHubAgentCounts.append(random.randint(1, 50))

    def tooCloseToOtherHubs(self, nextPos):
        for pos in self.hubLocations:
            if abs(pos[0] - nextPos[0]) < MAX_SEARCH_DIST * 1.5 and \
                    abs(pos[1] - nextPos[1]) < MAX_SEARCH_DIST * 1.5:
                return True
        return False

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

    def createSites(self, numSites, numHubs, siteRadius):
        """ Create as many sites as required """
        for siteIndex in range(numSites):
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
                radius = siteRadius
            self.createSite(x, y, radius, quality, numHubs)

    def createSite(self, x, y, radius, quality, numHubs):
        """ Creates a site with specified values. If values are none, then default values will apply """
        newSite = SiteBuilder.getNewSite(numHubs, x, y, radius, quality, self.hubLocations)
        self.siteList.append(newSite)  # Add the site to the world's list of sites
        self.siteRectList.append(newSite.getSiteRect())

    def removeSite(self, site):
        """ Deletes the site unless it is the hub """
        if site.getQuality() == -1:
            print("Cannot delete the hub")
        else:
            index = self.siteList.index(site, 0, len(self.siteList))
            self.siteList.pop(index)
            self.siteRectList.pop(index)
            del site

    def addAgent(self, agent):
        self.agentList.append(agent)
        self.initialHubAgentCounts[agent.getHubIndex()] = self.initialHubAgentCounts[agent.getHubIndex()] + 1
        if self.request is not None:
            self.request.addAgent(agent)

    def deleteSelectedAgents(self):
        originalIndex = 0
        i = 0
        while i < len(self.agentList):
            agent = self.agentList[i]
            if agent.isSelected:
                self.removeAgent(agent)
                self.agentsToDeleteIndexes.append(originalIndex)
                if self.request is not None:
                    self.request.removeAgent(i)
            else:
                i += 1
            originalIndex += 1

    def removeAgent(self, agent):
        agent.assignedSite.decrementCount(agent.getHubIndex())
        self.agentList.remove(agent)
        for group in self.agentGroups:
            try:
                group.remove(agent)
            except ValueError:
                pass
        self.initialHubAgentCounts[agent.getHubIndex()] -= 1
        del agent

    def getDeletedAgentsIndexes(self):
        indexes = self.agentsToDeleteIndexes
        self.agentsToDeleteIndexes = []
        return indexes

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

    def createHubs(self, numHubs, locations, radii, agentCounts):
        hubs = []
        for i in range(numHubs):
            pos = locations[i]
            rad = radii[i]
            hubSite = SiteBuilder.getNewSite(numHubs, pos[0], pos[1], rad, -1)
            count = agentCounts[i]
            hubSite.agentCount = count
            hubSite.setEstimates([pos, -1, count, rad])
            hubSite.blurAmount = 1
            hubSite.blurRadiusDiff = 0
            self.siteList.append(hubSite)
            self.siteRectList.append(hubSite.getSiteRect())
            hubs.append(hubSite)
        for hub in hubs:
            hubRect = hub.getSiteRect()
            self.hubsRects.append(hubRect)
            self.hubsObserveRects.append(Rect(hubRect.left - HUB_OBSERVE_DIST, hubRect.top - HUB_OBSERVE_DIST,
                                         hubRect.width + 2 * HUB_OBSERVE_DIST, hubRect.height + 2 * HUB_OBSERVE_DIST))
        return hubs

    def getHubs(self):
        return self.hubs

    def getHubsRects(self):
        return self.hubsRects

    def getHubsObserveRects(self):
        return self.hubsObserveRects

    def updateStateAndPhaseCounts(self):
        """ Counts the phase and state of each agent so they can be displayed to the user """
        self.states = np.zeros((NUM_POSSIBLE_STATES,))
        self.phases = np.zeros((NUM_POSSIBLE_PHASES,))
        if Display.drawFarAgents:
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
            self.states[CONVERGED] = self.request.numConverged

            self.phases[EXPLORE] = self.request.numExplore
            self.phases[ASSESS] = self.request.numAssess
            self.phases[CANVAS] = self.request.numCanvas
            self.phases[COMMIT] = self.request.numCommit

    def updatePaths(self, agent):
        if Display.shouldDrawPaths and Display.drawFarAgents:  # If the paths should be drawn anywhere, the world can keep track of all of them
            self.paths.append(agent.getPosition())
            if len(self.paths) > 50 * len(self.agentList):
                for i in range(len(self.agentList)):
                    self.paths.pop(0)
        else:  # The agents will need to keep track of their paths so they can report it when they get to the hub an no other time.
            agent.updatePath()

    def updateGroup(self, index, agents):
        """ Sets an easily selectable group of agents to the specified agents """
        self.agentGroups[index] = agents

    def getGroup(self, index):
        """ Gets the group of agents that was set to the specified index """
        return self.agentGroups[index]

    def getClosestHub(self, pos):
        minDist = 100000
        closestHub = None
        for hub in self.hubs:
            hubDist = np.sqrt(np.square(pos[0] - hub.getPosition()[0]) + np.square(pos[1] - hub.getPosition()[1]))
            if hubDist < minDist:
                minDist = hubDist
                closestHub = hub
        return closestHub

    def getClosestAgentWithState(self, pos, stateNums):
        minDist = 100000
        closestAgent = None
        for agent in self.agentList:
            if stateNums.__contains__(agent.getState()):
                dist = np.sqrt(np.square(pos[0] - agent.getPosition()[0]) + np.square(pos[1] - agent.getPosition()[1]))
                if dist < minDist:
                    minDist = dist
                    closestAgent = agent
        return closestAgent
