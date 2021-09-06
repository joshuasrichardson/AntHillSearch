import random

import numpy as np

from Constants import *
from display import SiteDisplay, WorldDisplay
from display.Display import getAgentImage
from model.builder import AgentSettings
from model.phases.AssessPhase import AssessPhase
from model.phases.ExplorePhase import ExplorePhase


class Agent:
    """ Represents an agent that works to find a new nest when the old one is broken by going through different
    phases and states"""

    def __init__(self, world, startingAssignment, startingPosition, speed, decisiveness, navSkills, estAccuracy):
        self.world = world  # The colony the agent lives in
        self.hub = self.world.getClosestHub(startingPosition)

        self.prevPos = list(startingPosition)  # Initial position
        self.pos = [startingPosition[0] + np.random.choice([-1, 1]), startingPosition[1] + np.random.choice([-1, 1])]   # Initial position
        self.path = []  # A list of the positions the agent has recently come from
        self.agentHandle = getAgentImage(self.pos)  # Image on screen representing the agent
        self.agentRect = self.agentHandle.get_rect()  # Rectangle around the agent to help track collisions
        self.agentRect.centerx = self.pos[0]  # Horizontal center of the agent
        self.agentRect.centery = self.pos[1]  # Vertical center of the agent

        self.speed = speed  # Speed the agent moves on the screen
        self.uncommittedSpeed = self.speed  # The speed of the agents outside the committed phase
        self.committedSpeed = self.speed * AgentSettings.commitSpeedFactor  # The speed of the agents in the committed phase
        self.decisiveness = decisiveness  # Influences how quickly an agent can assess
        self.navigationSkills = navSkills  # Influences how likely an agent is to get lost
        self.estimationAccuracy = estAccuracy  # How far off an agent's estimate of the quality of a site will be on average.
        # self.laziness = laziness  # How unwilling the agent is to change sites, even if the new site is better.
        self.assessmentThreshold = 5  # A number to influence how long an agent will assess a site. Should be longer for lower quality sites.
        self.speedCoefficient = 1  # The number multiplied my the agent's original speed to get its current speed

        self.target = list(startingPosition)  # The position the agent is going to
        self.angle = np.random.uniform(0, np.pi, 1)  # Angle the agent is moving

        self.state = None  # The current state of the agent such as AT_NEST, SEARCH, FOLLOW, etc.
        self.phase = ExplorePhase()  # The current phase or level of commitment (explore, assess, canvas, commit)

        self.assignedSite = startingAssignment  # Site that the agent has discovered and is trying to get others to go see
        self.estimatedQuality = -1  # The agent's evaluation of the assigned site. Initially -1 so they can like any site better than the broken home they are coming from.
        self.estimatedAgentCount = self.getHub().agentCount  # The number of agents the agent thinks are assigned to their assigned site.
        self.estimatedRadius = self.getHub().radius  # The agent's estimate of the radius of their assigned site
        self.estimatedSitePosition = self.assignedSite.getPosition()  # An estimate of where the agent thinks their site is

        self.siteInRangeIndex = self.getHubIndex()
        self.knownSites = [self.getHub()]  # A list of sites that the agent has been to before
        self.knownSitesPositions = [self.getHub().getPosition()]  # A list of positions of sites the agent has found
        self.addToKnownSites(startingAssignment)
        self.recruitSite = None  # The site the agent chooses to go recruit from when in the LEAD_FORWARD or TRANSPORT state
        self.recruitSiteLastKnownPos = None  # The position of the agent's recruitSite when they last visited it
        self.leadAgent = None  # The agent that is leading this agent in the FOLLOW state or carrying it in the BEING_CARRIED state
        self.numFollowers = 0  # The number of agents following the current agent in LEAD_FORWARD or TANDEM_RUN state
        self.goingToRecruit = False  # Whether the agent is heading toward a site to recruit or not
        self.comingWithFollowers = False  # Whether the agent is coming back toward a new site with followers or not

        self.isSelected = False  # Whether the user clicked on the agent or its site most recently
        self.isTheSelected = False  # Whether the agent is the one with its information shown
        self.marker = None  # A marker to be drawn on the screen representing an action the agent will perform
        self.eraseFogCommands = []  # A list of eraseFog methods and agentRects used to clear fog after an agent has returned to the hub

    def setState(self, state):
        self.state = state

    def changeState(self, neighborList):
        if self.state.executeCommand():
            return
        self.state.changeState(neighborList)

    def getState(self):
        return self.state.state

    def setAngle(self, angle):
        self.angle = angle

    def getStateColor(self):
        return self.state.getColor()

    def setPhase(self, phase):
        """ Sets the phase to the specified phase and updates the speed accordingly
        (Committed agents are faster than agents in other phases) """
        self.phase = phase
        self.speed = phase.getSpeed(self.uncommittedSpeed, self.committedSpeed, self.speedCoefficient)

    def getPhaseColor(self):
        return self.phase.getColor()

    def getPhaseNumber(self):
        """ Returns a number representing the agent's phase instead of the actual phase object """
        return self.phase.getNumber()

    def getAngle(self):
        return self.angle

    def getPosition(self):
        self.pos = list([self.agentRect.centerx, self.agentRect.centery])
        return self.pos

    def setPosition(self, x, y):
        self.agentRect.centerx = x
        self.agentRect.centery = y
        self.pos = list([x, y])

    def updatePosition(self, position=None):
        self.prevPos = self.pos
        if position is None:  # If the position is not specified, continue moving along the same path as before
            self.agentRect.centerx = int(np.round(float(self.pos[0]) + self.speed * np.cos(self.angle)))
            self.agentRect.centery = int(np.round(float(self.pos[1]) + self.speed * np.sin(self.angle)))
        else:  # Else, update the position to match the parameter
            self.agentRect.centerx = position[0]
            self.agentRect.centery = position[1]
        self.pos = list([self.agentRect.centerx, self.agentRect.centery])

    def updateFollowPosition(self):
        """ Updates the agent's position to be just behind their lead agent """
        self.agentRect.centerx = int(np.round(float(self.leadAgent.pos[0]) - self.leadAgent.speed * np.cos(self.leadAgent.angle)))
        self.agentRect.centery = int(np.round(float(self.leadAgent.pos[1]) - self.leadAgent.speed * np.sin(self.leadAgent.angle)))
        self.pos = list([self.agentRect.centerx, self.agentRect.centery])

    def getAssignedSitePosition(self):
        if AgentSettings.findAssignedSiteEasily:
            return self.assignedSite.getPosition()  # Return the actual position of the site
        else:
            return self.estimatedSitePosition  # Return where they last saw the site (it could have moved from there)

    def getRecruitSitePosition(self):
        if AgentSettings.findAssignedSiteEasily:
            return self.recruitSite.getPosition()  # Return the actual position of the site
        else:
            return self.recruitSiteLastKnownPos  # Return where they last saw the site (it could have moved from there)

    def updatePath(self):
        """ Adds the agent's current position to their path and erases the oldest position if the path is getting long """
        self.path.append(self.pos)
        if len(self.path) > 50:
            self.path.pop(0)

    def clearFog(self):
        """ Erases fog rectangles from the screen where the agent has been """
        if SiteDisplay.knowSitePosAtStart:
            WorldDisplay.eraseFog(self.pos)
        elif self.isClose(self.getHub().getPosition(), self.getHub().radius + HUB_OBSERVE_DIST) and \
                not SiteDisplay.knowSitePosAtStart:
            for command in self.eraseFogCommands:
                command[0](command[1])  # Execute each of the eraseFogCommands that have been appended since the last visit to the hub
            self.eraseFogCommands = []
        elif not SiteDisplay.knowSitePosAtStart:  # If they are not by the hub
            self.eraseFogCommands.append([WorldDisplay.eraseFog, self.pos.copy()])  # Add their current position and erase fog command to a list to be executed when they get back to the hub.

    def getHub(self):
        return self.hub

    def getAgentRect(self):
        return self.agentRect

    def incrementFollowers(self):
        self.numFollowers += 1

    def isCloseToASite(self):
        """ Returns whether the agent is next to a site or not """
        for site in self.world.siteList:
            if self.isClose(site.getPosition(), site.radius * 2):
                return True
        return False

    def isClose(self, position, distance):
        """ Returns a boolean representing whether the agent is within the specified distance of the specified position """
        dist = np.sqrt(np.square(abs(self.pos[0] - position[0])) + np.square(abs(self.pos[1] - position[1])))
        return dist <= distance

    def isTooFarAway(self, site):
        """ Returns a boolean representing whether the agent is outside their searching area """
        # a ^ 2 + b ^ 2 = c ^ 2
        dist = np.sqrt(np.square(abs(self.pos[0] - site.getPosition()[0])) + np.square(abs(self.pos[1] - site.getPosition()[1])))
        return dist > AgentSettings.maxSearchDistance

    def estimateQuality(self, site):
        """ Returns an estimate of a site quality that is within estimationAccuracy units from the actual quality """
        if site.quality == -1:
            return -1
        return site.getQuality() + (self.estimationAccuracy if random.randint(0, 2) == 1 else -self.estimationAccuracy)

    def estimateAgentCount(self, site):
        self.estimatedAgentCount = site.agentCount  # TODO: Actually estimate the count
        return self.estimatedAgentCount

    def estimateRadius(self, site):
        """ Returns an estimate of a site radius that is within estimationAccuracy/4 pixels from the actual radius """
        if site.quality == -1:
            return site.radius
        estimate = site.radius + ((self.estimationAccuracy / 4) if random.randint(0, 2) == 1 else (-(self.estimationAccuracy / 4)))
        if estimate <= 0:  # The radius cannot be negative or zero.
            estimate = 1
        return estimate

    def addToKnownSites(self, site):
        """ Lets the agent know about the site so they can recruit from it (or to it if they think it's the best) """
        if not self.knownSites.__contains__(site):
            self.knownSites.append(site)
            self.knownSitesPositions.append(site.getPosition())

    def removeKnownSite(self, site):
        """ Makes the agent forget about a site (in situations like when a site is deleted or moved) """
        if self.knownSites.__contains__(site):
            if site is self.assignedSite:
                self.assignSite(self.getHub())
            index = self.knownSites.index(site)
            self.knownSites.remove(site)
            self.knownSitesPositions.pop(index)

    def removeKnownSite2(self, index):
        """ Removes the known position of a site. """
        self.knownSitesPositions.pop(index)

    def assignSite(self, site):
        """ Sets the site the agent will be assessing or recruiting to """
        if self.assignedSite is not None:
            self.assignedSite.decrementCount(self.getHubIndex())
        if site.getPosition()[0] != self.assignedSite.getPosition()[0] and\
                site.getPosition()[1] != self.assignedSite.getPosition()[1] and\
                site is not self.assignedSite:  # If the site they are assigned to is not the one they came from
            self.setPhase(AssessPhase())  # Start assessing it, and estimate its values
            self.estimatedQuality = self.estimateQuality(site)
            self.estimatedAgentCount = self.estimateAgentCount(site)
            self.estimatedRadius = self.estimateRadius(site)
            self.estimatedSitePosition = self.estimateSitePosition(site)
        else:
            self.estimateSitePositionMoreAccurately()
        self.assignedSite = site
        self.assignedSite.incrementCount(self.getHubIndex())
        # Take longer to assess lower-quality sites
        self.assessmentThreshold = MAX_ASSESS_THRESHOLD - (self.estimatedQuality / ASSESS_DIVIDEND)

    def estimateSitePosition(self, site):
        """ Returns an estimate of a site position that is within estimationAccuracy * 2 pixels from the actual position """
        if site is self.getHub():
            estimatedSitePosition = self.getHub().getPosition()
        else:
            estimatedSitePosition = site.getPosition().copy()
            estimatedSitePosition[0] = site.getPosition()[0] + random.randint(int(-20 / self.navigationSkills), int(20 / self.navigationSkills))
            estimatedSitePosition[1] = site.getPosition()[1] + random.randint(int(-20 / self.navigationSkills), int(20 / self.navigationSkills))
        return estimatedSitePosition

    def estimateSitePositionMoreAccurately(self):
        """ Returns an estimate of a site position that is closer than the agent's last estimate """
        sitePos = self.assignedSite.getPosition()
        if self.estimatedSitePosition[0] != sitePos[0]:
            self.estimatedSitePosition[0] = (self.estimatedSitePosition[0] + sitePos[0]) / 2
        if self.estimatedSitePosition[1] != sitePos[1]:
            self.estimatedSitePosition[1] = (self.estimatedSitePosition[1] + sitePos[1]) / 2

    def getAssignedSiteIndex(self):
        """ Returns the agent's assigned site's position in the world site list """
        return self.world.getSiteIndex(self.assignedSite)

    def isDoneAssessing(self):
        """ Returns whether the agent is ready to make a decision to accept or reject their assigned site """
        return np.random.exponential() * self.decisiveness > self.assessmentThreshold

    def getHubIndex(self):
        return self.world.getHubs().index(self.getHub())

    @staticmethod
    def checkLeadAgent(agent, stateNum):
        if stateNum == FOLLOW:
            leadAgent = agent.world.getClosestAgentWithState(agent.getPosition(), [REVERSE_TANDEM, LEAD_FORWARD, TRANSPORT])
            if leadAgent is None:
                return False
            else:
                agent.leadAgent = leadAgent
        elif stateNum == CARRIED:
            leadAgent = agent.world.getClosestAgentWithState(agent.getPosition(), [TRANSPORT])
            if leadAgent is None:
                return False
            else:
                agent.leadAgent = leadAgent
        return True

    def quorumMet(self, numNeighbors):
        """ Returns whether the agent met enough other agents at their assigned site to go into the commit phase """
        return numNeighbors > self.world.initialHubAgentCounts[self.getHubIndex()] / QUORUM_DIVIDEND

    def tryConverging(self):
        if self.assignedSite.agentCount > self.world.initialHubAgentCounts[self.getHubIndex()] * CONVERGENCE_FRACTION:
            from model.states.ConvergedState import ConvergedState
            self.state.setState(ConvergedState(self), self.getAssignedSitePosition())
            return True
        return False

    def shouldSearch(self, siteWithinRange):
        """ Returns whether the agent is ready to go out searching the area """
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
        """ Returns whether the agent is ready to go back to their assigned site """
        return np.random.exponential() > AT_NEST_THRESHOLD

    @staticmethod
    def shouldRecruit():
        """ Returns whether the agent is ready to go recruit to their assigned site """
        return np.random.exponential() > LEAD_THRESHOLD

    @staticmethod
    def shouldKeepTransporting():
        """ Returns whether the agent should continue recruiting to their assigned site """
        return np.random.randint(0, 3) != 0

    @staticmethod
    def shouldFollow():
        """ Returns whether the agent should follow a canvasing or committed agent """
        return np.random.exponential() > FOLLOW_THRESHOLD

    def shouldGetLost(self):
        """ Returns whether the agent will lose their way """
        return np.random.exponential() > self.navigationSkills * GET_LOST_THRESHOLD

    def transportOrReverseTandem(self, state):
        """ Randomly chooses between switching to reverse tandem and transport states with a higher chance of going to transport """
        if np.random.randint(0, 3) == 0:
            from model.states.ReverseTandemState import ReverseTandemState
            state.setState(ReverseTandemState(self), self.getAssignedSitePosition())
        else:
            from model.states.TransportState import TransportState
            state.setState(TransportState(self), self.getAssignedSitePosition())

    def select(self):
        """ Selects the agent to allow various user interactions """
        self.isSelected = True

    def unselect(self):
        """ Unselects the agent to prevent various user interactions """
        self.isSelected = False
        self.isTheSelected = False
        self.marker = None
