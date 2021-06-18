""" World class. Stores 2D positions of hub and sites """
from Site import *


# TODO: set internal thresholds for each agent to switch out of a
#  existing state because of time-out. Replace magic numbers with
#  agent-specific thresholds. Use this to show how diversity is
#  necessary for increased resilience for the elements of autonomy paper

class World:
    def __init__(self, numSites, screen):
        self.hubLocation = HUB_LOCATION
        self.siteList = []
        self.siteRectList = []  # List of agent rectangles
        self.screen = screen
        self.numSites = numSites
        self.gloc = STATE_GRAPH_LOCATION
        self.colors = COLORS
        self.phaseGLoc = PHASE_GRAPH_LOCATION
        self.phaseColors = PHASE_COLORS
        pyg.font.init()
        self.myfont = pyg.font.SysFont('Comic Sans MS', 12)
        self.possible_states = STATES_LIST
        self.possiblePhases = PHASES_LIST
        # Create as many sites as required
        for siteIndex in range(0, numSites):
            newSite = Site(screen)
            self.siteList.append(newSite)
            self.siteRectList.append(newSite.getAgentRect())
        # Set the site qualities so that the best is bright green and the worst bright red
        self.normalizeQuality()
        self.createHub()

    def normalizeQuality(self):
        """Set the site qualities so that the best is bright green and the worst bright red"""
        # Normalize quality to be between lower bound and upper bound
        minValue = -np.inf
        maxValue = np.inf
        for siteIndex in range(0, self.numSites):
            quality = self.siteList[siteIndex].getQuality()
            if quality > minValue:
                minValue = quality
            if quality < maxValue:
                maxValue = quality
        zero = minValue
        span = maxValue - minValue
        for siteIndex in range(0, self.numSites):
            self.siteList[siteIndex].normalizeQuality(span, zero)

    def createHub(self):
        hubSite = Site(self.screen)
        self.siteList.append(hubSite)
        self.siteRectList.append(hubSite.getAgentRect())
        hubSite.pos = HUB_LOCATION
        hubSite.quality = -1  # because it is broken and they need a new home
        hubSite.color = 0, 0, 0
        hubSite.agentCount = NUM_AGENTS

    def drawWorldObjects(self):
        for siteIndex in range(0, self.numSites + 1):  # Add one for the hub
            self.siteList[siteIndex].drawSite()

    def getHubPosition(self):
        return self.hubLocation

    def getSiteObserveRectList(self):
        return self.siteRectList

    def drawStateGraph(self, arr):
        img = self.myfont.render("STATES:", True, (0, 0, 0))
        self.screen.blit(img, (self.gloc[0]-100, self.gloc[1] - 15))
        for id, ii in enumerate(arr):
            pyg.draw.rect(self.screen, self.colors[id], pyg.Rect(self.gloc[0], self.gloc[1] + id*11, ii, 10))
            img = self.myfont.render(self.possible_states[id], True, self.colors[id])
            self.screen.blit(img, (self.gloc[0]-100, self.gloc[1] - 5 + id*11))

    def drawPhaseGraph(self, arr):
        img = self.myfont.render("PHASES:", True, (0, 0, 0))
        self.screen.blit(img, (self.phaseGLoc[0]-100, self.phaseGLoc[1] - 15))
        for id, ii in enumerate(arr):
            pyg.draw.rect(self.screen, self.phaseColors[id], pyg.Rect(self.phaseGLoc[0], self.phaseGLoc[1] + id*11, ii, 10))
            img = self.myfont.render(self.possiblePhases[id], True, self.phaseColors[id])
            self.screen.blit(img, (self.phaseGLoc[0]-100, self.phaseGLoc[1] - 5 + id*11))

    def drawSelectedAgentInfo(self, agent):
        knownSitesPositions = []
        for site in agent.knownSites:
            knownSitesPositions.append(site.pos)
        siteToRecruitFromPos = None
        if agent.siteToRecruitFrom is not None:
            siteToRecruitFromPos = agent.siteToRecruitFrom.pos

        attributes = ["SELECTED AGENT:",
                      "Position: " + str(agent.pos),
                      "Assigned Site: " + str(agent.assignedSite.pos),
                      "Estimated Quality: " + str(agent.estimatedQuality),
                      "Target: " + str(agent.target),
                      "Speed: " + str(agent.speed),
                      "Known Sites: " + str(knownSitesPositions),
                      "Site to Recruit from: " + str(siteToRecruitFromPos),
                      "State: " + agent.stateToString(),
                      "Phase: " + agent.phaseToString(),
                      "Assessment Threshold: " + str(agent.assessmentThreshold),
                      "Lead Agent: " + str(agent.leadAgent),
                      "Number of followers: " + str(agent.numFollowers),
                      "Going to recruit: " + ("Yes" if agent.goingToRecruit else "No")]

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

    def getSiteList(self):
        return self.siteList
