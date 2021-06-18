""" Agent class. Stores 2D position and agent state """
import numpy as np
import pygame as pyg
from Constants import *

# TODO: set internal thresholds for each agent to switch out of an
#  existing state because of time-out. Replace magic numbers with
#  agent-specific thresholds. Use this to show how diversity is
#  necessary for increased resilience for the elements of autonomy paper

# TODO: Fix this problem: Sometimes when they are committed to a site, and they follow someone to another site that is better,
#  they don't choose to be assigned to that site.

# TODO: Add a way to select an agent and have its important attributes show up (known sites, assigned site, pos, etc.)

# TODO: Make committed agents move faster than canvasing agents. How much?

# TODO: Mess with the length of time in the assessment phase.

# TODO: Add individual behavior: estimated quality accuracy (how close their estimated quality is to the site quality),
#                                speed (how fast they move),
#                                decisiveness (how fast they can assess),
#                                navigation skills (likeliness of getting lost)

# TODO: Let estimated quality become more accurate as assessment time goes on.

# TODO: Consider keeping assessing+ agents close to their site when searching. Maybe not necessary.

# TODO: Consider separating the probability of changing states in different phases
#  (i.e. SEARCH -> AT_NEST in COMMIT_PHASE is less likely than SEARCH -> AT_NEST in EXPLORE_PHASE or something like that)


