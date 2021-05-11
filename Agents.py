""" Agent class. Stores 2D position and agent state """
import numpy as np
import pygame as pyg
from Constants import *

# TODO: set internal thresholds for each agent to switch out of a
# existing state because of time-out. Replace magic numbers with
# agent-specific thresholds. Use this to show how diversity is
# necessary for increased resilience for the elements of autonomy paper


class Agent:
    def __init__(self, world):
        """randomly places agent at a 2D location and assigns it
        a random state"""
        self.world = world  # The world the agent lives in
        self.pos = world.getHubPosition()  # Initial position
        self.siteObserveRectList = world.getSiteObserveRectList()  # List of rectangles of all the sites in the world
        self.siteList = world.getSiteList()  # List of all the sites in the world
        self.hubLocation = world.getHubPosition()  # Original home location
        self.hub = self.siteList[len(self.siteList) - 1]
        self.agentHandle = pyg.image.load("copter.png")  # Image on screen representing the agent
        self.agentRect = self.agentHandle.get_rect()  # Rectangle around the agent
        self.agentRect.centerx = self.pos[0]  # Horizontal center of the agent
        self.agentRect.centery = self.pos[1]  # Vertical center of the agent
        self.speed = AGENT_SPEED*TIME_STEP  # Speed the agent moves on the screen
        self.state = None  # Defines what the agent is currently doing
        self.phase = EXPLORE_PHASE             # """JOSHUA"""
        self.phaseColor = EXPLORE_PHASE_COLOR  # """JOSHUA"""
        self.setState(AT_NEST, REST_COLOR, self.hubLocation)
        self.angularVelocity = 0  # Speed the agent is changing direction
        self.assignedSite = None  # Site that the agent has discovered and is trying to get others to go see
        self.estimatedQuality = None  # The agent's evaluation of the assigned site
        self.danceTimeFactor = None  # A number to help decide how long an agent dances
        self.ADPX = 0  # Number of neighbor agents Assessing, Dancing, Piping, or Committed for site X
        self.RTFX_agents = 0  # Agents around this agent in the hub that are ready to fly
        self.piping_agents = 0  # Number of agents around this agent that are piping
        self.target = self.hubLocation  # Either the hub or a site the agent is going to
        self.angle = np.arctan2(self.target[1]-self.pos[1], self.target[0]-self.pos[0])  # Angle the agent is moving
        self.color = REST_COLOR  # Color around the agent displaying their current state

        self.knownSites = [self.hub]                   # """JOSHUA"""
        self.siteToRecruitFrom = None
        self.leadAgent = None  # The agent that is leading this agent in the FOLLOW state or carrying it in the BEING_CARRIED state
        self.numFollowers = 0
        self.goingToRecruit = False  # Whether the agent is in the process of flying toward a site to recruit or not.
        self.comingWithFollowers = False  # Whether the agent is coming back toward a new site with followers or not.

    def setState(self, state, color, target):
        self.target = target
        if state == EXPLORE:
            if self.state == EXPLORE:
                # If not changing state, just update angle
                self.angularVelocity += np.random.normal(0, np.pi/200)  # TODO: Magic number
                self.angle = self.angle + self.angularVelocity*TIME_STEP
            else:
                # If changing state, set angle randomly
                self.state = EXPLORE
                self.color = EXPLORE_COLOR
                self.target = target  # TODO: may be redundant.
                # Random direction
                self.angle = np.random.uniform(0, np.pi*2, 1)
                self.angularVelocity = 0
        else:
            # All states aim for target location except for EXPLORE.
            # EXPLORE does a random walk, so set its angle in the if statement below
            self.angle = np.arctan2(self.target[1]-self.pos[1], self.target[0]-self.pos[0])
            self.state = state
            self.color = color
            if self.phase == EXPLORE_PHASE and self.target != self.hubLocation:
                self.phase = ASSESS_PHASE
                self.phaseColor = ASSESS_PHASE_COLOR

    def changeState(self, neighborList):

        # TODO: define events and parameters that change states
        if self.state == AT_NEST:
            self.setState(AT_NEST, REST_COLOR, self.hubLocation)
            self.piping_agents = 0
            if np.random.exponential(REST_EXPONENTIAL) > REST_THRESHOLD*REST_EXPONENTIAL:
                self.setState(OBSERVE_HUB, OBSERVE_COLOR, self.hubLocation)
                return
            # If there is an ant that wants to lead this one in a tandem run   # """JOSHUA"""
            # if True:                                                         # """JOSHUA"""
            #    self.setState(FOLLOW, FOLLOW_COLOR, self.hubLocation)         # """JOSHUA"""
            #    print('rest to follow')                                       # """JOSHUA"""
            #    return                                                        # """JOSHUA"""

            if self.phase == CANVAS_PHASE:
                if np.random.randint(0, 1) == 1:  # np.random.exponential(RECRUIT_EXPONENTIAL) > RECRUIT_THRESHOLD*RECRUIT_EXPONENTIAL:
                    self.setState(LEAD_FORWARD, LEAD_FORWARD_COLOR, self.assignedSite.getPosition())
                    return

            for i in range(0, len(neighborList)):
                if neighborList[i].getState() == PIPE:
                    self.piping_agents += 1

                if neighborList[i].getState() == LEAD_FORWARD:  # TODO: maybe add some randomness so they don't all follow
                    if np.random.exponential(FOLLOW_EXPONENTIAL) > FOLLOW_THRESHOLD*FOLLOW_EXPONENTIAL:
                        self.tryFollowing(neighborList[i])
                        return

                if np.random.exponential(self.piping_agents*PIPE_EXPONENTIAL) > PIPE_THRESHOLD*PIPE_EXPONENTIAL and self.piping_agents != 0:  # TODO
                    # print('rest to observe')
                    self.setState(OBSERVE_HUB, OBSERVE_COLOR, self.hubLocation)
                    self.piping_agents = 0
                    return

        if self.state == FOLLOW:
            if self.leadAgent.state == LEAD_FORWARD:
                if np.random.exponential(GET_LOST_EXPONENTIAL) > GET_LOST_THRESHOLD*GET_LOST_EXPONENTIAL:
                    self.leadAgent = None
                    self.setState(EXPLORE, EXPLORE_COLOR, None)
                else:
                    self.updateFollowPosition()

            else:  # elif self.leadAgent.state == AT_NEST or self.leadAgent.state == ASSESS_SITE:
                self.leadAgent = None
                # if they arrived at a nest:
                self.setState(EXPLORE, EXPLORE_COLOR, None)

        if self.state == LEAD_FORWARD:
            # choose a site to recruit from
            if self.goingToRecruit:  # if they are on the way to go recruit someone, they keep going until they get there. TODO: Can they get lost here? for now, no.
                # print("Leader is going to recruit")
                self.setState(LEAD_FORWARD, LEAD_FORWARD_COLOR, self.siteToRecruitFrom.getPosition())
                if self.agentRect.collidepoint(self.siteToRecruitFrom.pos):  # If agent finds the old site, (or maybe this works with accidentally running into a site on the way)
                    print("Leader is close to recruit site")
                    self.goingToRecruit = False  # The agent is now going to head back to the new site
                    self.comingWithFollowers = True
                    self.setState(LEAD_FORWARD, LEAD_FORWARD_COLOR, self.assignedSite.getPosition())  # Go back to the new site with the new follower(s).
                return

            if self.comingWithFollowers:
                # print("Leader is coming with followers")
                self.setState(LEAD_FORWARD, LEAD_FORWARD_COLOR, self.assignedSite.getPosition())
                if self.agentRect.collidepoint(self.assignedSite.pos):
                    print("Leader is going to assess")
                    self.numFollowers = 0
                    self.comingWithFollowers = False
                    self.setState(ASSESS_SITE, LEAD_FORWARD_COLOR, self.assignedSite.getPosition())  # TODO: Set at nest when I have changed that state
                return

            # print("Leader is found a site")
            self.siteToRecruitFrom = self.hub
            if len(self.knownSites) > 2 and np.random.randint(0, 2) != 0:  # if they know some sites, they can choose from them or the hub. If they only know the one they are at, they just go recruit from the hub.
                self.siteToRecruitFrom = self.knownSites[np.random.randint(0, len(self.knownSites) - 1)]
                while self.siteToRecruitFrom == self.assignedSite:
                    self.siteToRecruitFrom = self.knownSites[np.random.randint(0, len(self.knownSites) - 1)]
            self.goingToRecruit = True
            # Go to their randomly chosen site to recruit.
            self.setState(LEAD_FORWARD, LEAD_FORWARD_COLOR, self.siteToRecruitFrom.getPosition())
            # TODO: Can they get lost here? I think so.

        if self.state == OBSERVE_HUB:
            self.setState(OBSERVE_HUB, OBSERVE_COLOR, self.hubLocation)

            if len(neighborList) != 0:
                #  look for pipers
                for i in range(0, len(neighborList)):
                    if neighborList[i].getState() == PIPE or neighborList[i].getState() == COMMIT:
                        if np.random.exponential(RTFX_EXPONENTIAL) > RTFX_THRESHOLD*RTFX_EXPONENTIAL:
                            self.setState(RTFX, RTFX_COLOR, self.hubLocation)
                            self.assignSite(neighborList[i].assignedSite)
                            return

                    if neighborList[i].getState() == LEAD_FORWARD:  # TODO: maybe add some randomness so they don't all follow
                        self.tryFollowing(neighborList[i])
                        return

            if np.random.exponential(OBSERVE_EXPONENTIAL) > OBSERVE_THRESHOLD*OBSERVE_EXPONENTIAL:
                if len(neighborList) != 0:
                    # then look for dancers
                    dancingNeighborList = []
                    for i in range(0, len(neighborList)):
                        if neighborList[i].getState() == DANCE_HUB:
                            dancingNeighborList.append(neighborList[i])
                    if len(dancingNeighborList) != 0:
                        randomNeighbor = np.random.random_integers(0, len(dancingNeighborList)-1)
                        self.assignSite(dancingNeighborList[randomNeighbor].assignedSite)
                        self.estimatedQuality = None
                        self.setState(ASSESS_SITE, ASSESS_COLOR, self.assignedSite.getPosition())
                        return
                        print(f"Chosen neighbor = {randomNeighbor+1} of {len(dancingNeighborList)} @ {self.assignedSite.getPosition()} of quality {self.assignedSite.getQuality()}")
                # If no pipers or dancers, explore

                self.setState(EXPLORE, EXPLORE_COLOR, None)

        if self.state == EXPLORE:
            self.setState(EXPLORE, EXPLORE_COLOR, None)
            siteWithinRange = self.agentRect.collidelist(self.siteObserveRectList)
            # If agent finds a site within range then assess it
            if siteWithinRange != -1 and self.siteList[siteWithinRange] != self.hub:
                self.assignSite(self.siteList[siteWithinRange])
                self.setState(ASSESS_SITE, ASSESS_COLOR, self.assignedSite.getPosition())
            # Else if timeout then switch to resting
            elif np.random.exponential(EXPLORE_EXPONENTIAL) > EXPLORE_THRESHOLD*EXPLORE_EXPONENTIAL:
                self.setState(AT_NEST, REST_COLOR, self.hubLocation)

        if self.state == ASSESS_SITE:
            self.setState(ASSESS_SITE, ASSESS_COLOR, self.assignedSite.getPosition())
            self.ADPX = 0
            # Check to see if you have arrived at the site. If so, evaluate quality and wait to return
            if self.agentRect.collidepoint(self.assignedSite.getPosition()):
                if self.estimatedQuality is None:
                    self.estimatedQuality = self.assignedSite.getQuality()  # TODO: add noise
                    # + int(np.round(np.min(255.0,np.max(0.0, np.random.normal(0,QUALITY_STD))))) # Site quality can't be less than zero
                    print(f"quality = {self.assignedSite.getQuality()}, estimated = {self.estimatedQuality}")
                    if self.estimatedQuality > 255 / 2:
                        self.phase = CANVAS_PHASE  # TODO: Where should I put this?
                        self.phaseColor = CANVAS_PHASE_COLOR
                        self.setState(LEAD_FORWARD, LEAD_FORWARD_COLOR, self.assignedSite.getPosition())
                        # print("Canvasing")
                        return

                if len(neighborList) != 0:
                    for i in range(0, len(neighborList)):
                        if (neighborList[i].getState() == ASSESS_SITE or
                                neighborList[i].getState() == ASSESS_HOME or
                                neighborList[i].getState() == DANCE_SITE or
                                neighborList[i].getState() == DANCE_HUB or
                                neighborList[i].getState() == PIPE or
                                neighborList[i].getState() == COMMIT) and neighborList[i].assignedSite == self.assignedSite:
                            self.ADPX += 1
                            site_to_attach = i

                    if np.random.exponential(self.ADPX*PIPE_EXPONENTIAL) > PIPE_THRESHOLD*PIPE_EXPONENTIAL and self.ADPX != 0:  # TODO
                        # print('assess to pipe')
                        self.setState(PIPE, PIPE_COLOR, self.hubLocation)
                        self.assignSite(neighborList[site_to_attach].assignedSite)
                        self.ADPX = 0
                        return

                if np.random.exponential(ASSESS_EXPONENTIAL) > ASSESS_THRESHOLD*ASSESS_EXPONENTIAL:
                    self.setState(ASSESS_HOME, ASSESS_COLOR, self.hubLocation)
                    self.ADPX = 0

        if self.state == PIPE:
            self.setState(PIPE, PIPE_COLOR, self.hubLocation)
            self.RTFX_agents = 0
            # check if you are at HUB
            if self.agentRect.collidepoint(self.hubLocation):
                # check if enough agents are ready to fly
                for i in range(0, len(neighborList)):
                    if (neighborList[i].getState() == RTFX or neighborList[i].getState() == PIPE or neighborList[i].getState() == COMMIT) and neighborList[i].assignedSite == self.assignedSite:
                        self.RTFX_agents += 1

                if np.random.exponential(self.RTFX_agents*COMMIT_EXPONENTIAL) > COMMIT_THRESHOLD*COMMIT_EXPONENTIAL and self.RTFX_agents != 0:  # TODO
                    # print('pipe to commit')
                    self.setState(COMMIT, COMMIT_COLOR, self.assignedSite.getPosition())
                    self.RTFX_agents = 0

                elif np.random.exponential(PIPE2REST_EXPONENTIAL) > PIPE2REST_THRESHOLD*PIPE2REST_EXPONENTIAL:  # TODO
                    # print('pipe to rest')
                    self.setState(AT_NEST, REST_COLOR, self.hubLocation)
                    self.RTFX_agents = 0

        if self.state == ASSESS_HOME:
            self.setState(ASSESS_HOME, ASSESS_COLOR, self.hubLocation)
            if self.agentRect.collidepoint(self.hubLocation):
                self.setState(DANCE_HUB, DANCE_COLOR, self.hubLocation)
                self.danceTimeFactor = 1.0  # When assessors first return, they dance proportional to quality
                # print(f"danceTimeFactor = {self.danceTimeFactor}")

        if self.state == DANCE_SITE:
            self.setState(DANCE_SITE, DANCE_COLOR, self.assignedSite.getPosition())
            self.ADPX = 0
            if self.agentRect.collidepoint(self.assignedSite.getPosition()):
                if len(neighborList) != 0:
                    for i in range(0, len(neighborList)):
                        if (neighborList[i].getState() == ASSESS_SITE or neighborList[i].getState() == ASSESS_HOME or neighborList[i].getState() == DANCE_SITE or
                                neighborList[i].getState() == DANCE_HUB or neighborList[i].getState() == PIPE or neighborList[i].getState() == COMMIT) and neighborList[i].assignedSite == self.assignedSite:
                            self.ADPX += 1
                            site_to_attach = i

                    if np.random.exponential(self.ADPX*PIPE_EXPONENTIAL) > PIPE_THRESHOLD*PIPE_EXPONENTIAL and self.ADPX != 0:  # TODO
                        # print('dance site to pipe')
                        self.setState(PIPE, PIPE_COLOR, self.hubLocation)
                        self.assignSite(neighborList[site_to_attach].assignedSite)
                        self.ADPX = 0
                        return

                if np.random.exponential(ASSESS_EXPONENTIAL) > ASSESS_THRESHOLD*ASSESS_EXPONENTIAL:
                    # print('dance site to hub')
                    self.estimatedQuality = self.assignedSite.getQuality()  # TODO: add noise
                    self.danceTimeFactor *= DANCE_DECAY
                    self.setState(DANCE_HUB, DANCE_COLOR, self.hubLocation)
                    self.ADPX = 0

        if self.state == DANCE_HUB:
            self.setState(DANCE_HUB, DANCE_COLOR, self.hubLocation)
            self.RTFX_agents = 0
            self.piping_agents = 0

            if len(neighborList) != 0:
                for i in range(0, len(neighborList)):
                    if (neighborList[i].getState() == ASSESS_HOME or neighborList[i].getState() == DANCE_SITE or
                            neighborList[i].getState() == DANCE_HUB or neighborList[i].getState() == PIPE or neighborList[i].getState() == COMMIT or
                            neighborList[i].getState() == RTFX) and neighborList[i].assignedSite == self.assignedSite:
                        self.RTFX_agents += 1
                        site_to_attach = i
                    if neighborList[i].getState() == PIPE:
                        self.piping_agents += 1

                if np.random.exponential(RTFX_EXPONENTIAL*self.RTFX_agents) > RTFX_THRESHOLD*RTFX_EXPONENTIAL and self.RTFX_agents != 0 and self.piping_agents > 0:
                    # print('dance hub to rtfx')
                    self.RTFX_agents = 0
                    self.assignSite(neighborList[site_to_attach].assignedSite)
                    self.setState(RTFX, RTFX_COLOR, self.hubLocation)
                    return

            if self.agentRect.collidepoint(self.hubLocation) and np.random.exponential(ASSESS_EXPONENTIAL) < np.int(np.round(self.danceTimeFactor * self.estimatedQuality/255.0 * np.float(ASSESS_THRESHOLD*ASSESS_EXPONENTIAL))):
                # print('dance hub to site')
                self.setState(DANCE_SITE, DANCE_COLOR, self.assignedSite.getPosition())
                self.RTFX_agents = 0
                return

            if self.agentRect.collidepoint(self.hubLocation) and self.danceTimeFactor*self.estimatedQuality < 0.3*255.0:  # TODO: Magic number for when to go from dancing to resting
                # print('dance hub to rest')
                self.setState(AT_NEST, REST_COLOR, self.hubLocation)
                self.RTFX_agents = 0

        if self.state == RTFX:
            self.setState(RTFX, RTFX_COLOR, self.hubLocation)
            self.RTFX_agents = 0
            for i in range(0, len(neighborList)):
                if (neighborList[i].getState() == COMMIT or neighborList[i].getState() == RTFX or neighborList[i].getState() == PIPE) and neighborList[i].assignedSite == self.assignedSite:
                    self.RTFX_agents += 1
                    site_to_attach = i

            if np.random.exponential(self.RTFX_agents*COMMIT_EXPONENTIAL) > COMMIT_THRESHOLD*COMMIT_EXPONENTIAL and self.RTFX_agents != 0:  # TODO
                print('RTFX to Commit')
                self.assignSite(neighborList[site_to_attach].assignedSite)
                self.setState(COMMIT, COMMIT_COLOR, self.assignedSite.getPosition())  # TODO: check self assigned site vs neighbors site
                self.RTFX_agents = 0
                return

            if np.random.exponential(RTF2REST_EXPONENTIAL) > RTF2REST_EXPONENTIAL*RTF2REST_THRESHOLD:
                self.setState(AT_NEST, REST_COLOR, self.hubLocation)
                self.RTFX_agents = 0

        if self.state == COMMIT:
            self.setState(COMMIT, COMMIT_COLOR, self.assignedSite.getPosition())

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
        self.agentRect.centerx = int(np.round(float(self.leadAgent.pos[0]) - self.leadAgent.speed * np.cos(self.leadAgent.angle))) # TODO: Maybe need to subtract more?
        self.agentRect.centery = int(np.round(float(self.leadAgent.pos[1]) - self.leadAgent.speed * np.sin(self.leadAgent.angle)))
        self.pos = [self.agentRect.centerx, self.agentRect.centery]

    def tryFollowing(self, leader):
        if leader.numFollowers < MAX_FOLLOWERS:  # TODO: How many ants can follow?
            self.leadAgent = leader
            self.leadAgent.incrementFollowers()
            self.setState(FOLLOW, FOLLOW_COLOR, self.leadAgent.pos)

    def incrementFollowers(self):
        self.numFollowers += 1
        print("Followers: " + str(self.numFollowers))

    def drawAgent(self, surface):
        surface.blit(self.agentHandle, self.agentRect)

        pyg.draw.ellipse(surface, self.color, self.agentRect, 4)
        pyg.draw.ellipse(surface, self.phaseColor, self.agentRect, 2)

    def getAgentHandle(self):
        return self.agentHandle

    def getAgentRect(self):
        return self.agentRect

    def assignSite(self, site):
        if site == self.hub:
            return  # Don't assign them to the home they are leaving
        if self.assignedSite is not None:
            self.assignedSite.decrementCount()
        self.assignedSite = site
        self.assignedSite.incrementCount()
        self.knownSites.append(self.assignedSite)
