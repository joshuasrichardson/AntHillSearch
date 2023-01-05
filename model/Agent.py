import random

import Utils
from display.Display import getDestinationMarker
from config import Config
from Constants import *
from display.simulation import FogDisplay
from display.simulation.AgentDisplay import getAgentImage
from model.phases.AssessPhase import AssessPhase
from model.phases.ConvergedPhase import ConvergedPhase
from model.phases.ExplorePhase import ExplorePhase
from model.states.AtNestState import AtNestState
from numpy import random, pi, cos, sin, sqrt, square


class Agent:
    """ Represents an agent that works to find a new nest when the old one is broken by going through different
    phases and states"""

    def __init__(self, world, startingAssignment, startingPosition, speed, decisiveness, navSkills, estAccuracy):
        """ world - the world the agent lives in
        startingAssignment - the hub or site the agent will start out assigned to
        startingPosition - x, y coordinates of the position where the agent starts
        speed - proportional to how far the agent moves each iteration
        decisiveness - proportional to how quickly the agent can judge sites
        navSkills - inversely proportional to how easily the agent gets lost
        estAccuracy - proportional to how closely the agent can estimate the quality of a site """
        self.world = world  # The colony the agent lives in
        self.hub = self.world.getClosestHub(startingPosition)

        self.prevPos = list(startingPosition)  # Where the agent was during the last iteration
        self.pos = [startingPosition[0] + random.choice([-1, 1]), startingPosition[1] + random.choice([-1, 1])]   # Initial position
        self.lastSeenPos = self.pos  # Where the agent was last seen
        self.path = []  # A list of the positions the agent has recently come from
        self.agentHandle = getAgentImage(self.pos)  # Image on screen representing the agent
        self.agentRect = self.agentHandle.get_rect()  # Rectangle around the agent to help track collisions
        self.agentRect.centerx = self.pos[0]  # Horizontal center of the agent
        self.agentRect.centery = self.pos[1]  # Vertical center of the agent
        self.prevRect = self.agentHandle.get_rect()  # Rectangle around the agent at previous position
        self.prevRect.centerx = self.pos[0]  # Horizontal center of the agent at previous position
        self.prevRect.centery = self.pos[1]  # Vertical center of the agent at previous position

        self.speed = speed  # Speed the agent moves on the screen
        self.uncommittedSpeed = self.speed  # The speed of the agents outside the committed phase
        self.committedSpeed = self.speed * Config.COMMIT_SPEED_FACTOR  # The speed of the agents in the committed phase
        self.decisiveness = decisiveness  # Influences how quickly an agent can assess
        self.navigationSkills = navSkills  # Influences how likely an agent is to get lost
        self.estimationAccuracy = estAccuracy  # How far off an agent's estimate of the quality of a site will be on average.
        self.assessmentThreshold = 5  # A number to influence how long an agent will assess a site. Should be longer for lower quality sites.
        self.speedCoefficient = 1  # The number multiplied my the agent's original speed to get its current speed

        self.target = list(startingPosition)  # The position the agent is going to
        self.angle = random.uniform(0, 2 * pi)  # Angle the agent is moving
        self.placesToAvoid = []  # A list of points that the agent should stay away from
        # self.obstaclesToAvoid = []  # A list of obstacles the agent cannot walk over
        self.recentlySeenPredatorPositions = []

        self.state = None  # The current state of the agent such as AT_NEST, SEARCH, FOLLOW, etc.
        self.phase = ExplorePhase()  # The current phase or level of commitment (explore, assess, canvas, commit)
        self.lastKnownPhaseColor = self.getPhaseColor()  # The color of the phase of the agent when they left the hub

        self.assignedSite = startingAssignment  # Site that the agent has discovered and is trying to get others to go see
        self.estimatedQuality = -1  # The agent's evaluation of the assigned site. Initially -1 so they can like any site better than the broken home they are coming from.
        self.estimatedAgentCount = self.getHub().agentCount  # The number of agents the agent thinks are assigned to their assigned site.
        self.estimatedRadius = self.getHub().getRadius()  # The agent's estimate of the radius of their assigned site
        self.estimatedSitePosition = self.assignedSite.getPosition()  # An estimate of where the agent thinks their site is
        self.prevReportedSite = startingAssignment  # The site the agent was assigned to last time they were at the hub
        self.newReport = True  # Whether the agent has new estimates to report

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
        self.isMainSelected = False  # Whether the agent is the one with its information shown
        self.marker = None  # A marker to be drawn on the screen representing an action the agent will perform
        self.checkPoints = []  # A list of places the agent has to go to on the way to their GO destination
        self.eraseFogCommands = []  # A list of eraseFog methods and agentRects used to clear fog after an agent has returned to the hub

        self.angleBeforeObstacle = self.angle  # Agent's angle when they collide with an obstacle

    def setState(self, state):
        self.state = state

    def doStateActions(self, neighborList):
        if self.state.executeCommands():
            return
        self.state.doStateActions(neighborList)

    def getStateNumber(self):
        return self.state.stateNumber

    def setAngle(self, angle):
        self.angle = angle

    def setTarget(self, target):
        self.target = target
        if self.isMainSelected and self.target is not None:
            self.marker = getDestinationMarker(self.target)

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
        self.prevPos = self.pos
        self.prevRect.centerx = self.pos[0]
        self.prevRect.centery = self.pos[1]
        self.agentRect.centerx = x
        self.agentRect.centery = y
        self.pos = list([x, y])
        if not Config.DRAW_FAR_AGENTS and self.isClose(self.hub.getPosition(), Config.HUB_OBSERVE_DIST):
            self.lastSeenPos = self.pos
            self.lastKnownPhaseColor = self.getPhaseColor()

    def moveForward(self):
        if self.getPhaseNumber() == CONVERGED:
            self.setPosition(self.assignedSite.getPosition()[0], self.assignedSite.getPosition()[1])
        else:
            x, y = Utils.getNextPosition(self.pos, self.speed, self.angle)
            self.setPosition(x, y)

    def updateFollowPosition(self):
        """ Updates the agent's position to be just behind their lead agent """
        self.agentRect.centerx = int(round(float(self.leadAgent.pos[0]) - self.leadAgent.speed * cos(self.leadAgent.angle)))
        self.agentRect.centery = int(round(float(self.leadAgent.pos[1]) - self.leadAgent.speed * sin(self.leadAgent.angle)))
        self.pos = list([self.agentRect.centerx, self.agentRect.centery])

    def getAssignedSitePosition(self):
        if Config.FIND_SITES_EASILY:
            return self.assignedSite.getPosition()  # Return the actual position of the site
        else:
            return self.estimatedSitePosition  # Return where they last saw the site (it could have moved from there)

    def getRecruitSitePosition(self):
        if Config.FIND_SITES_EASILY:
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
        if Config.DRAW_FAR_AGENTS:
            FogDisplay.eraseFog(self.world.fog, self.pos)
        elif self.isClose(self.getHub().getPosition(), Config.HUB_OBSERVE_DIST) and not Config.DRAW_FAR_AGENTS:
            for command in self.eraseFogCommands:
                command[0](*command[1])  # Execute each of the eraseFogCommands that have been appended since the last visit to the hub
            self.eraseFogCommands = []
        elif not Config.DRAW_FAR_AGENTS:  # If they are not by the hub
            self.eraseFogCommands.append([FogDisplay.eraseFog, [self.world.fog, self.pos.copy()]])  # Add their current position and erase fog command to a list to be executed when they get back to the hub.

    def getHub(self):
        return self.hub

    def getPrevRect(self):
        return self.prevRect

    def getRect(self):
        return self.agentRect

    def incrementFollowers(self):
        self.numFollowers += 1

    def isCloseToHub(self):
        return self.isClose(self.getHub().getPosition(), Config.HUB_OBSERVE_DIST)

    def isCloseToASite(self):
        """ Returns whether the agent is next to a site or not """
        for site in self.world.siteList:
            if self.isClose(site.getPosition(), site.getRadius() * 2):
                return True
        return False

    def getNearbyPlaceToAvoid(self):
        closePositions = []
        for pos in self.placesToAvoid:
            if self.isClose(pos, Config.MIN_AVOID_DIST):
                closePositions.append(pos)
        return closePositions

    def isClose(self, position, distance):
        """ Returns a boolean representing whether the agent is within the specified distance of the specified position """
        return Utils.isClose(self.pos, position, distance)

    def isTooFarAway(self, site):
        """ Returns a boolean representing whether the agent is outside their searching area """
        # a ^ 2 + b ^ 2 = c ^ 2
        dist = sqrt(square(abs(self.pos[0] - site.getPosition()[0])) + square(abs(self.pos[1] - site.getPosition()[1])))
        return dist > Config.MAX_SEARCH_DIST

    def estimateQuality(self, site):
        """ Returns an estimate of a site quality that is within estimationAccuracy units from the actual quality """
        if site.quality == -1:
            return -1
        self.newReport = True
        return site.getQuality() + (self.estimationAccuracy if random.randint(0, 2) == 1 else -self.estimationAccuracy)

    def estimateRadius(self, site):
        """ Returns an estimate of a site radius that is within estimationAccuracy/4 pixels from the actual radius """
        if site.quality == -1:
            return site.getRadius()
        self.newReport = True
        estimate = site.getRadius() + ((self.estimationAccuracy / 4) if random.randint(0, 2) == 1 else (-(self.estimationAccuracy / 4)))
        if estimate <= 0:  # Main radius cannot be negative or zero.
            estimate = 1
        return estimate

    def addToKnownSites(self, site):
        """ Lets the agent know about the site so they can recruit from it (or to it if they think it's the best) """
        if not self.knownSites.__contains__(site) and site is not None:
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
        if site is None:
            return
        if self.assignedSite is not None:
            self.assignedSite.decrementCount(self.getHubIndex())
        if site is not self.assignedSite:  # If the site they are assigned to is not the one they came from
            self.setPhase(AssessPhase())  # Start assessing it, and estimate its values
            self.estimatedQuality = self.estimateQuality(site)
            self.estimatedRadius = self.estimateRadius(site)
            self.estimatedSitePosition = self.estimateSitePosition(site)
        else:
            self.estimateSitePositionMoreAccurately()
        self.assignedSite = site
        self.assignedSite.incrementCount(self.getHubIndex())
        # Take longer to assess lower-quality sites
        self.assessmentThreshold = Config.MAX_ASSESS_THRESHOLD - (self.estimatedQuality / Config.ASSESS_DIVIDEND)

    def estimateSitePosition(self, site):
        """ Returns an estimate of a site position that is within estimationAccuracy * 2 pixels from the actual position """
        if site is self.getHub():
            estimatedSitePosition = self.getHub().getPosition()
        else:
            self.newReport = True
            estimatedSitePosition = site.getPosition().copy()
            estimatedSitePosition[0] = site.getPosition()[0] + random.randint(int(-20 / self.navigationSkills), int(20 / self.navigationSkills))
            estimatedSitePosition[1] = site.getPosition()[1] + random.randint(int(-20 / self.navigationSkills), int(20 / self.navigationSkills))
        return estimatedSitePosition

    def estimateSitePositionMoreAccurately(self):
        """ Returns an estimate of a site position that is closer than the agent's last estimate """
        if not self.newReport:
            if self.assignedSite is not self.getHub():
                self.newReport = True
            sitePos = self.assignedSite.getPosition()
            if self.estimatedSitePosition[0] != sitePos[0]:
                self.estimatedSitePosition[0] = (self.estimatedSitePosition[0] + sitePos[0]) / 2
            if self.estimatedSitePosition[1] != sitePos[1]:
                self.estimatedSitePosition[1] = (self.estimatedSitePosition[1] + sitePos[1]) / 2

    def avoid(self, pos):
        if pos is not None and len(self.getNearbyPlaceToAvoid()) == 0:
            self.placesToAvoid.append(pos)
            self.recentlySeenPredatorPositions.append(pos)
            if len(self.placesToAvoid) > Config.MAX_NUM_AVOIDS:
                self.placesToAvoid.pop(0)
            if self.isClose(pos, Config.MIN_AVOID_DIST):
                self.escape([pos])
            self.forgetDangerousSites(pos)

    def escape(self, positions):
        from model.states.EscapeState import EscapeState
        stateNumber = self.state.prevStateNum if self.getStateNumber() == ESCAPE else self.getStateNumber()
        self.setState(EscapeState(self, stateNumber, positions))

    def stopAvoiding(self, index):
        if len(self.placesToAvoid) > index:
            self.placesToAvoid.pop(index)

    def forgetDangerousSites(self, pos):
        for site in self.knownSites:
            if self.world.isClose(pos, site.getPosition(), Config.MIN_AVOID_DIST):
                self.removeKnownSite(site)

    def getAssignedSiteIndex(self):
        """ Returns the agent's assigned site's position in the world site list """
        return self.world.getSiteIndex(self.assignedSite)

    def isDoneAssessing(self):
        """ Returns whether the agent is ready to make a decision to accept or reject their assigned site """
        return random.exponential() * self.decisiveness > self.assessmentThreshold

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

    def quorumMet(self, neighborList):
        """ Returns whether the agent met enough other agents at their assigned site to go into the commit phase """
        return (len(neighborList) > self.world.initialHubAgentCounts[self.getHubIndex()] / Config.QUORUM_DIVIDEND or
                self.neighborIsCommitted(neighborList)) and not self.assignedSite.isHub()

    @staticmethod
    def neighborIsCommitted(neighborList):
        for neighbor in neighborList:
            if neighbor.getStateNumber() == COMMIT:
                return True
        return False

    def tryConverging(self):
        if self.assignedSite.agentCount > self.world.initialHubAgentCounts[self.getHubIndex()] * Config.CONVERGENCE_FRACTION \
                and not self.assignedSite.isHub():
            self.setPhase(ConvergedPhase())
            self.setState(AtNestState(self))
            self.assignedSite.chosen = True
            return True
        return False

    def shouldSearch(self, siteWithinRange):
        """ Returns whether the agent is ready to go out searching the area """
        if siteWithinRange == -1:
            # When self.findAssignedSiteEasily is False, this will be False everytime.
            # When self.findAssignedSiteEasily is True, this will only be True if the agent is
            # close to where their site was before it moved.
            if self.isClose(self.getAssignedSitePosition(), self.assignedSite.getRadius()):
                self.removeKnownSite(self.assignedSite)
                return True
        if not self.world.siteList[siteWithinRange] is self.assignedSite:
            # Mainy should get back to their site before they go out searching again.
            return False
        if self.assignedSite == self.getHub():
            return random.exponential() > Config.SEARCH_FROM_HUB_THRESHOLD
        return random.exponential() > Config.SEARCH_THRESHOLD  # Make it more likely to search if they aren't at the hub.

    @staticmethod
    def shouldReturnToNest():
        """ Returns whether the agent is ready to go back to their assigned site """
        return random.exponential() > Config.AT_NEST_THRESHOLD

    @staticmethod
    def shouldRecruit():
        """ Returns whether the agent is ready to go recruit to their assigned site """
        return random.exponential() > Config.LEAD_THRESHOLD

    @staticmethod
    def shouldKeepTransporting():
        """ Returns whether the agent should continue recruiting to their assigned site """
        return random.randint(0, 3) != 0

    @staticmethod
    def shouldFollow():
        """ Returns whether the agent should follow a canvasing or committed agent """
        return random.exponential() > Config.FOLLOW_THRESHOLD

    @staticmethod
    def shouldFollowDance():
        """ Returns whether the agent should go to the site of a dancing agent """
        return random.exponential() > Config.FOLLOW_DANCE_THRESHOLD

    @staticmethod
    def doneRecruiting():
        """ Returns whether the agent is ready to stop recruiting and rest """
        return random.exponential() > Config.LEAD_THRESHOLD

    def shouldGetLost(self):
        """ Returns whether the agent will lose their way """
        return random.exponential() > self.navigationSkills * Config.GET_LOST_THRESHOLD

    def transportOrReverseTandem(self, state):
        """ Randomly chooses between switching to reverse tandem and transport states with a higher chance of going to transport """
        if random.randint(0, 3) == 0:
            from model.states.ReverseTandemState import ReverseTandemState
            state.setState(ReverseTandemState(self), self.getAssignedSitePosition())
        else:
            from model.states.TransportState import TransportState
            state.setState(TransportState(self), self.getAssignedSitePosition())

    def select(self):
        """ Selects the agent to allow various user interactions """
        self.isSelected = True

    def mainSelect(self):
        """ Selects the agent as the main agent selected so that more of their information is shown """
        self.isMainSelected = True
        if self.target is not None:
            self.marker = getDestinationMarker(self.target)

    def unselect(self):
        """ Unselects the agent to prevent various user interactions """
        self.isSelected = False
        self.isMainSelected = False
        self.marker = None

    def unMainSelect(self):
        """ Stops displaying extra information about the agent """
        self.isMainSelected = False
        self.marker = None

    def die(self):
        if self.getStateNumber() != DEAD:
            from model.states.DeadState import DeadState
            self.setState(DeadState(self))  # This will stop the ant from moving etc.
            self.assignedSite.decrementCount(self.getHubIndex())  # They no longer count toward converging to a site
            self.assignedSite = None
            self.world.incrementDeadAgents(self.getHubIndex())  # Need to keep track of how many died so the number needed to converge goes down.
            self.checkPoints = []
            self.placesToAvoid = []
            self.setTarget(None)
