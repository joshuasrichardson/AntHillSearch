""" Agent class. Stores 2D position and agent state """
import random
import numpy as np
import pygame
from Constants import *
from colony.PygameUtils import getAgentImage, rotateImage, getDestinationMarker, drawDashedLine
from phases.AssessPhase import AssessPhase
from phases.ExplorePhase import ExplorePhase


class Agent:
    """ Represents an agent that works to find a new nest when the old one is broken by going through different
    phases and states"""

    def __init__(self, world, startingAssignment, homogenousAgents=HOMOGENOUS_AGENTS, minSpeed=MIN_AGENT_SPEED,
                 maxSpeed=MAX_AGENT_SPEED, minDecisiveness=MIN_DECISIVENESS, maxDecisiveness=MAX_DECISIVENESS,
                 minNavSkills=MIN_NAV_SKILLS, maxNavSkills=MAX_NAV_SKILLS, minEstAccuracy=MIN_QUALITY_MISJUDGMENT,
                 maxEstAccuracy=MAX_QUALITY_MISJUDGMENT, startingPosition=HUB_LOCATION,
                 maxSearchDistance=MAX_SEARCH_DIST, findAssignedSiteEasily=FIND_SITES_EASILY,
                 commitSpeedFactor=COMMIT_SPEED_FACTOR, drawFarAgents=DRAW_FAR_AGENTS):
        self.world = world  # The colony the agent lives in

        self.prevPos = startingPosition  # Initial position
        self.pos = startingPosition  # Initial position
        self.path = []
        self.agentHandle = getAgentImage(self.pos)  # Image on screen representing the agent
        self.agentRect = self.agentHandle.get_rect()  # Rectangle around the agent to help track collisions
        self.agentRect.centerx = self.pos[0]  # Horizontal center of the agent
        self.agentRect.centery = self.pos[1]  # Vertical center of the agent
        self.drawFarAgents = drawFarAgents  # Whether the agent is drawn when it is not by the hub

        self.homogenousAgents = homogenousAgents  # Whether all the agents have the same attributes (if false, their attributes vary)
        self.findAssignedSiteEasily = findAssignedSiteEasily
        self.speed = self.initializeAttribute(minSpeed, maxSpeed)  # Speed the agent moves on the screen
        self.uncommittedSpeed = self.speed  # The speed of the agents outside the committed phase
        self.committedSpeed = self.speed * commitSpeedFactor  # The speed of the agents in the committed phase
        self.decisiveness = self.initializeAttribute(minDecisiveness, maxDecisiveness)  # Influences how quickly an agent can assess
        self.navigationSkills = self.initializeAttribute(minNavSkills, maxNavSkills)  # Influences how likely an agent is to get lost
        self.estimationAccuracy = self.initializeAttribute(minEstAccuracy, maxEstAccuracy)  # How far off an agent's estimate of the quality of a site will be on average.
        self.assessmentThreshold = 5  # A number to influence how long an agent will assess a site. Should be longer for lower quality sites.
        self.speedCoefficient = 1  # The number multiplied my the agent's original speed to get its current speed

        self.target = startingPosition  # The position the agent is going to
        self.angle = np.arctan2(self.target[1] - self.pos[1], self.target[0] - self.pos[0])  # Angle the agent is moving
        self.angularVelocity = 0  # Speed the agent is changing direction
        self.maxSearchDistance = maxSearchDistance

        self.state = None  # The current state of the agent such as AT_NEST, SEARCH, FOLLOW, etc.
        self.phase = ExplorePhase()  # The current phase or level of commitment (explore, assess, canvas, commit)

        self.assignedSite = startingAssignment  # Site that the agent has discovered and is trying to get others to go see
        self.estimatedQuality = -1  # The agent's evaluation of the assigned site. Initially -1 so they can like any site better than the broken home they are coming from.
        self.estimatedAgentCount = self.getHub().agentCount
        self.estimatedRadius = self.getHub().radius
        self.assignedSiteLastKnownPos = self.assignedSite.getPosition()
        self.estimatedSitePosition = self.assignedSite.getPosition()

        self.knownSites = [self.getHub()]  # A list of sites that the agent has been to before
        self.knownSitesPositions = [self.getHub().getPosition()]
        self.addToKnownSites(startingAssignment)
        self.siteToRecruitFrom = None  # The site the agent chooses to go recruit from when in the LEAD_FORWARD or TRANSPORT state
        self.recruitSiteLastKnownPos = None
        self.leadAgent = None  # The agent that is leading this agent in the FOLLOW state or carrying it in the BEING_CARRIED state
        self.numFollowers = 0  # The number of agents following the current agent in LEAD_FORWARD or TANDEM_RUN state
        self.goingToRecruit = False  # Whether the agent is heading toward a site to recruit or not.
        self.comingWithFollowers = False  # Whether the agent is coming back toward a new site with followers or not.

        self.isSelected = False  # Whether the user clicked on the agent or its site most recently.
        self.isTheSelected = False  # Whether the agent is the one with its information shown.
        self.marker = None

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

    def setAngle(self, angle):
        self.angle = angle

    def getStateColor(self):
        return self.state.getColor()

    def setPhase(self, phase):
        self.phase = phase
        self.speed = phase.getSpeed(self.uncommittedSpeed, self.committedSpeed, self.speedCoefficient)

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

    def getAssignedSitePosition(self):
        if self.findAssignedSiteEasily:
            return self.assignedSite.getPosition()
        else:
            return self.assignedSiteLastKnownPos

    def getRecruitSitePosition(self):
        if self.findAssignedSiteEasily:
            return self.siteToRecruitFrom.getPosition()
        else:
            return self.recruitSiteLastKnownPos

    def updatePath(self):
        self.path.append(self.pos)
        if len(self.path) > 50:
            self.path.pop(0)

    def getHub(self):
        return self.world.getHub()

    def getAgentRect(self):
        return self.agentRect

    def incrementFollowers(self):
        self.numFollowers += 1

    def drawPath(self, surface):
        color = SCREEN_COLOR
        for pos in self.path:
            color = color[0] - 1,  color[1] - 1, color[2] - 1
            pygame.draw.circle(surface, color, pos, 2)

    def drawKnownSiteMarkers(self, surface):
        for pos in self.knownSitesPositions:
            pygame.draw.circle(surface, FOLLOW_COLOR, pos, SITE_RADIUS + 8, 2)

    def drawAssignedSite(self):
        self.assignedSite.drawAssignmentMarker(self.pos, self.getPhaseColor())

    def drawTarget(self, surface):
        if self.target is not None:
            self.marker = getDestinationMarker(self.target)
            self.drawMarker(surface)

    def drawMarker(self, surface):
        if self.marker is not None:
            drawDashedLine(surface, BORDER_COLOR, self.pos, self.marker[1].center)
            surface.blit(self.marker[0], self.marker[1])

    def drawAgent(self, surface):
        if not self.drawFarAgents and self.isClose(self.getHub().getPosition(), self.getHub().radius + HUB_OBSERVE_DIST):
            self.drawPath(surface)
        if self.drawFarAgents or self.isClose(self.getHub().getPosition(), self.getHub().radius + HUB_OBSERVE_DIST):
            if self.isTheSelected:
                self.drawKnownSiteMarkers(surface)
                self.drawAssignedSite()
                self.drawTarget(surface)
            if self.isSelected:
                pygame.draw.circle(surface, self.state.getColor(), self.agentRect.center, self.agentHandle.get_width() * 3 / 5, 2)
                pygame.draw.circle(surface, self.phase.getColor(), self.agentRect.center, self.agentHandle.get_width() * 3 / 4, 2)
            w, h = self.agentHandle.get_size()
            rotateImage(surface, self.agentHandle, self.pos, [w / 2, h / 2], (-self.angle * 180 / np.pi) - 132)

            if SHOW_ESTIMATED_QUALITY:
                img = self.world.font.render(str(self.estimatedQuality), True, self.assignedSite.color)
                surface.blit(img, (self.pos[0] + 10, self.pos[1] + 5, 15, 10))

    def isClose(self, position, distance):
        from math import isclose
        closeX = isclose(self.pos[0], position[0], abs_tol=distance)
        closeY = isclose(self.pos[1], position[1], abs_tol=distance)
        return closeX and closeY

    def isTooFarAway(self, site):
        from math import isclose
        tooFarX = not isclose(self.pos[0], site.getPosition()[0], abs_tol=self.maxSearchDistance)
        tooFarY = not isclose(self.pos[1], site.getPosition()[1], abs_tol=self.maxSearchDistance)
        return tooFarX or tooFarY

    def estimateQuality(self, site):
        return site.getQuality() + \
            (self.estimationAccuracy if random.randint(0, 2) == 1 else -self.estimationAccuracy)

    def estimateAgentCount(self, site):
        return site.agentCount

    def estimateRadius(self, site):
        estimate = site.radius + ((self.estimationAccuracy / 4) if random.randint(0, 2) == 1 else (-(self.estimationAccuracy / 4)))
        if estimate < 0:
            estimate = 1
        return estimate

    def addToKnownSites(self, site):
        if not self.knownSites.__contains__(site):
            self.knownSites.append(site)
            self.knownSitesPositions.append(site.getPosition())

    def removeKnownSite(self, site):
        if self.knownSites.__contains__(site):
            if site is self.assignedSite:
                self.assignSite(self.getHub())
            index = self.knownSites.index(site)
            self.knownSites.remove(site)
            self.knownSitesPositions.pop(index)

    def assignSite(self, site):
        if self.assignedSite is not None:
            self.assignedSite.decrementCount()
        if site.getPosition()[0] != self.assignedSite.getPosition()[0] and\
                site.getPosition()[1] != self.assignedSite.getPosition()[1] and\
                site is not self.assignedSite:
            self.setPhase(AssessPhase())
            self.estimatedQuality = self.estimateQuality(site)
            self.estimatedAgentCount = self.estimateAgentCount(site)
            self.estimatedRadius = self.estimateRadius(site)
            self.estimatedSitePosition = self.estimateSitePosition(site)
        else:
            self.estimateSitePositionMoreAccurately()
        self.assignedSite = site
        self.assignedSiteLastKnownPos = site.getPosition()
        self.assignedSite.incrementCount()
        # Take longer to assess lower-quality sites
        self.assessmentThreshold = MAX_ASSESS_THRESHOLD - (self.estimatedQuality / ASSESS_DIVIDEND)

    def estimateSitePosition(self, site):
        if not self.world.hubCanMove and site is self.getHub():
            estimatedSitePosition = self.getHub().getPosition()
        else:
            estimatedSitePosition = site.getPosition().copy()
            estimatedSitePosition[0] = site.getPosition()[0] + random.randint(-100, 100)
            estimatedSitePosition[1] = site.getPosition()[1] + random.randint(-100, 100)
        return estimatedSitePosition

    def estimateSitePositionMoreAccurately(self):
        if self.estimatedSitePosition[0] != self.getAssignedSitePosition()[0]:
            self.estimatedSitePosition[0] = (self.estimatedSitePosition[0] + self.getAssignedSitePosition()[0]) / 2
        if self.estimatedSitePosition[1] != self.getAssignedSitePosition()[1]:
            self.estimatedSitePosition[1] = (self.estimatedSitePosition[1] + self.getAssignedSitePosition()[1]) / 2

    def getAssignedSiteIndex(self):
        return self.world.getSiteIndex(self.assignedSite)

    def isDoneAssessing(self):
        return np.random.exponential() * self.decisiveness > self.assessmentThreshold

    def quorumMet(self):
        return self.assignedSite.agentCount > QUORUM_SIZE

    def shouldSearch(self, siteWithinRange):
        if siteWithinRange == -1:
            # When self.findAssignedSiteEasily is False, this will be False everytime.
            # When self.findAssignedSiteEasily is True, this will only be True if the agent is
            # close to where their site was before it moved.
            if self.isClose(self.getAssignedSitePosition(), self.assignedSite.radius):
                self.removeKnownSite(self.assignedSite)
                return True
        if not self.world.siteList[siteWithinRange] is self.assignedSite:
            # They should get back to their site before they go out searching again.
            return False
        if self.assignedSite == self.getHub():
            return np.random.exponential() > SEARCH_FROM_HUB_THRESHOLD
        return np.random.exponential() > SEARCH_THRESHOLD  # Make it more likely to search if they aren't at the hub.

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

    def transportOrReverseTandem(self, state):
        if np.random.randint(0, 3) == 0:
            from states.ReverseTandemState import ReverseTandemState
            state.setState(ReverseTandemState(self), self.getAssignedSitePosition())
        else:
            from states.TransportState import TransportState
            state.setState(TransportState(self), self.getAssignedSitePosition())

    def select(self):
        self.isSelected = True

    def unselect(self):
        self.isSelected = False
        self.isTheSelected = False

    def getAttributes(self):
        knownSitesPositions = []
        for site in self.knownSites:
            knownSitesPositions.append(site.getPosition())

        return ["SELECTED AGENT:",
                "Estimated Quality: " + str(self.estimatedQuality),
                "Speed: " + str(self.speed),
                "Decisiveness: " + str(self.decisiveness),
                "Navigation skills: " + str(self.navigationSkills),
                "Known Sites: " + str(knownSitesPositions),
                "Thinks Known Sites are at: " + str(self.knownSitesPositions),
                "Assessment Threshold: " + str(self.assessmentThreshold),
                "Lead Agent: " + str(self.leadAgent),
                "Number of followers: " + str(self.numFollowers)]
