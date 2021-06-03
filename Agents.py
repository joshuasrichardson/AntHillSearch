""" Agent class. Stores 2D position and agent state """
import numpy as np
import pygame as pyg
from Constants import *

# TODO: set internal thresholds for each agent to switch out of an
#  existing state because of time-out. Replace magic numbers with
#  agent-specific thresholds. Use this to show how diversity is
#  necessary for increased resilience for the elements of autonomy paper


class Agent:

    def __init__(self, world):
        self.world = world  # The world the agent lives in
        self.siteObserveRectList = world.getSiteObserveRectList()  # List of rectangles of all the sites in the world
        self.siteList = world.getSiteList()  # List of all the sites in the world
        self.hubLocation = world.getHubPosition()  # Original home location
        self.hub = self.siteList[len(self.siteList) - 1]  # Original home that the agents are leaving

        self.pos = world.getHubPosition()  # Initial position
        self.agentHandle = pyg.image.load("copter.png")  # Image on screen representing the agent
        self.agentRect = self.agentHandle.get_rect()  # Rectangle around the agent to help track collisions
        self.agentRect.centerx = self.pos[0]  # Horizontal center of the agent
        self.agentRect.centery = self.pos[1]  # Vertical center of the agent
        self.speed = AGENT_SPEED*TIME_STEP  # Speed the agent moves on the screen
        self.target = self.hubLocation  # Either the hub or a site the agent is going to
        self.angle = np.arctan2(self.target[1]-self.pos[1], self.target[0]-self.pos[0])  # Angle the agent is moving
        self.angularVelocity = 0  # Speed the agent is changing direction

        self.state = AT_NEST  # Defines what the agent is currently doing
        self.color = AT_NEST_COLOR  # Color around the agent displaying their current state
        self.phase = EXPLORE_PHASE  # The current phase or level of commitment (explore, assess, canvas, commit)
        self.phaseColor = EXPLORE_PHASE_COLOR  # A color to represent the phase so it can be seen on the screen
        self.setState(AT_NEST, AT_NEST_COLOR, self.hubLocation)

        self.assignedSite = self.hub  # Site that the agent has discovered and is trying to get others to go see
        self.estimatedQuality = -1  # The agent's evaluation of the assigned site. Initially -1 so they can like any site better than the broken home they are coming from.
        self.assessmentThreshold = 1  # A number to influence how long an agent will assess a site. Should be longer for lower quality sites.

        self.knownSites = [self.hub]  # A list of sites that the agent has been to before
        self.siteToRecruitFrom = None  # The site the agent chooses to go recruit from when in the LEAD_FORWARD or TRANSPORT state
        self.leadAgent = None  # The agent that is leading this agent in the FOLLOW state or carrying it in the BEING_CARRIED state
        self.numFollowers = 0  # The number of agents following the current agent in LEAD_FORWARD or TANDEM_RUN state
        self.goingToRecruit = False  # Whether the agent is heading toward a site to recruit or not.
        self.comingWithFollowers = False  # Whether the agent is coming back toward a new site with followers or not.

    def setState(self, state, color, target):
        self.target = target
        if state == SEARCH:
            if self.state == SEARCH:
                # If not changing state, just update angle
                self.angularVelocity += np.random.normal(0, np.pi/200)
                self.angle = self.angle + self.angularVelocity*TIME_STEP
            else:
                # If changing state, set angle randomly
                # Random direction
                self.angularVelocity = 0
                self.angle = np.random.uniform(0, np.pi*2, 1)

        else:
            # All states aim for target location except for EXPLORE.
            # EXPLORE does a random walk, so set its angle in the if statement below
            self.angle = np.arctan2(self.target[1]-self.pos[1], self.target[0]-self.pos[0])
        self.state = state
        self.color = color

    def changeState(self, neighborList):
        if self.state == AT_NEST:
            self.setState(AT_NEST, AT_NEST_COLOR, self.assignedSite.getPosition())

            if self.shouldExplore():
                self.setState(SEARCH, SEARCH_COLOR, None)
                return

            if self.phase == ASSESS_PHASE:
                if self.isDoneAssessing():
                    self.acceptOrReject()
                    return

            if self.phase == CANVAS_PHASE:
                if self.shouldLead():
                    self.setState(LEAD_FORWARD, LEAD_FORWARD_COLOR, self.assignedSite.getPosition())
                    return

            if self.phase == COMMIT_PHASE:
                # Recruit, search, or follow
                self.transportOrReverseTandem()
                # TODO: search or follow and make recruit less than 100%

            for i in range(0, len(neighborList)):
                if neighborList[i].getState() == LEAD_FORWARD and neighborList[i].estimatedQuality > self.estimatedQuality:  # TODO: Should it be on their estimated quality or just that the sites are not the same site?
                    if self.shouldFollow():
                        self.tryFollowing(neighborList[i])
                        return

        if self.state == SEARCH:
            self.setState(SEARCH, SEARCH_COLOR, None)
            siteWithinRange = self.agentRect.collidelist(self.siteObserveRectList)
            # If agent finds a site within range then assess it

            if self.phase == EXPLORE_PHASE:
                if siteWithinRange != -1 and self.siteList[siteWithinRange] != self.hub:
                    self.knownSites.append(self.assignedSite)
                    self.assignSite(self.siteList[siteWithinRange])
                    self.setPhase(ASSESS_PHASE)
                    self.setState(AT_NEST, AT_NEST_COLOR, self.assignedSite.getPosition())
                # Else if timeout then switch to resting
                elif self.shouldReturnToNest():
                    self.setState(AT_NEST, AT_NEST_COLOR, self.assignedSite.getPosition())

            else:
                if siteWithinRange != -1 and self.siteList[siteWithinRange] != self.hub:
                    self.knownSites.append(self.assignedSite)
                    # If the site is better than the one they were assessing, they assess it instead.
                    if self.siteList[siteWithinRange].getQuality() > self.estimatedQuality:
                        self.assignSite(self.siteList[siteWithinRange])
                        self.setState(AT_NEST, AT_NEST_COLOR, self.assignedSite.getPosition())
                elif self.shouldReturnToNest():  # Else if timeout then go back to continue assessing the site
                    self.setState(AT_NEST, AT_NEST_COLOR, self.assignedSite.getPosition())
                elif self.phase == ASSESS_PHASE and self.isDoneAssessing():
                    self.acceptOrReject()

            for i in range(0, len(neighborList)):
                if neighborList[i].getState() == TRANSPORT:
                    self.getCarried(neighborList[i])
                    return

        if self.state == FOLLOW:
            if self.phase == COMMIT_PHASE:
                # TODO: Fix this if statement
                if self.shouldGetLost():
                    self.leadAgent = None
                    self.setState(SEARCH, SEARCH_COLOR, None)
                else:
                    self.updateFollowPosition()
                return

            if self.leadAgent.state == LEAD_FORWARD:
                if self.shouldGetLost():
                    self.leadAgent = None
                    self.setPhase(EXPLORE_PHASE)
                    self.setState(SEARCH, SEARCH_COLOR, None)
                else:
                    self.updateFollowPosition()
            else:
                # if they arrived at a nest:
                self.leadAgent = None
                self.setPhase(ASSESS_PHASE)
                self.setState(SEARCH, SEARCH_COLOR, None)

        if self.state == LEAD_FORWARD:
            # Choose a site to recruit from
            if self.goingToRecruit:  # if they are on the way to go recruit someone, they keep going until they get there. TODO: Can they get lost here? for now, no.
                self.setState(LEAD_FORWARD, LEAD_FORWARD_COLOR, self.siteToRecruitFrom.getPosition())
                if self.agentRect.collidepoint(self.siteToRecruitFrom.pos):  # If agent finds the old site, (or maybe this works with accidentally running into a site on the way)
                    self.goingToRecruit = False  # The agent is now going to head back to the new site
                    self.comingWithFollowers = True
                    self.setState(LEAD_FORWARD, LEAD_FORWARD_COLOR, self.assignedSite.getPosition())  # Go back to the new site with the new follower(s).
                return

            if self.comingWithFollowers:
                self.setState(LEAD_FORWARD, LEAD_FORWARD_COLOR, self.assignedSite.getPosition())
                if self.agentRect.collidepoint(self.assignedSite.pos):  # If they get to the assigned site
                    self.numFollowers = 0
                    self.comingWithFollowers = False
                    if self.quorumMet():  # If enough agents are at that site
                        self.setPhase(COMMIT_PHASE)  # Commit to the site
                        self.transportOrReverseTandem()
                    else:
                        self.setState(AT_NEST, AT_NEST_COLOR, self.assignedSite.getPosition())  # Just be at the site and decide what to do next in the AT_NEST state
                return

            self.siteToRecruitFrom = self.knownSites[np.random.randint(0, len(self.knownSites) - 1)]
            while self.siteToRecruitFrom == self.assignedSite:
                self.siteToRecruitFrom = self.knownSites[np.random.randint(0, len(self.knownSites) - 1)]
            self.goingToRecruit = True
            self.setState(LEAD_FORWARD, LEAD_FORWARD_COLOR, self.siteToRecruitFrom.getPosition())  # Go to their randomly chosen site to recruit.
            # TODO: Can they get lost here? I think so.

        if self.state == REVERSE_TANDEM:
            self.setState(REVERSE_TANDEM, REVERSE_TANDEM_COLOR, self.assignedSite.getPosition())
            # TODO: Lead back to a previous site to have them help transport
            self.setState(TRANSPORT, TRANSPORT_COLOR, self.assignedSite.getPosition())

        if self.state == TRANSPORT:
            # Choose a site to recruit from
            if self.goingToRecruit:  # if they are on the way to go recruit someone, they keep going until they get there. TODO: Can they get lost here? for now, no.
                self.setState(TRANSPORT, TRANSPORT_COLOR, self.siteToRecruitFrom.getPosition())
                if self.agentRect.collidepoint(self.siteToRecruitFrom.pos):  # If agent finds the old site, (or maybe this works with accidentally running into a site on the way)
                    self.goingToRecruit = False  # The agent is now going to head back to the new site
                    self.comingWithFollowers = True
                    self.setState(TRANSPORT, TRANSPORT_COLOR, self.assignedSite.getPosition())  # Go back to the new site with the new follower(s).
                return

            if self.comingWithFollowers:
                self.setState(TRANSPORT, TRANSPORT_COLOR, self.assignedSite.getPosition())
                if self.agentRect.collidepoint(self.assignedSite.pos):  # If they get to the assigned site
                    self.numFollowers = 0
                    self.comingWithFollowers = False
                    if self.shouldKeepTransporting():
                        self.transportOrReverseTandem()
                    else:
                        self.setState(SEARCH, SEARCH_COLOR, self.assignedSite.getPosition())  # Just be at the site and decide what to do next in the AT_NEST state
                return

            self.siteToRecruitFrom = self.knownSites[np.random.randint(0, len(self.knownSites) - 1)]
            while self.siteToRecruitFrom == self.assignedSite:
                self.siteToRecruitFrom = self.knownSites[np.random.randint(0, len(self.knownSites) - 1)]
            self.goingToRecruit = True
            self.setState(TRANSPORT, TRANSPORT_COLOR, self.siteToRecruitFrom.getPosition())  # Go to their randomly chosen site to recruit.
            # TODO: Can they get lost here? I think so.

        if self.state == CARRIED:
            self.setState(CARRIED, CARRIED_COLOR, self.leadAgent.pos)
            if self.leadAgent.state == TRANSPORT:
                self.updateFollowPosition()
            else:
                # if they arrived at a nest or the lead agent got lost and put them down or something:
                self.leadAgent = None
                self.setPhase(ASSESS_PHASE)
                self.setState(SEARCH, SEARCH_COLOR, None)

    def getState(self):
        return self.state

    def getColor(self):
        return self.color

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

    def tryFollowing(self, leader):
        if leader.numFollowers < MAX_FOLLOWERS:
            self.leadAgent = leader
            self.leadAgent.incrementFollowers()
            self.setState(FOLLOW, FOLLOW_COLOR, self.leadAgent.pos)

    def getCarried(self, transporter):
        if transporter.numFollowers < MAX_FOLLOWERS:
            self.leadAgent = transporter
            self.leadAgent.incrementFollowers()
            self.setState(CARRIED, CARRIED_COLOR, self.leadAgent.pos)

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
        surface.blit(self.agentHandle, self.agentRect)

        pyg.draw.ellipse(surface, self.color, self.agentRect, 4)
        pyg.draw.ellipse(surface, self.phaseColor, self.agentRect, 2)

        if self.assignedSite is None:
            img = self.world.myfont.render(str(self.estimatedQuality), True, self.color)
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
        self.assignedSite = site
        self.assignedSite.incrementCount()
        self.estimatedQuality = self.assignedSite.getQuality()  # TODO: Give agents different levels of quality-checking abilities. Maybe even have the estimatedQuality change as they have spent more time at a site to make it more accurate as time goes on.

    def shouldExplore(self):
        # TODO: decide good probability
        if self.assignedSite == self.hub:
            return np.random.exponential(SEARCH_EXPONENTIAL) > SEARCH_FROM_HUB_THRESHOLD * SEARCH_EXPONENTIAL
        return np.random.exponential(SEARCH_EXPONENTIAL) > SEARCH_THRESHOLD * SEARCH_EXPONENTIAL  # Make it more likely if they aren't at the hub.

    def shouldAssess(self):
        # TODO: decide good probability
        return np.random.exponential(ASSESS_EXPONENTIAL) > self.assessmentThreshold*ASSESS_EXPONENTIAL

    def isDoneAssessing(self):
        # TODO: decide good probability
        return np.random.exponential(LEAD_EXPONENTIAL) > LEAD_THRESHOLD*LEAD_EXPONENTIAL

    def acceptOrReject(self):
        if self.estimatedQuality > MIN_ACCEPT_VALUE:
            # If they determine the site is good enough after they've been there long enough,
            # they enter the canvasing phase and start recruiting others.
            self.setPhase(CANVAS_PHASE)
            self.setState(LEAD_FORWARD, LEAD_FORWARD_COLOR, self.assignedSite.getPosition())
        else:
            self.setPhase(EXPLORE_PHASE)
            self.setState(SEARCH, SEARCH_COLOR, None)

    def shouldReturnToNest(self):
        # TODO: decide good probability
        return np.random.exponential(AT_NEST_EXPONENTIAL) > AT_NEST_THRESHOLD * AT_NEST_EXPONENTIAL

    def shouldLead(self):
        # TODO: decide good probability. Maybe 100% for the first time in canvasing.
        return np.random.exponential(LEAD_EXPONENTIAL) > LEAD_THRESHOLD * LEAD_EXPONENTIAL

    def shouldFollow(self):
        # TODO: decide good probability
        return np.random.exponential(FOLLOW_EXPONENTIAL) > FOLLOW_THRESHOLD*FOLLOW_EXPONENTIAL

    def shouldGetLost(self):
        # TODO: decide good probability
        return np.random.exponential(GET_LOST_EXPONENTIAL) > GET_LOST_THRESHOLD*GET_LOST_EXPONENTIAL

    def quorumMet(self):
        return self.assignedSite.agentCount > QUORUM_SIZE

    def transportOrReverseTandem(self):
        if np.random.randint(0, 3) == 0:
            self.setState(REVERSE_TANDEM, REVERSE_TANDEM_COLOR, self.assignedSite.pos)
        else:
            self.setState(TRANSPORT, TRANSPORT_COLOR, self.assignedSite.pos)

    def shouldKeepTransporting(self):
        return np.random.randint(0, 2) == 0
