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
        self.pos = world.getHubPosition()  # Initial position
        self.siteObserveRectList = world.getSiteObserveRectList()  # List of rectangles of all the sites in the world
        self.siteList = world.getSiteList()  # List of all the sites in the world
        self.hubLocation = world.getHubPosition()  # Original home location
        self.agentHandle = pyg.image.load("copter.png")  # Image on screen representing the agent
        self.agentRect = self.agentHandle.get_rect()  # Rectangle around the agent
        self.agentRect.centerx = self.pos[0]  # Horizontal center of the agent
        self.agentRect.centery = self.pos[1]  # Vertical center of the agent
        self.speed = AGENT_SPEED*TIME_STEP  # Speed the agent moves on the screen
        self.state = None  # Defines what the agent is currently doing
        self.setState(REST, self.hubLocation)
        self.AngularVelocity = 0  # Speed the agent is changing direction
        self.assignedSite = None  # Site that the agent has discovered and is trying to get others to go see
        self.estimatedQuality = None  # The agent's evaluation of the assigned site
        self.danceTimeFactor = None  # A number to help decide how long an agent dances
        self.ADPX = 0  # Number of neighbor agents Assessing, Dancing, Piping, or Committed for site X
        self.RTFX_agents = 0  # Agents around this agent in the hub that are ready to fly
        self.piping_agents = 0  # Number of agents around this agent that are piping
        self.target = self.hubLocation  # Either the hub or a site the agent is going to
        self.angle = np.arctan2(self.target[1]-self.pos[1], self.target[0]-self.pos[0])  # Angle the agent is moving
        self.angularVelocity = 0  # The speed at which the agent is changing direction
        self.color = REST_COLOR  # Color around the agent displaying their current state

    def setState(self, state, target):
        self.target = target
        if state != EXPLORE:
            # All states aim for target location except for EXPLORE.
            # EXPLORE does a random walk, so set its angle in the if statement below
            self.angle = np.arctan2(self.target[1]-self.pos[1], self.target[0]-self.pos[0])
        if state == REST:
            self.state = REST
            self.color = REST_COLOR
        if state == OBSERVE_HUB:
            self.state = OBSERVE_HUB
            self.color = OBSERVE_COLOR
        if state == EXPLORE:
            if self.state == EXPLORE:
                # If not changing state, just update angle
                self.angularVelocity += np.random.normal(0, np.pi/200)  # TODO: Magic number
                self.angle = self.angle + self.angularVelocity*TIME_STEP
            else:
                # If changing state, set angle randomly
                self.state = EXPLORE
                self.color = EXPLORE_COLOR
                self.target = target
                # Random direction
                self.angle = np.random.uniform(0, np.pi*2, 1)
                self.angularVelocity = 0
        if state == ASSESS_SITE:
            self.state = ASSESS_SITE
            self.color = ASSESS_COLOR
        if state == ASSESS_HOME:
            self.state = ASSESS_HOME
            self.color = ASSESS_COLOR
        if state == DANCE_SITE:
            self.state = DANCE_SITE
            self.color = DANCE_COLOR
        if state == DANCE_HUB:
            self.state = DANCE_HUB
            self.color = DANCE_COLOR
        if state == PIPE:
            self.state = PIPE
            self.color = PIPE_COLOR
        if state == COMMIT:
            self.state = COMMIT
            self.color = COMMIT_COLOR
        if state == RTFX:
            self.state = RTFX
            self.color = RTFX_COLOR

    def changeState(self, neighborList):
        # TODO: define events and parameters that change states
        if self.state == REST:
            self.setState(REST, self.hubLocation)
            self.piping_agents = 0
            if np.random.exponential(REST_EXPONENTIAL) > REST_THRESHOLD*REST_EXPONENTIAL:
                self.setState(OBSERVE_HUB, self.hubLocation)
                return

            for i in range(0, len(neighborList)):
                if neighborList[i].getState() == PIPE:
                    self.piping_agents += 1

                if np.random.exponential(self.piping_agents*PIPE_EXPONENTIAL) > PIPE_THRESHOLD*PIPE_EXPONENTIAL and self.piping_agents != 0:  # TODO
                    print('rest to observe')
                    self.setState(OBSERVE_HUB, self.hubLocation)
                    self.piping_agents = 0
                    return

                # if np.random.exponential(RTFX_EXPONENTIAL) > RTFX_THRESHOLD*RTFX_EXPONENTIAL:
                #     self.setState(RTFX,self.hubLocation)
                #     self.assignedSite = neighborList[i].assignedSite
                #     return

        if self.state == OBSERVE_HUB:
            self.setState(OBSERVE_HUB, self.hubLocation)

            if len(neighborList) != 0:
                #  look for pipers
                for i in range(0, len(neighborList)):
                    if neighborList[i].getState() == PIPE or neighborList[i].getState() == COMMIT:
                        if np.random.exponential(RTFX_EXPONENTIAL) > RTFX_THRESHOLD*RTFX_EXPONENTIAL:
                            self.setState(RTFX, self.hubLocation)
                            self.assignedSite = neighborList[i].assignedSite
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
                        self.assignedSite = dancingNeighborList[randomNeighbor].assignedSite
                        self.estimatedQuality = None
                        self.setState(ASSESS_SITE, self.assignedSite.getPosition())
                        return
                        print(f"Chosen neighbor = {randomNeighbor+1} of {len(dancingNeighborList)} @ {self.assignedSite.getPosition()} of quality {self.assignedSite.getQuality()}")
                # If no pipers or dancers, explore

                self.setState(EXPLORE, None)

        if self.state == EXPLORE:
            self.setState(EXPLORE, None)
            siteWithinRange = self.agentRect.collidelist(self.siteObserveRectList)
            # If agent finds a site within range then assess it
            if siteWithinRange != -1:
                self.assignedSite = self.siteList[siteWithinRange]
                self.setState(ASSESS_SITE, self.assignedSite.getPosition())
            # Else if timeout then switch to resting
            elif np.random.exponential(EXPLORE_EXPONENTIAL) > EXPLORE_THRESHOLD*EXPLORE_EXPONENTIAL:
                self.setState(REST, self.hubLocation)

        if self.state == ASSESS_SITE:
            self.setState(ASSESS_SITE, self.assignedSite.getPosition())
            self.ADPX = 0
            # Check to see if you have arrived at the site. If so, evaluate quality and wait to return
            if self.agentRect.collidepoint(self.assignedSite.getPosition()):
                if self.estimatedQuality is None:
                    self.estimatedQuality = self.assignedSite.getQuality()  # TODO: add noise
                    # + int(np.round(np.min(255.0,np.max(0.0, np.random.normal(0,QUALITY_STD))))) # Site quality can't be less than zero
                    print(f"quality = {self.assignedSite.getQuality()}, estimated = {self.estimatedQuality}")

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
                        print('assess to pipe')
                        self.setState(PIPE, self.hubLocation)
                        self.assignedSite = neighborList[site_to_attach].assignedSite
                        self.ADPX = 0
                        return

                if np.random.exponential(ASSESS_EXPONENTIAL) > ASSESS_THRESHOLD*ASSESS_EXPONENTIAL:
                    self.setState(ASSESS_HOME, self.hubLocation)
                    self.ADPX = 0

        if self.state == PIPE:
            self.setState(PIPE, self.hubLocation)
            self.RTFX_agents = 0
            # check if you are at HUB
            if self.agentRect.collidepoint(self.hubLocation):
                # check if enough agents are ready to fly
                for i in range(0, len(neighborList)):
                    if (neighborList[i].getState() == RTFX or neighborList[i].getState() == PIPE or neighborList[i].getState() == COMMIT) and neighborList[i].assignedSite == self.assignedSite:
                        self.RTFX_agents += 1

                if np.random.exponential(self.RTFX_agents*COMMIT_EXPONENTIAL) > COMMIT_THRESHOLD*COMMIT_EXPONENTIAL and self.RTFX_agents != 0:  # TODO
                    print('pipe to commit')
                    self.setState(COMMIT, self.assignedSite.getPosition())
                    self.RTFX_agents = 0

                elif np.random.exponential(PIPE2REST_EXPONENTIAL) > PIPE2REST_THRESHOLD*PIPE2REST_EXPONENTIAL:  # TODO
                    print('pipe to rest')
                    self.setState(REST, self.hubLocation)
                    self.RTFX_agents = 0

        if self.state == ASSESS_HOME:
            self.setState(ASSESS_HOME, self.hubLocation)
            if self.agentRect.collidepoint(self.hubLocation):
                self.setState(DANCE_HUB, self.hubLocation)
                self.danceTimeFactor = 1.0  # When assessors first return, they dance proportional to quality
                # print(f"danceTimeFactor = {self.danceTimeFactor}")

        if self.state == DANCE_SITE:
            self.setState(DANCE_SITE, self.assignedSite.getPosition())
            self.ADPX = 0
            if self.agentRect.collidepoint(self.assignedSite.getPosition()):
                if len(neighborList) != 0:
                    for i in range(0, len(neighborList)):
                        if (neighborList[i].getState() == ASSESS_SITE or neighborList[i].getState() == ASSESS_HOME or neighborList[i].getState() == DANCE_SITE or
                                neighborList[i].getState() == DANCE_HUB or neighborList[i].getState() == PIPE or neighborList[i].getState() == COMMIT) and neighborList[i].assignedSite == self.assignedSite:
                            self.ADPX += 1
                            site_to_attach = i

                    if np.random.exponential(self.ADPX*PIPE_EXPONENTIAL) > PIPE_THRESHOLD*PIPE_EXPONENTIAL and self.ADPX != 0:  # TODO
                        print('dance site to pipe')
                        self.setState(PIPE, self.hubLocation)
                        self.assignedSite = neighborList[site_to_attach].assignedSite
                        self.ADPX = 0
                        return

                if np.random.exponential(ASSESS_EXPONENTIAL) > ASSESS_THRESHOLD*ASSESS_EXPONENTIAL:
                    # print('dance site to hub')
                    self.estimatedQuality = self.assignedSite.getQuality()  # TODO: add noise
                    self.danceTimeFactor *= DANCE_DECAY
                    self.setState(DANCE_HUB, self.hubLocation)
                    self.ADPX = 0

        if self.state == DANCE_HUB:
            self.setState(DANCE_HUB, self.hubLocation)
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
                    print('dance hub to rtfx')
                    self.RTFX_agents = 0
                    self.assignedSite = neighborList[site_to_attach].assignedSite
                    self.setState(RTFX, self.hubLocation)
                    return

            if self.agentRect.collidepoint(self.hubLocation) and np.random.exponential(ASSESS_EXPONENTIAL) > np.int(np.round(self.danceTimeFactor * self.estimatedQuality/255.0 * np.float(ASSESS_THRESHOLD*ASSESS_EXPONENTIAL))):
                # print('dance hub to site')
                self.setState(DANCE_SITE, self.assignedSite.getPosition())
                self.RTFX_agents = 0
                return

            if self.agentRect.collidepoint(self.hubLocation) and self.danceTimeFactor*self.estimatedQuality < 0.3*255.0:  # TODO: Magic number for when to go from dancing to resting
                # print('dance hub to rest')
                self.setState(REST, self.hubLocation)
                self.RTFX_agents = 0

        if self.state == RTFX:
            self.setState(RTFX, self.hubLocation)
            self.RTFX_agents = 0
            for i in range(0, len(neighborList)):
                if (neighborList[i].getState() == COMMIT or neighborList[i].getState() == RTFX or neighborList[i].getState() == PIPE) and neighborList[i].assignedSite == self.assignedSite:
                    self.RTFX_agents += 1
                    site_to_attach = i

            if np.random.exponential(self.RTFX_agents*COMMIT_EXPONENTIAL) > COMMIT_THRESHOLD*COMMIT_EXPONENTIAL and self.RTFX_agents != 0:  # TODO
                print('RTFX to Commit')
                self.assignedSite = neighborList[site_to_attach].assignedSite
                self.setState(COMMIT, self.assignedSite.getPosition())  # TODO: check self assigned site vs neighbors site
                self.RTFX_agents = 0
                return

            if np.random.exponential(RTF2REST_EXPONENTIAL) > RTF2REST_EXPONENTIAL*RTF2REST_THRESHOLD:
                self.setState(REST, self.hubLocation)
                self.RTFX_agents = 0

        if self.state == COMMIT:
            self.setState(COMMIT, self.assignedSite.getPosition())

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

    def drawAgent(self, surface):
        surface.blit(self.agentHandle, self.agentRect)
        pyg.draw.ellipse(surface, self.color, self.agentRect, 1)

    def getAgentHandle(self):
        return self.agentHandle

    def getAgentRect(self):
        return self.agentRect

# for i in range(0, len(neighborList)):
#     if neighborList[i].getState() == COMMIT and neighborList[i].assignedSite == self.assignedSite:
#         if np.random.exponential(COMMIT_EXPONENTIAL) > COMMIT_THRESHOLD*COMMIT_EXPONENTIAL:  # TODO
#             self.setState(COMMIT, neighborList[i].assignedSite.getPosition())  # TODO: check self assigned site vs neighbors site
#             self.assignedSite = neighborList[i].assignedSite
#             return
