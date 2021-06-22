""" Agent class. Stores 2D position and agent state """
import random

import numpy as np
import pygame as pyg
from Constants import *

# TODO: Consider separating the probability of changing states in different phases
#  (i.e. SEARCH -> AT_NEST in COMMIT_PHASE is less likely than SEARCH -> AT_NEST in EXPLORE_PHASE or something like that)

# TODO: Individualize more stuff?


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

        self.speed = random.uniform(MIN_AGENT_SPEED, MAX_AGENT_SPEED) * TIME_STEP  # AGENT_SPEED * TIME_STEP  # Speed the agent moves on the screen
        self.uncommittedSpeed = self.speed
        self.committedSpeed = self.speed * COMMIT_SPEED_FACTOR
        self.decisiveness = random.uniform(MIN_DECISIVENESS, MAX_DECISIVENESS)  # Influences how quickly an agent can assess
        self.navigationSkills = random.uniform(MIN_NAV_SKILLS, MAX_NAV_SKILLS)  # Influences how likely an agent is to get lost

        self.target = self.hubLocation  # Either the hub or a site the agent is going to
        self.angle = np.arctan2(self.target[1] - self.pos[1], self.target[0] - self.pos[0])  # Angle the agent is moving
        self.angularVelocity = 0  # Speed the agent is changing direction

        self.state = None  # The current state of the agent such as AT_NEST, SEARCH, FOLLOW, etc.
        self.phase = EXPLORE  # The current phase or level of commitment (explore, assess, canvas, commit)
        self.phaseColor = EXPLORE_COLOR  # A color to represent the phase so it can be seen on the screen

        self.assignedSite = self.hub  # Site that the agent has discovered and is trying to get others to go see
        self.estimatedQuality = -1  # The agent's evaluation of the assigned site. Initially -1 so they can like any site better than the broken home they are coming from.
        self.assessmentThreshold = 5  # A number to influence how long an agent will assess a site. Should be longer for lower quality sites.

        self.knownSites = {self.hub}  # A list of sites that the agent has been to before
        self.siteToRecruitFrom = None  # The site the agent chooses to go recruit from when in the LEAD_FORWARD or TRANSPORT state
        self.leadAgent = None  # The agent that is leading this agent in the FOLLOW state or carrying it in the BEING_CARRIED state
        self.numFollowers = 0  # The number of agents following the current agent in LEAD_FORWARD or TANDEM_RUN state
        self.goingToRecruit = False  # Whether the agent is heading toward a site to recruit or not.
        self.comingWithFollowers = False  # Whether the agent is coming back toward a new site with followers or not.

        self.isSelected = False  # Whether the user clicked on the agent or its site most recently.
        self.isTheSelected = False  # Whether the agent is the one with its information shown.

        self.estimationAccuracy = random.randint(0, MAX_QUALITY_MISJUDGMENT)  # How far off an agent's estimate of the quality of a site will be on average.
        self.speedCoefficient = 1

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
        self.speed = self.uncommittedSpeed * self.speedCoefficient
        if phase == EXPLORE:
            self.phaseColor = EXPLORE_COLOR
        elif phase == ASSESS:
            self.phaseColor = ASSESS_COLOR
        elif phase == CANVAS:
            self.phaseColor = CANVAS_COLOR
        elif phase == COMMIT:
            self.phaseColor = COMMIT_COLOR
            self.speed = self.committedSpeed * self.speedCoefficient

    def incrementFollowers(self):
        self.numFollowers += 1

    def drawAgent(self, surface):
        if self.isTheSelected:
            pyg.draw.circle(self.world.screen, THE_SELECTED_COLOR, self.pos, 15, 0)
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

    def estimateQuality(self, site):
        return site.getQuality() + \
            (self.estimationAccuracy if random.randint(0, 2) == 1 else -self.estimationAccuracy)
        # TODO: Make a bell curve instead of even distribution?

    def assignSite(self, site):
        if self.assignedSite is not None:
            self.assignedSite.decrementCount()
        if site is not self.assignedSite:
            self.setPhase(ASSESS)
        if site is not self.assignedSite:
            self.estimatedQuality = self.estimateQuality(site)
        self.assignedSite = site
        self.assignedSite.incrementCount()
        # Take longer to assess lower-quality sites
        self.assessmentThreshold = MAX_ASSESS_THRESHOLD - (self.estimatedQuality / ASSESS_DIVIDEND)

    def isDoneAssessing(self):
        return np.random.exponential(ASSESS_EXPONENTIAL) * self.decisiveness > self.assessmentThreshold * ASSESS_EXPONENTIAL

    def quorumMet(self):
        return self.assignedSite.agentCount > QUORUM_SIZE

    def shouldSearch(self):
        if self.assignedSite == self.hub:
            return np.random.exponential(SEARCH_EXPONENTIAL) > SEARCH_FROM_HUB_THRESHOLD * SEARCH_EXPONENTIAL
        return np.random.exponential(SEARCH_EXPONENTIAL) > SEARCH_THRESHOLD * SEARCH_EXPONENTIAL  # Make it more likely if they aren't at the hub.

    @staticmethod
    def shouldReturnToNest():
        return np.random.exponential(AT_NEST_EXPONENTIAL) > AT_NEST_THRESHOLD * AT_NEST_EXPONENTIAL

    @staticmethod
    def shouldRecruit():
        return np.random.exponential(LEAD_EXPONENTIAL) > LEAD_THRESHOLD * LEAD_EXPONENTIAL

    @staticmethod
    def shouldKeepTransporting():
        return np.random.randint(0, 3) != 0

    @staticmethod
    def shouldFollow():
        return np.random.exponential(FOLLOW_EXPONENTIAL) > FOLLOW_THRESHOLD * FOLLOW_EXPONENTIAL

    def shouldGetLost(self):
        return np.random.exponential(GET_LOST_EXPONENTIAL) > self.navigationSkills * GET_LOST_THRESHOLD * GET_LOST_EXPONENTIAL

    def select(self):
        self.isSelected = True

    def unselect(self):
        self.isSelected = False
        self.isTheSelected = False

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
        if self.state.state == GO:
            return "GO"

    def phaseToString(self):
        if self.phase == EXPLORE:
            return "EXPLORE"
        if self.phase == ASSESS:
            return "ASSESS"
        if self.phase == CANVAS:
            return "CANVAS"
        if self.phase == COMMIT:
            return "COMMIT"

    def getAttributes(self):
        knownSitesPositions = []
        for site in self.knownSites:
            knownSitesPositions.append(site.pos)
        siteToRecruitFromPos = None
        if self.siteToRecruitFrom is not None:
            siteToRecruitFromPos = self.siteToRecruitFrom.pos

        return ["SELECTED AGENT:",
                "Position: " + str(self.pos),
                "Assigned Site: " + str(self.assignedSite.pos),
                "Estimated Quality: " + str(self.estimatedQuality),
                "Target: " + str(self.target),
                "Speed: " + str(self.speed),
                "Decisiveness: " + str(self.decisiveness),
                "Navigation skills: " + str(self.navigationSkills),
                "Known Sites: " + str(knownSitesPositions),
                "Site to Recruit from: " + str(siteToRecruitFromPos),
                "State: " + self.stateToString(),
                "Phase: " + self.phaseToString(),
                "Assessment Threshold: " + str(self.assessmentThreshold),
                "Lead Agent: " + str(self.leadAgent),
                "Number of followers: " + str(self.numFollowers),
                "Going to recruit: " + ("Yes" if self.goingToRecruit else "No")]