class Agent:

    def __init__(self, world):
        self.world = world  # The colony the agent lives in
        self.siteObserveRectList = world.getSiteObserveRectList()  # List of rectangles of all the sites in the colony
        self.siteList = world.getSiteList()  # List of all the sites in the colony
        self.hubLocation = world.getHubPosition()  # Original home location
        self.hub = self.siteList[len(self.siteList) - 1]  # Original home that the agents are leaving

        self.pos = world.getHubPosition()  # Initial position
        self.agentHandle = pyg.image.load("../copter.png")  # Image on screen representing the agent
        self.agentRect = self.agentHandle.get_rect()  # Rectangle around the agent to help track collisions
        self.agentRect.centerx = self.pos[0]  # Horizontal center of the agent
        self.agentRect.centery = self.pos[1]  # Vertical center of the agent
        self.speed = AGENT_SPEED * TIME_STEP  # Speed the agent moves on the screen
        self.target = self.hubLocation  # Either the hub or a site the agent is going to
        self.angle = np.arctan2(self.target[1] - self.pos[1], self.target[0] - self.pos[0])  # Angle the agent is moving
        self.angularVelocity = 0  # Speed the agent is changing direction

        self.state = None  # The current state of the agent such as AT_NEST, SEARCH, FOLLOW, etc.
        self.phase = EXPLORE_PHASE  # The current phase or level of commitment (explore, assess, canvas, commit)
        self.phaseColor = EXPLORE_PHASE_COLOR  # A color to represent the phase so it can be seen on the screen

        self.assignedSite = self.hub  # Site that the agent has discovered and is trying to get others to go see
        self.estimatedQuality = -1  # The agent's evaluation of the assigned site. Initially -1 so they can like any site better than the broken home they are coming from.
        self.assessmentThreshold = 5  # A number to influence how long an agent will assess a site. Should be longer for lower quality sites.

        self.knownSites = {self.hub}  # A list of sites that the agent has been to before
        self.siteToRecruitFrom = None  # The site the agent chooses to go recruit from when in the LEAD_FORWARD or TRANSPORT state
        self.leadAgent = None  # The agent that is leading this agent in the FOLLOW state or carrying it in the BEING_CARRIED state
        self.numFollowers = 0  # The number of agents following the current agent in LEAD_FORWARD or TANDEM_RUN state
        self.goingToRecruit = False  # Whether the agent is heading toward a site to recruit or not.
        self.comingWithFollowers = False  # Whether the agent is coming back toward a new site with followers or not.

        self.isSelected = False  # Whether the user clicked on the agent most recently.

    def setState(self, state):
        self.state = state

    def changeState(self, neighborList):
        self.state.changeState(neighborList)

    def getState(self):
        return self.state.state

    def getColor(self):
        return self.state.color

    def getPosition(self):
        self.pos = [self.agentRect.centerx, self.agentRect.centery]
        return self.pos

    def setPosition(self, x, y):
        self.agentRect.centerx = x
        self.agentRect.centery = y

    def updatePosition(self):
        self.agentRect.centerx = int(np.round(float(self.pos[0]) + self.speed * np.cos(self.angle)))
        self.agentRect.centery = int(np.round(float(self.pos[1]) + self.speed * np.sin(self.angle)))
        self.pos = [self.agentRect.centerx, self.agentRect.centery]

    def updateFollowPosition(self):
        self.agentRect.centerx = int(np.round(float(self.leadAgent.pos[0]) - self.leadAgent.speed * np.cos(self.leadAgent.angle)))
        self.agentRect.centery = int(np.round(float(self.leadAgent.pos[1]) - self.leadAgent.speed * np.sin(self.leadAgent.angle)))
        self.pos = [self.agentRect.centerx, self.agentRect.centery]

    def setPhase(self, phase):
        self.phase = phase
        if phase == EXPLORE_PHASE:
            self.phaseColor = EXPLORE_PHASE_COLOR
        elif phase == ASSESS_PHASE:
            self.phaseColor = ASSESS_PHASE_COLOR
        elif phase == CANVAS_PHASE:
            self.phaseColor = CANVAS_PHASE_COLOR
        elif phase == COMMIT_PHASE:
            self.phaseColor = COMMIT_PHASE_COLOR

    def incrementFollowers(self):
        self.numFollowers += 1

    def drawAgent(self, surface):
        if self.isSelected:
            pyg.draw.circle(self.world.screen, SELECTED_COLOR, self.pos, 12, 0)
        surface.blit(self.agentHandle, self.agentRect)

        pyg.draw.ellipse(surface, self.state.color, self.agentRect, 4)
        pyg.draw.ellipse(surface, self.phaseColor, self.agentRect, 2)

        if self.assignedSite is None:
            img = self.world.myfont.render(str(self.estimatedQuality), True, self.state.color)
        else:
            img = self.world.myfont.render(str(self.estimatedQuality), True, self.assignedSite.color)
        self.world.screen.blit(img, (self.pos[0] + 10, self.pos[1] + 5, 15, 10))

    def getAgentHandle(self):
        return self.agentHandle

    def getAgentRect(self):
        return self.agentRect

    def assignSite(self, site):
        if self.assignedSite is not None:
            self.assignedSite.decrementCount()
        if site is not self.assignedSite:
            self.setPhase(ASSESS_PHASE)
        self.assignedSite = site
        self.assignedSite.incrementCount()
        self.estimatedQuality = self.assignedSite.getQuality()
        self.assessmentThreshold = 9 - (self.estimatedQuality / 36)  # Take longer to assess lower-quality sites

    def isDoneAssessing(self):
        return np.random.exponential(ASSESS_EXPONENTIAL) > self.assessmentThreshold * ASSESS_EXPONENTIAL

    def quorumMet(self):
        return self.assignedSite.agentCount > QUORUM_SIZE

    def shouldSearch(self):
        if self.assignedSite == self.hub:
            return np.random.exponential(SEARCH_EXPONENTIAL) > SEARCH_FROM_HUB_THRESHOLD * SEARCH_EXPONENTIAL
        return np.random.exponential(SEARCH_EXPONENTIAL) > SEARCH_THRESHOLD * SEARCH_EXPONENTIAL  # Make it more likely if they aren't at the hub.

    def shouldReturnToNest(self):
        return np.random.exponential(AT_NEST_EXPONENTIAL) > AT_NEST_THRESHOLD * AT_NEST_EXPONENTIAL

    def shouldRecruit(self):
        return np.random.exponential(LEAD_EXPONENTIAL) > LEAD_THRESHOLD * LEAD_EXPONENTIAL

    def shouldFollow(self):
        return np.random.exponential(FOLLOW_EXPONENTIAL) > FOLLOW_THRESHOLD * FOLLOW_EXPONENTIAL

    def shouldGetLost(self):
        return np.random.exponential(GET_LOST_EXPONENTIAL) > GET_LOST_THRESHOLD * GET_LOST_EXPONENTIAL

    def shouldKeepTransporting(self):
        return np.random.randint(0, 3) != 0

    def select(self):
        self.isSelected = True

    def unselect(self):
        self.isSelected = False

    def stateToString(self):
        if self.state.state == AT_NEST:
            return "AT_NEST"
        if self.state.state == SEARCH:
            return "SEARCH"
        if self.state.state == FOLLOW:
            return "FOLLOW"
        if self.state.state == LEAD_FORWARD:
            return "LEAD_FORWARD"
        if self.state.state == REVERSE_TANDEM:
            return "REVERSE_TANDEM"
        if self.state.state == TRANSPORT:
            return "TRANSPORT"
        if self.state.state == CARRIED:
            return "CARRIED"

    def phaseToString(self):
        if self.phase == EXPLORE_PHASE:
            return "EXPLORE"
        if self.phase == ASSESS_PHASE:
            return "ASSESS"
        if self.phase == CANVAS_PHASE:
            return "CANVAS"
        if self.phase == COMMIT_PHASE:
            return "COMMIT"
