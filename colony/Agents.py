""" Agent class. Stores 2D position and agent state """
import random
import numpy as np
import pygame
from Constants import *
from phases.AssessPhase import AssessPhase
from phases.ExplorePhase import ExplorePhase


# TODO: Consider separating the probability of changing states in different phases
#  (i.e. SEARCH -> AT_NEST in COMMIT_PHASE is less likely than SEARCH -> AT_NEST in EXPLORE_PHASE or something like that)


class Agent:
    """ Represents an agent that works to find a new nest when the old one is broken by going through different
    phases and states"""

    def __init__(self, world, startingAssignment, homogenousAgents=HOMOGENOUS_AGENTS, minSpeed=MIN_AGENT_SPEED,
                 maxSpeed=MAX_AGENT_SPEED, minDecisiveness=MIN_DECISIVENESS, maxDecisiveness=MAX_DECISIVENESS,
                 minNavSkills=MIN_NAV_SKILLS, maxNavSkills=MAX_NAV_SKILLS, minEstAccuracy=MIN_QUALITY_MISJUDGMENT,
                 maxEstAccuracy=MAX_QUALITY_MISJUDGMENT, startingPosition=HUB_LOCATION, maxSearchDistance=MAX_SEARCH_DIST):
        self.world = world  # The colony the agent lives in

        self.prevPos = startingPosition  # Initial position
        self.pos = startingPosition  # Initial position
        self.agentHandle = pygame.image.load("copter.png")  # Image on screen representing the agent
        self.agentRect = self.agentHandle.get_rect()  # Rectangle around the agent to help track collisions
        self.agentRect.centerx = self.pos[0]  # Horizontal center of the agent
        self.agentRect.centery = self.pos[1]  # Vertical center of the agent

        self.homogenousAgents = homogenousAgents  # Whether all the agents have the same attributes (if false, their attributes vary)
        self.speed = self.initializeAttribute(minSpeed, maxSpeed)  # Speed the agent moves on the screen
        self.uncommittedSpeed = self.speed  # The speed of the agents outside the committed phase
        self.committedSpeed = self.speed * COMMIT_SPEED_FACTOR  # The speed of the agents in the committed phase
        self.decisiveness = self.initializeAttribute(minDecisiveness, maxDecisiveness)  # Influences how quickly an agent can assess
        self.navigationSkills = self.initializeAttribute(minNavSkills, maxNavSkills)  # Influences how likely an agent is to get lost
        self.estimationAccuracy = self.initializeAttribute(minEstAccuracy, maxEstAccuracy)  # How far off an agent's estimate of the quality of a site will be on average.

        self.target = startingPosition  # The position the agent is going to
        self.angle = np.arctan2(self.target[1] - self.pos[1], self.target[0] - self.pos[0])  # Angle the agent is moving
        self.angularVelocity = 0  # Speed the agent is changing direction
        self.maxSearchDistance = maxSearchDistance

        self.state = None  # The current state of the agent such as AT_NEST, SEARCH, FOLLOW, etc.
        self.phase = ExplorePhase()  # The current phase or level of commitment (explore, assess, canvas, commit)

        self.assignedSite = startingAssignment  # Site that the agent has discovered and is trying to get others to go see
        self.estimatedQuality = -1  # The agent's evaluation of the assigned site. Initially -1 so they can like any site better than the broken home they are coming from.
        self.assessmentThreshold = 5  # A number to influence how long an agent will assess a site. Should be longer for lower quality sites.
        self.speedCoefficient = 1  # The number multiplied my the agent's original speed to get its current speed

        self.knownSites = {self.getHub()}  # A list of sites that the agent has been to before
        self.knownSites.add(startingAssignment)
        self.siteToRecruitFrom = None  # The site the agent chooses to go recruit from when in the LEAD_FORWARD or TRANSPORT state
        self.leadAgent = None  # The agent that is leading this agent in the FOLLOW state or carrying it in the BEING_CARRIED state
        self.numFollowers = 0  # The number of agents following the current agent in LEAD_FORWARD or TANDEM_RUN state
        self.goingToRecruit = False  # Whether the agent is heading toward a site to recruit or not.
        self.comingWithFollowers = False  # Whether the agent is coming back toward a new site with followers or not.

        self.isSelected = False  # Whether the user clicked on the agent or its site most recently.
        self.isTheSelected = False  # Whether the agent is the one with its information shown.

    def initializeAttribute(self, minimum, maximum):
        if self.homogenousAgents:
            return maximum
        else:
            return random.uniform(minimum, maximum)

    def setState(self, state):
        self.state = state

    def changeState(self, neighborList):
        self.state.changeState(neighborList)

    def getState(self):
        return self.state.state

    def getStateColor(self):
        return self.state.getColor()

    def phaseToString(self):
        return self.phase.toString()

    def getPhaseColor(self):
        return self.phase.getColor()

    def getPhaseNumber(self):
        return self.phase.getNumber()

    def getPosition(self):
        self.pos = [self.agentRect.centerx, self.agentRect.centery]
        return self.pos

    def setPosition(self, x, y):
        self.agentRect.centerx = x
        self.agentRect.centery = y
        self.pos = [x, y]

    def updatePosition(self, position):
        self.prevPos = self.pos
        if position is None:
            self.agentRect.centerx = int(np.round(float(self.pos[0]) + self.speed * np.cos(self.angle)))
            self.agentRect.centery = int(np.round(float(self.pos[1]) + self.speed * np.sin(self.angle)))
        else:
            self.agentRect.centerx = position[0]
            self.agentRect.centery = position[1]
        self.pos = [self.agentRect.centerx, self.agentRect.centery]

    def updateFollowPosition(self):
        self.agentRect.centerx = int(np.round(float(self.leadAgent.pos[0]) - self.leadAgent.speed * np.cos(self.leadAgent.angle)))
        self.agentRect.centery = int(np.round(float(self.leadAgent.pos[1]) - self.leadAgent.speed * np.sin(self.leadAgent.angle)))
        self.pos = [self.agentRect.centerx, self.agentRect.centery]

    def setPhase(self, phase):
        self.phase = phase
        self.speed = phase.getSpeed(self.uncommittedSpeed, self.committedSpeed)

    def getHub(self):
        return self.world.getHub()

    def getAgentRect(self):
        return self.agentRect

    def incrementFollowers(self):
        self.numFollowers += 1

    def drawAgent(self, surface):
        if self.isTheSelected:
            pygame.draw.circle(self.world.screen, THE_SELECTED_COLOR, self.pos, 15, 0)
        if self.isSelected:
            pygame.draw.circle(self.world.screen, SELECTED_COLOR, self.pos, 12, 0)
        surface.blit(self.agentHandle, self.agentRect)

        if SHOW_AGENT_COLORS:
            pygame.draw.ellipse(surface, self.state.getColor(), self.agentRect, 4)
            pygame.draw.ellipse(surface, self.phase.getColor(), self.agentRect, 2)

        if SHOW_ESTIMATED_QUALITY:
            img = self.world.font.render(str(self.estimatedQuality), True, self.assignedSite.color)
            self.world.screen.blit(img, (self.pos[0] + 10, self.pos[1] + 5, 15, 10))

    def isTooFarAway(self, site):
        from math import isclose
        tooFarX = not isclose(self.pos[0], site.getPosition()[0], abs_tol=self.maxSearchDistance)
        tooFarY = not isclose(self.pos[1], site.getPosition()[1], abs_tol=self.maxSearchDistance)
        return tooFarX or tooFarY

    def estimateQuality(self, site):
        return site.getQuality() + \
            (self.estimationAccuracy if random.randint(0, 2) == 1 else -self.estimationAccuracy)
        # TODO: Make a bell curve instead of even distribution

    def assignSite(self, site):
        if self.assignedSite is not None:
            self.assignedSite.decrementCount()
        if site is not self.assignedSite:
            self.setPhase(AssessPhase())
            self.estimatedQuality = self.estimateQuality(site)
        self.assignedSite = site
        self.assignedSite.incrementCount()
        # Take longer to assess lower-quality sites
        self.assessmentThreshold = MAX_ASSESS_THRESHOLD - (self.estimatedQuality / ASSESS_DIVIDEND)

    def getAssignedSiteIndex(self):
        return self.world.getSiteIndex(self.assignedSite)

    def isDoneAssessing(self):
        return np.random.exponential() * self.decisiveness > self.assessmentThreshold

    def quorumMet(self):
        return self.assignedSite.agentCount > QUORUM_SIZE

    def shouldSearch(self):
        if self.assignedSite == self.getHub():
            return np.random.exponential() > SEARCH_FROM_HUB_THRESHOLD
        return np.random.exponential() > SEARCH_THRESHOLD  # Make it more likely if they aren't at the hub.

    @staticmethod
    def shouldReturnToNest():
        return np.random.exponential() > AT_NEST_THRESHOLD

    @staticmethod
    def shouldRecruit():
        return np.random.exponential() > LEAD_THRESHOLD

    @staticmethod
    def shouldKeepTransporting():
        return np.random.randint(0, 3) != 0

    @staticmethod
    def shouldFollow():
        return np.random.exponential() > FOLLOW_THRESHOLD

    def shouldGetLost(self):
        return np.random.exponential() > self.navigationSkills * GET_LOST_THRESHOLD

    @staticmethod
    def transportOrReverseTandem(state):
        if np.random.randint(0, 3) == 0:
            from states.ReverseTandemState import ReverseTandemState
            state.setState(ReverseTandemState(state.agent), state.agent.assignedSite.pos)
        else:
            from states.TransportState import TransportState
            state.setState(TransportState(state.agent), state.agent.assignedSite.pos)

    def select(self):
        self.isSelected = True

    def unselect(self):
        self.isSelected = False
        self.isTheSelected = False

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
                "State: " + self.state.toString(),
                "Phase: " + self.phaseToString(),
                "Assessment Threshold: " + str(self.assessmentThreshold),
                "Lead Agent: " + str(self.leadAgent),
                "Number of followers: " + str(self.numFollowers),
                "Going to recruit: " + ("Yes" if self.goingToRecruit else "No")]
