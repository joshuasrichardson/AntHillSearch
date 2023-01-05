from numpy import random, zeros, pi, cos, sin, inf
import time

import Utils
from config import Config
from Constants import *
from display import Display
from display.simulation import FogDisplay
from model.FloodZone import FloodZone
from model.Predator import Predator
from model.Ladybug import Ladybug
from model.Obstacle import Obstacle
from model.builder import SiteBuilder


class World:
    """ Represents the world around the ants old home """

    def __init__(self, numHubs, numSites, hubLocations, hubRadii, hubAgentCounts, sitePositions, siteQualities,
                 siteRadii, siteRadius=Config.SITE_RADIUS, numPredators=Config.NUM_PREDATORS,
                 predPositions=Config.PRED_POSITIONS,
                 numLadybugs=Config.NUM_LADYBUGS, ladybugPositions=Config.LADYBUG_POSITIONS,
                 numObstacles=Config.NUM_OBSTACLES, obstaclePositions=Config.OBSTACLE_POSITIONS):
        """ numHubs - the number of original homes of ant colonies
        numSites - the number of sites in the simulation, not including hubs
        hubLocations - x, y coordinates of the center of each hub
        hubRadii - a list of the radii for each hub
        hubAgentCounts - the number of agents initially at each hub
        sitePositions - the x, y coordinates for each site, not including hubs
        siteQualities - the quality from 0 to 255 for each site, not including hubs
        siteRadii - a list of the radii for each site, not including hubs
        numPredators - the number of predators in the world
        predPositions - the initial position of each predator
        numLadybugs - the number of ladybugs in the world
        ladybugPositions - the initial position of each ladybug
        numObstacles - the number of obstacles in the world
        obstaclePositions - the initial position of each obstacle """
        self.hubLocations = hubLocations  # Where the agents' original homes are located
        self.hubRadii = hubRadii  # The radii of the agent's original homes
        self.initialHubAgentCounts = hubAgentCounts  # The number of agents at the hubs at the start of the simulation
        self.siteList = []  # The sites in the world
        self.siteRectList = []  # List of site rectangles
        self.sitePositions = sitePositions  # Where the sites are located
        self.siteQualities = siteQualities  # The quality of each site
        self.sitesRadii = siteRadii  # A list of the radius of each site
        self.checkHubs(numHubs, siteRadius)

        self.hubsRects = []
        self.hubs = self.createHubs(numHubs)  # The agents' original homes
        self.createSites(numSites, numHubs,
                         siteRadius)  # Initializes the site list with sites that match the specified values or random sites by default
        self.normalizeQuality()  # Set the site qualities so that the best is bright green and the worst bright red
        self.agentList = []  # List of all the agents in the world
        self.numDeadAgents = [0 for _ in range(numHubs)]  # The number of agents that have died during the simulation
        self.predatorList = self.generatePredators(numPredators,
                                                   predPositions)  # List of all the predators in the world
        self.ladybugList = self.generateLadybugs(numLadybugs, ladybugPositions)  # List of all the ladybugs in the world
        self.obstacleList = self.generateObstacles(numObstacles, obstaclePositions)  # List of all the obstacles in the world
        self.paths = []  # List of all the positions the agents have been to recently
        self.agentGroups = [[], [], [], [], [], [], [], [], [],
                            []]  # Groups of agents that are selected together and assigned a number 0 - 9.
        self.request = None  # The request, used to sent information to a rest API
        self.agentsToDeleteIndexes = []
        self.dangerZones = []
        self.dangerZonesVisibilities = []

        self.states = zeros((NUM_POSSIBLE_STATES,))  # List of the number of agents assigned to each state
        self.phases = zeros((NUM_POSSIBLE_PHASES,))  # List of the number of agents assigned to each phase

        self.floodZone = FloodZone()
        if Config.SHOULD_DRAW:
            self.fog = FogDisplay.initFog(self.hubs)

    def getNumSites(self):
        return len(self.siteList) - len(self.hubs)

    def getNumAgents(self):
        return len(self.agentList)

    def checkHubs(self, numHubs, siteRadius):
        """ Ensure that hubs have all necessary attributes. If they aren't preassigned, assign them randomly. """
        if len(self.hubLocations) == 0 and numHubs == 1:
            self.hubLocations.append([Display.origWidth / 2, Display.origHeight / 2])
        while len(self.hubRadii) < numHubs:
            self.hubRadii.append(siteRadius)
        t1 = time.time()
        while len(self.hubLocations) < numHubs:
            nextPos = self.generateNextPos()
            while self.tooCloseToEdge(nextPos) or self.tooCloseToOtherHubs(nextPos):
                # Make sure the hubs are not too close together
                nextPos = self.generateNextPos()
                if time.time() - t1 > 0.7:
                    nextPos = [random.randint(Config.HUB_MIN_X, Config.HUB_MAX_X),
                               random.randint(Config.HUB_MIN_Y, Config.HUB_MAX_Y)]
                    break
            self.hubLocations.append(nextPos)
        while len(self.initialHubAgentCounts) < numHubs:
            self.initialHubAgentCounts.append(random.randint(1, 50))

    def generateNextPos(self):
        if len(self.hubLocations) == 0:
            return [random.randint(Config.HUB_MIN_X, Config.HUB_MAX_X),
                    random.randint(Config.HUB_MIN_Y, Config.HUB_MAX_Y)]
        neighborHubLocation = self.hubLocations[random.randint(0, len(self.hubLocations))]
        dist = Config.MAX_SEARCH_DIST * random.uniform(1.25, 1.75)
        angle = random.uniform(0, 2 * pi)
        x = int(cos(angle) * dist + neighborHubLocation[0])
        y = int(sin(angle) * dist + neighborHubLocation[1])
        return [x, y]

    @staticmethod
    def tooCloseToEdge(nextPos):
        return nextPos[0] < Config.HUB_MIN_X or nextPos[0] > Config.HUB_MAX_X or nextPos[1] < Config.HUB_MIN_Y or \
               nextPos[1] > Config.HUB_MAX_Y

    def tooCloseToOtherHubs(self, nextPos):
        """ If another hub is too close, return True. """
        for i, pos in enumerate(self.hubLocations):
            if Utils.isClose(pos, nextPos, Config.MAX_SEARCH_DIST + 2 * self.hubRadii[i]):
                return True
        return False

    def randomizeState(self):
        """ Sets all the agents at random sites """
        for agent in self.agentList:
            site = self.siteList[random.randint(0, len(self.siteList) - 1)]
            agent.addToKnownSites(site)
            agent.assignSite(site)
            pos = agent.assignedSite.getPosition()
            agent.setPosition(pos[0], pos[1])

    def generatePredators(self, numPredators, predPositions):
        return self.generateBugs(Predator, numPredators, predPositions)

    def generateLadybugs(self, numLadybugs, ladybugPositions):
        return self.generateBugs(Ladybug, numLadybugs, ladybugPositions)

    def generateBugs(self, bug, numBugs, bugPositions):
        bugs = []

        if numBugs > len(bugPositions):
            for i in range(len(bugPositions)):  # Create all the bugs with preset positions
                bugs.append(bug(self.siteList[random.randint(len(self.hubs), len(self.siteList))], self, bugPositions[i]))

            for i in range(len(bugPositions), numBugs):  # Create all the bugs without preset positions
                bugs.append(bug(self.siteList[random.randint(len(self.hubs), len(self.siteList))], self))
        else:
            for i in range(numBugs):  # Create all the bugs with preset positions
                bugs.append(bug(self.siteList[random.randint(len(self.hubs), len(self.siteList))], self, bugPositions[i]))

        return bugs

    def generateObstacles(self, numObstacles, obstaclePositions):
        obstacles = []

        if numObstacles > len(obstaclePositions):
            for i in range(len(obstaclePositions)):  # Create all the obstacles with preset positions
                obstacles.append(Obstacle(self, obstaclePositions[i]))
            for i in range(len(obstaclePositions), numObstacles):  # Create all the obstacles without preset positions
                obstacles.append(Obstacle(self))
        else:
            for i in range(numObstacles):  # Create all the obstacles with preset positions
                obstacles.append(Obstacle(self, obstaclePositions[i]))
        return obstacles

    def getSiteList(self):
        return self.siteList

    def getSiteIndex(self, site):
        """ Returns the position of the site in the world's site list """
        try:
            return self.siteList.index(site)
        except ValueError:
            return None

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
        if site.isHub():
            print("Cannot delete the hub")
            site.unselect()
        else:
            index = self.siteList.index(site, 0, len(self.siteList))
            self.siteList.pop(index)
            self.siteRectList.pop(index)
            del site

    def addAgent(self, agent):
        self.agentList.append(agent)
        self.initialHubAgentCounts[agent.getHubIndex()] += 1
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
        minValue = inf
        maxValue = -inf
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

    def centerHubs(self, hubs):
        if len(hubs) > 1 and Config.SHOULD_DRAW:
            leftMostPos = inf
            rightMostPos = -inf
            upMostPos = inf
            downMostPos = -inf
            for site in self.siteList:
                leftMostPos = site.pos[0] if site.pos[0] < leftMostPos else leftMostPos
                rightMostPos = site.pos[0] if site.pos[0] > rightMostPos else rightMostPos
                upMostPos = site.pos[1] if site.pos[1] < upMostPos else upMostPos
                downMostPos = site.pos[1] if site.pos[1] > downMostPos else downMostPos
            midX = (rightMostPos + leftMostPos) / 2
            midY = (downMostPos + upMostPos) / 2
            displacementX = midX - Display.origWidth / 2
            displacementY = midY - Display.origHeight / 2
            for i, site in enumerate(self.siteList):
                site.setPosition([site.pos[0] - displacementX, site.pos[1] - displacementY])
                self.siteRectList[i] = site.getSiteRect()
                self.hubsRects[i] = site.getSiteRect()
                self.hubLocations[i][0] -= displacementX
                self.hubLocations[i][1] -= displacementY

    def createHubs(self, numHubs):
        hubs = []
        for i in range(numHubs):
            pos = self.hubLocations[i]
            rad = self.hubRadii[i]
            hubSite = SiteBuilder.getNewSite(numHubs, pos[0], pos[1], rad, -1)
            count = self.initialHubAgentCounts[i]
            hubSite.agentCount = count
            hubSite.setEstimates(pos, -1, count, rad)
            hubSite.blurAmount = 1
            hubSite.blurRadiusDiff = 0
            self.siteList.append(hubSite)
            self.siteRectList.append(hubSite.getSiteRect())
            self.hubsRects.append(hubSite.getSiteRect())
            hubs.append(hubSite)
        self.centerHubs(hubs)

        return hubs

    def getHubs(self):
        return self.hubs

    def getHubsRects(self):
        return self.hubsRects

    def updateStateAndPhaseCounts(self):
        """ Counts the phase and state of each agent so they can be displayed to the user """
        if Config.DRAW_FAR_AGENTS:
            for i in range(NUM_POSSIBLE_STATES):
                self.states[i] = 0
            for i in range(NUM_POSSIBLE_PHASES):
                self.phases[i] = 0
            for agent in self.agentList:
                st = agent.getStateNumber()
                self.states[st] += 1
                ph = agent.getPhaseNumber()
                self.phases[ph] += 1

    def updatePaths(self, agent):
        if Config.SHOULD_DRAW_PATHS and Config.DRAW_FAR_AGENTS:  # If the paths should be drawn anywhere, the world can keep track of all of them
            self.paths.append(agent.getPosition())
            if len(self.paths) > 50 * len(self.agentList):
                for i in range(len(self.agentList)):
                    self.paths.pop(0)
        elif Config.SHOULD_DRAW_PATHS:  # The agents will need to keep track of their paths so they can report it when they get to the hub an no other time.
            agent.updatePath()

    def updateGroup(self, index, agents):
        """ Sets an easily selectable group of agents to the specified agents """
        self.agentGroups[index] = agents

    def getGroup(self, index):
        """ Gets the group of agents that was set to the specified index """
        return self.agentGroups[index]

    def getClosestHub(self, pos):
        minDist = inf
        closestHub = None
        for hub in self.hubs:
            hubDist = Utils.getDistance(pos, hub.getPosition())
            if hubDist < minDist:
                minDist = hubDist
                closestHub = hub
        return closestHub

    def getClosestAgentWithState(self, pos, stateNums):
        minDist = inf
        closestAgent = None
        for agent in self.agentList:
            if stateNums.__contains__(agent.getStateNumber()):
                dist = Utils.getDistance(pos, agent.getPosition())
                if dist < minDist:
                    minDist = dist
                    closestAgent = agent
        return closestAgent

    def incrementDeadAgents(self, hubIndex):
        self.numDeadAgents[hubIndex] += 1

    def addDangerZone(self, pos):
        dzPos = self.getNearbyDangerZone(pos)
        if dzPos is None:
            self.dangerZones.append(pos)
            self.dangerZonesVisibilities.append(255)
        else:
            i = self.dangerZones.index(dzPos)
            self.dangerZonesVisibilities[i] = 255

    def getNearbyDangerZone(self, newZonePos):
        for pos in self.dangerZones:
            if self.isClose(newZonePos, pos, Config.MIN_AVOID_DIST):
                return pos
        return None

    def updateDangerZones(self):
        for i in reversed(range(len(self.dangerZones))):
            self.dangerZonesVisibilities[i] -= 0.5
            if self.dangerZonesVisibilities[i] == 0:
                self.dangerZonesVisibilities.pop(i)
                self.dangerZones.pop(i)

    @staticmethod
    def isClose(newZonePos, position, distance):
        """ Returns a boolean representing whether the new position is within the specified distance of the specified position """
        return Utils.isClose(newZonePos, position, distance)
