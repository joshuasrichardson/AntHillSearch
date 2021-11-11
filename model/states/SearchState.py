import numpy as np

from Constants import *
from model.phases.AssessPhase import AssessPhase
from model.states.State import State


class SearchState(State):
    """ State where agents look around the world for better sites """

    def __init__(self, agent):
        super().__init__(agent)
        self.stateNumber = SEARCH
        self.collides = False
        self.itersSinceLastCollide = 8

    def updateAngle(self, stateNumber) -> None:
        if stateNumber != SEARCH:
            super().updateAngle(stateNumber)
        else:
            self.itersSinceLastCollide += 1
            if self.collides and self.itersSinceLastCollide > 8:  # Go straight unless they bump into an obstacle
                if np.random.randint(0, 2) == 1:
                    self.agent.setAngle(self.agent.angle - np.pi / 2)  # Ants are more likely to turn left for some reason.
                    # See https://www.nature.com/articles/s41598-018-23652-4
                else:
                    self.agent.setAngle(np.random.uniform(0, 2 * np.pi, 1))
                self.itersSinceLastCollide = 0

    def changeState(self, neighborList) -> None:
        # Set whether they collided with another agent or not. If they are by a nest, they don't collide because they can go down into the nest, etc.
        self.collides = len(neighborList) > 1 and not self.agent.isCloseToASite()
        self.setState(self, self.agent.target)
        self.agent.marker = None

        avoidPlace = self.agent.getNearbyPlaceToAvoid()
        if avoidPlace is not None:  # If the agent is too close to a place they are supposed to avoid
            self.moveAway(avoidPlace)  # Turn away from it.
        # If agent finds a site within range then assess it
        elif self.agent.siteInRangeIndex != -1:
            self.agent.addToKnownSites(self.agent.world.siteList[self.agent.siteInRangeIndex])
            # If the site is better than the one they were assessing, they assess it instead.
            if self.agent.estimateQuality(self.agent.world.siteList[self.agent.siteInRangeIndex]) > self.agent.estimatedQuality\
                    and self.agent.world.siteList[self.agent.siteInRangeIndex] is not self.agent.getHub():
                self.agent.assignSite(self.agent.world.siteList[self.agent.siteInRangeIndex])
                if self.agent.world.siteList[self.agent.siteInRangeIndex] is not self.agent.assignedSite\
                        or self.agent.getPhaseNumber() == EXPLORE:
                    self.agent.setPhase(AssessPhase())
                from model.states.AtNestState import AtNestState
                self.setState(AtNestState(self.agent), self.agent.getAssignedSitePosition())
        elif self.agent.shouldReturnToNest():
            from model.states.AtNestState import AtNestState
            self.setState(AtNestState(self.agent), self.agent.getAssignedSitePosition())
        elif self.agent.isTooFarAway(self.agent.getHub()):
            self.goBackTowardSite(self.agent.getHub())

        # If an agent nearby is transporting, get carried by that agent.
        for i in range(0, len(neighborList)):
            if neighborList[i].getStateNumber() == TRANSPORT:
                self.getCarried(neighborList[i])
                return

    def getCarried(self, transporter):
        if transporter.numFollowers < MAX_FOLLOWERS:
            self.agent.leadAgent = transporter
            self.agent.leadAgent.incrementFollowers()
            from model.states.CarriedState import CarriedState
            self.setState(CarriedState(self.agent), self.agent.leadAgent.getPosition())

    def goBackTowardSite(self, site):
        if site.getPosition()[0] > self.agent.getPosition()[0]:
            x = self.agent.getPosition()[0] + 1
        else:
            x = self.agent.getPosition()[0] - 1
        if site.getPosition()[1] > self.agent.getPosition()[1]:
            y = self.agent.getPosition()[1] + 1
        else:
            y = self.agent.getPosition()[1] - 1
        self.agent.setPosition(x, y)
        self.agent.setAngle(self.agent.angle - (1.1 * np.pi))

    def moveAway(self, pos):
        if pos[0] < self.agent.getPosition()[0]:
            x = self.agent.getPosition()[0] + 1
        else:
            x = self.agent.getPosition()[0] - 1
        if pos[1] < self.agent.getPosition()[1]:
            y = self.agent.getPosition()[1] + 1
        else:
            y = self.agent.getPosition()[1] - 1
        self.agent.setPosition(x, y)
        self.agent.setAngle(self.agent.angle - np.random.uniform(np.pi / 2, np.pi))

    def toString(self):
        return "SEARCH"

    def getColor(self):
        return SEARCH_COLOR
