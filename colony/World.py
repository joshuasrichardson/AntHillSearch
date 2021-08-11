""" World class. Stores 2D positions of hub and sites """
import random

from colony.Site import *


class World:
    """ Represents the world around the ants old home """

    def __init__(self, numSites, screen, hubLocation, hubRadius, hubAgentCount, sitePositions, siteQualities, siteRadii,
                 siteNoCloserThan, siteNoFartherThan, shouldDraw, knowSitePosAtStart, drawEstimates=DRAW_ESTIMATES,
                 hubCanMove=HUB_CAN_MOVE, shouldDrawPaths=SHOULD_DRAW_PATHS):
        self.shouldDraw = shouldDraw  # Whether the simulation should be drawn on the screen
        self.hubCanMove = hubCanMove  # Whether the hub can be moved by the user
        self.hubLocation = hubLocation  # Where the agents' original home is located
        if hubLocation is None:
            if shouldDraw:
                x, y = screen.get_size()
            else:
                x, y = 1300, 800
            self.hubLocation = [x / 2, y / 2]
        self.hubRadius = hubRadius  # The radius of the agent's original home
        self.siteNoCloserThan = siteNoCloserThan  # The closest to the hub a site can randomly be generated
        self.siteNoFartherThan = siteNoFartherThan  # The furthest to the hub a site can randomly be generated
        self.initialHubAgentCount = hubAgentCount  # The number of agents at the start of the simulation
        self.siteList = []  # The sites in the world
        self.siteRectList = []  # List of site rectangles
        self.sitePositions = sitePositions  # Where the sites are located
        self.siteQualities = siteQualities  # The quality of each site
        self.sitesRadii = siteRadii  # A list of the radius of each site
        self.screen = screen  # The screen to draw the simulation on
        self.drawEstimates = drawEstimates  # Whether estimates are drawn (if False, actual values are drawn)
        self.shouldDrawPaths = shouldDrawPaths  # Whether paths behind the agents are drawn
        self.shouldDrawFog = True  # Whether the screen is initially filled with dark gray fog
        self.marker = None  # A marker drawn in the world representing a user's command

        self.knowSitePosAtStart = knowSitePosAtStart  # Whether the user knows site positions at the start of the simulation
        self.createSites(numSites)  # Initializes the site list with sites that match the specified values or random sites by default
        self.normalizeQuality()  # Set the site qualities so that the best is bright green and the worst bright red
        self.agentList = []  # List of all the agents in the world
        self.paths = []  # List of all the positions the agents have been to recently
        self.agentGroups = [[], [], [], [], [], [], [], [], [], []]  # Groups of agents that are selected together and assigned a number 0 - 9.
        self.hub = self.createHub()  # The agents' original home
        if self.shouldDraw:
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
                print("Site position index out of range. Assigning random position.")
                x = None
                y = None
            try:  # Try setting the quality to match the quality in the specified qualities list
                quality = self.siteQualities[siteIndex]
            except IndexError:  # If the qualities are not specified they will be randomized
                print("Site quality index out of range. Assigning random quality")
                quality = None
            try:  # Try setting the radius to match the radius in the specified radii list
                radius = self.sitesRadii[siteIndex]
            except IndexError:  # If the radii are not specified they will be randomized
                print("Site radius index out of range. Assigning radius to " + str(SITE_RADIUS))
                radius = SITE_RADIUS
            self.createSite(x, y, radius, quality, self.knowSitePosAtStart)

    def createSite(self, x, y, radius, quality, show):
        """ Creates a site with specified values. If values are none, then default values will apply """
        newSite = Site(self.screen, self.hubLocation, x, y, radius, quality,
                       self.siteNoCloserThan, self.siteNoFartherThan, show)
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
        w = self.screen.get_width()
        h = self.screen.get_height()
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

    def isClose(self, rect, pos):
        """ Returns whether the position and rectangle are close to each other """
        return rect.colliderect(pos[0] - (rect.width + HUB_OBSERVE_DIST) / 2,
                                pos[1] - (rect.height + HUB_OBSERVE_DIST) / 2,
                                (self.screen.get_width() / NUM_FOG_BLOCKS_X) + rect.width + HUB_OBSERVE_DIST,
                                (self.screen.get_height() / NUM_FOG_BLOCKS_Y) + rect.height + HUB_OBSERVE_DIST)

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
        hubSite = Site(self.screen, self.hubLocation, self.hubLocation[0], self.hubLocation[1], self.hubRadius, -1,
                       self.siteNoCloserThan, self.siteNoFartherThan, True)
        self.siteList.append(hubSite)
        self.siteRectList.append(hubSite.getSiteRect())
        hubSite.agentCount = self.initialHubAgentCount
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
        if self.shouldDrawPaths:  # If the paths should be drawn anywhere, the world can keep track of all of them
            self.paths.append(agent.getPosition())
            if len(self.paths) > 50 * len(self.agentList):
                for i in range(len(self.agentList)):
                    self.paths.pop(0)
        else:  # The agents will need to keep track of their paths so they can report it when they get to the hub an no other time.
            agent.updatePath()

    def setMarker(self, marker):
        self.marker = marker

    def drawWorldObjects(self):
        """ Draws the paths, agents, sites, markers, and fog in the world"""
        if self.shouldDrawPaths:
            self.drawPaths()
        self.drawAgents()
        if self.drawEstimates:
            for siteIndex in range(0, len(self.siteList)):
                self.siteList[siteIndex].drawEstimatedSite()
        else:
            for siteIndex in range(0, len(self.siteList)):
                self.siteList[siteIndex].drawSite()
        self.drawMarker()
        if self.shouldDrawFog:
            self.drawFog()

    def drawPaths(self):
        color = SCREEN_COLOR
        for posIndex, pos in enumerate(self.paths):
            if posIndex % len(self.agentList) == 0:
                color = color[0] - 1,  color[1] - 1, color[2] - 1
            pyg.draw.circle(self.screen, color, pos, 2)

    def drawAgents(self):
        for agent in self.agentList:
            agent.drawAgent(self.screen)

    def drawMarker(self):
        if self.marker is not None:
            self.screen.blit(self.marker[0], self.marker[1])

    def eraseFog(self, rect):
        fogIndices = rect.collidelist(self.fog)
        while fogIndices != -1:
            self.fog.pop(fogIndices)
            fogIndices = rect.collidelist(self.fog)

    def drawFog(self):
        r, g, b = 30, 30, 30
        for i in range(len(self.fog)):
            pyg.draw.rect(self.screen, (r, g, b), self.fog[i])

    def drawPotentialQuality(self, potentialQuality, font):
        """ Draws the value the selected sites will be set to if the user pushes Enter """
        img = font.render("Set quality: " + str(potentialQuality), True, (255 - potentialQuality, potentialQuality, 0))
        for site in self.siteList:
            if site.isSelected:
                self.screen.blit(img, (site.getPosition()[0] - (img.get_width() / 2), site.getPosition()[1] - (site.radius + 31), 15, 10))

    def updateGroup(self, index, agents):
        """ Sets an easily selectable group of agents to the specified agents """
        self.agentGroups[index] = agents

    def getGroup(self, index):
        """ Gets the group of agents that was set to the specified index """
        return self.agentGroups[index]

    def collidesWithSite(self, mousePos):
        """ Returns whether the mouse cursor is over any site in the world """
        for site in self.siteList:
            if site.wasFound and site.getSiteRect().collidepoint(mousePos):
                return True
        return False

    def collidesWithAgent(self, mousePos):
        """" Returns whether the mouse cursor is over any agent in the world """
        for agent in self.agentList:
            if agent.getAgentRect().collidepoint(mousePos):
                return True
        return False
