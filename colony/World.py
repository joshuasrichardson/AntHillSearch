""" World class. Stores 2D positions of hub and sites """
import random

from colony.Site import *


class World:
    """ Represents the world around the ants old home """

    def __init__(self, numSites, screen, hubLocation, hubRadius, hubAgentCount, sitePositions, siteQualities, siteRadii,
                 siteNoCloserThan, siteNoFartherThan, shouldDraw, knowSitePosAtStart, drawEstimates=DRAW_ESTIMATES,
                 hubCanMove=HUB_CAN_MOVE, shouldDrawPaths=SHOULD_DRAW_PATHS):
        self.shouldDraw = shouldDraw  # Whether the simulation should be drawn on the screen
        self.hubCanMove = hubCanMove
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
        self.drawEstimates = drawEstimates
        self.shouldDrawPaths = shouldDrawPaths
        self.onlyDrawExploredArea = True

        pyg.font.init()
        self.myfont = pyg.font.SysFont('Comic Sans MS', 12)  # The font used on the graphs
        self.marker = None

        self.knowSitePosAtStart = knowSitePosAtStart
        self.createSites(numSites)  # Initializes the site list with sites that match the specified values or random sites by default
        self.normalizeQuality()  # Set the site qualities so that the best is bright green and the worst bright red
        self.agentList = []  # List of all the agents in the world
        self.paths = []  # List of all the positions the agents have been to recently
        self.agentGroups = [[], [], [], [], [], [], [], [], [], []]  # Groups of agents that are selected together and assigned a number 0 - 9.
        self.hub = self.createHub()  # The agents' original home
        self.request = None  # The request, used to sent information to a rest API

        self.states = np.zeros((NUM_POSSIBLE_STATES,))  # List of the number of agents assigned to each state
        self.phases = np.zeros((NUM_POSSIBLE_PHASES,))  # List of the number of agents assigned to each phase

    def randomizeState(self):
        for agent in self.agentList:
            site = self.siteList[random.randint(0, len(self.siteList) - 1)]
            agent.addToKnownSites(site)
            agent.assignSite(site)
            agent.setPosition(agent.assignedSite.getPosition()[0], agent.assignedSite.getPosition()[1])

    def getSiteList(self):
        return self.siteList

    def getSiteIndex(self, site):
        return self.siteList.index(site)

    def setSitePosition(self, site, pos):
        siteIndex = self.siteList.index(site)
        self.siteList[siteIndex].setPosition(pos)
        self.siteRectList[siteIndex].centerx = pos[0]
        self.siteRectList[siteIndex].centery = pos[1]

    def createSites(self, numSites):
        # Create as many sites as required
        for siteIndex in range(0, numSites):
            try:
                x = self.sitePositions[siteIndex][0]
                y = self.sitePositions[siteIndex][1]
            except IndexError:
                print("Site position index out of range. Assigning random position.")
                x = None
                y = None
            try:
                quality = self.siteQualities[siteIndex]
            except IndexError:
                print("Site quality index out of range. Assigning random quality")
                quality = None
            try:
                radius = self.sitesRadii[siteIndex]
            except IndexError:
                print("Site radius index out of range. Assigning radius to " + str(SITE_RADIUS))
                radius = SITE_RADIUS
            self.createSite(x, y, radius, quality, self.knowSitePosAtStart)

    def createSite(self, x, y, radius, quality, show):
        newSite = Site(self.screen, self.hubLocation, x, y, radius, quality,
                       self.siteNoCloserThan, self.siteNoFartherThan, show)
        self.siteList.append(newSite)
        self.siteRectList.append(newSite.getSiteRect())

    def removeSite(self, site):
        if site.getQuality() == -1 and site.agentCount > 0:
            print("Cannot delete the hub")
        else:
            index = self.siteList.index(site, 0, len(self.siteList))
            self.siteList.pop(index)
            self.siteRectList.pop(index)
            del site

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

        if self.states[GO] == 0:
            self.marker = None

    def updatePaths(self, agent):
        if self.shouldDrawPaths:
            self.paths.append(agent.getPosition())
            if len(self.paths) > 50 * len(self.agentList):
                for i in range(len(self.agentList)):
                    self.paths.pop(0)
        else:
            agent.updatePath()

    def setMarker(self, marker):
        self.marker = marker

    def drawWorldObjects(self):
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
        # if self.onlyDrawExploredArea:
            # self.drawUnexploredDarkness()

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

    def drawUnexploredDarkness(self):
        darkness = pyg.Surface(self.screen.get_size())
        self.screen.blit(darkness, [0, 0])

    def drawPotentialQuality(self, potentialQuality):
        img = self.myfont.render("Set quality: " + str(potentialQuality), True, (255 - potentialQuality, potentialQuality, 0))
        for site in self.siteList:
            if site.isSelected:
                self.screen.blit(img, (site.getPosition()[0] - (img.get_width() / 2), site.getPosition()[1] - (site.radius + 31), 15, 10))

    def updateGroup(self, index, agents):
        self.agentGroups[index] = agents

    def getGroup(self, index):
        return self.agentGroups[index]
