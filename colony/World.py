""" World class. Stores 2D positions of hub and sites """
import random

from colony.Site import *


class World:
    """ Represents the world around the ants old home """

    def __init__(self, numSites, screen, hubLocation, hubRadius, hubAgentCount, sitePositions, siteQualities, siteRadii,
                 siteNoCloserThan, siteNoFartherThan, shouldDraw):
        self.shouldDraw = shouldDraw  # Whether the simulation should be drawn on the screen
        self.hubLocation = hubLocation  # Where the agents' original home is located
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
        self.gloc = STATE_GRAPH_LOCATION  # The location of the graph that displays the number of agents in each state
        self.colors = COLORS  # The colors displayed on the state graph
        self.phaseGLoc = PHASE_GRAPH_LOCATION  # The location of the graph that displays the number of agents in each phase
        self.phaseColors = PHASE_COLORS  # The colors displayed on the phase graph
        pyg.font.init()
        self.myfont = pyg.font.SysFont('Comic Sans MS', 12)  # The font used on the graphs
        self.possibleStates = STATES_LIST  # The states that agents can be assigned to
        self.possiblePhases = PHASES_LIST  # The phases that agents can be assigned to
        self.createSites(numSites)  # Initializes the site list with sites that match the specified values or random sites by default
        self.normalizeQuality()  # Set the site qualities so that the best is bright green and the worst bright red
        self.agentList = []  # List of all the agents in the world
        self.hub = self.createHub()  # The agents' original home
        self.request = None  # The request, used to sent information to a rest API

    def randomizeState(self):
        for agent in self.agentList:
            agent.assignSite(self.siteList[random.randint(0, len(self.siteList) - 1)])
            agent.setPosition(agent.assignedSite.getPosition()[0], agent.assignedSite.getPosition()[1])

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
            self.createSite(x, y, radius, quality)

    def createSite(self, x, y, radius, quality):
        newSite = Site(self.screen, self.hubLocation, x, y, radius, quality, self.siteQualities,
                       self.siteNoCloserThan, self.siteNoFartherThan, self.shouldDraw)
        self.siteList.append(newSite)
        self.siteRectList.append(newSite.getSiteRect())

    def removeSite(self, site):
        if site.quality == -1:
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
            self.siteList[siteIndex].normalizeQuality(span, zero)

    def createHub(self):
        hubSite = Site(self.screen, self.hubLocation, self.hubLocation[0], self.hubLocation[1], self.hubRadius, -1,
                       self.siteQualities, self.siteNoCloserThan, self.siteNoFartherThan, self.shouldDraw)
        self.siteList.append(hubSite)
        self.siteRectList.append(hubSite.getSiteRect())
        hubSite.agentCount = self.initialHubAgentCount
        return hubSite

    def drawWorldObjects(self):
        for siteIndex in range(0, len(self.siteList)):
            self.siteList[siteIndex].drawSite()

    def getHubPosition(self):
        return self.hub.getPosition()

    def getSiteObserveRectList(self):
        return self.siteRectList

    def drawStateGraph(self, states):
        img = self.myfont.render("STATES:", True, (0, 0, 0))
        self.screen.blit(img, (self.gloc[0]-100, self.gloc[1] - 15))
        for state, width in enumerate(states):
            pyg.draw.rect(self.screen, self.colors[state], pyg.Rect(self.gloc[0], self.gloc[1] + state * 11, width, 10))
            img = self.myfont.render(self.possibleStates[state], True, self.colors[state])
            self.screen.blit(img, (self.gloc[0] - 100, self.gloc[1] - 5 + state * 11))

    def drawPhaseGraph(self, phases):
        img = self.myfont.render("PHASES:", True, (0, 0, 0))
        self.screen.blit(img, (self.phaseGLoc[0] - 100, self.phaseGLoc[1] - 15))
        for phase, width in enumerate(phases):
            pyg.draw.rect(self.screen, self.phaseColors[phase], pyg.Rect(self.phaseGLoc[0], self.phaseGLoc[1] + phase * 11, width, 10))
            img = self.myfont.render(self.possiblePhases[phase], True, self.phaseColors[phase])
            self.screen.blit(img, (self.phaseGLoc[0] - 100, self.phaseGLoc[1] - 5 + phase * 11))

    def drawSelectedAgentInfo(self, agent):
        attributes = agent.getAttributes()
        for i, attribute in enumerate(attributes):
            img = self.myfont.render(attribute, True, (0, 0, 0))
            self.screen.blit(img, (AGENT_INFO_LOCATION[0] - 100, AGENT_INFO_LOCATION[1] - 5 + i * 11))

    def drawSelectedSiteInfo(self, site, agentIsSelected, agentsPositions):
        attributes = ["SELECTED SITE:",
                      "Position: " + str(site.pos),
                      "Quality: " + str(site.getQuality()),
                      "Agent Count: " + str(site.agentCount),
                      "Agents' Positions: "]

        for position in agentsPositions:
            attributes.append(str(position))

        location = AGENT_INFO_LOCATION
        if agentIsSelected:
            location = SITE_INFO_LOCATION

        for i, attribute in enumerate(attributes):
            img = self.myfont.render(attribute, True, (0, 0, 0))
            self.screen.blit(img, (location[0] - 100, location[1] - 5 + i * 11))

    def drawPause(self):
        pausedFont = pyg.font.SysFont('Comic Sans MS', 40)
        img = pausedFont.render("Paused", True, (123, 123, 123))
        self.screen.blit(img, (self.hubLocation[0] - (img.get_width() / 2), self.hubLocation[1] - (img.get_height() / 2)))

    def drawFinish(self):
        pausedFont = pyg.font.SysFont('Comic Sans MS', 40)
        img = pausedFont.render("Finished", True, (123, 123, 123))
        self.screen.blit(img, (self.hubLocation[0] - (img.get_width() / 2), self.hubLocation[1] - (img.get_height() / 2)))

    def drawSelectRect(self, selectRectCorner, mousePos):
        if selectRectCorner[0] < mousePos[0]:
            left = selectRectCorner[0]
        else:
            left = mousePos[0]
        if selectRectCorner[1] < mousePos[1]:
            top = selectRectCorner[1]
        else:
            top = mousePos[1]
        width = np.abs(selectRectCorner[0] - mousePos[0])
        height = np.abs(selectRectCorner[1] - mousePos[1])
        return pyg.draw.rect(self.screen, (128, 128, 128), pyg.Rect(left, top, width, height))

    def drawPotentialQuality(self, potentialQuality):
        img = self.myfont.render("Set quality: " + str(potentialQuality), True, (255 - potentialQuality, potentialQuality, 0))
        for site in self.siteList:
            if site.isSelected:
                self.screen.blit(img, (site.getPosition()[0] - (img.get_width() / 2), site.getPosition()[1] - (site.radius + 31), 15, 10))

    def getSiteList(self):
        return self.siteList
