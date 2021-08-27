import numpy as np

from Constants import *
from model.phases.AssessPhase import AssessPhase
from model.states.State import State


class SearchState(State):
    """ State where agents look around the world for better sites """

    def __init__(self, agent):
        super().__init__(agent)
        self.state = SEARCH

    def move(self, state) -> None:
        if state.state != SEARCH:
            super().move(state)
        else:
            # If going from search to search, just update angle
            self.agent.angularVelocity += np.random.normal(0, np.pi / 1000)
            self.agent.setAngle(self.agent.angle + self.agent.angularVelocity)

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.target)
        self.agent.marker = None

        # If agent finds a site within range then assess it
        if self.agent.siteInRangeIndex != -1:
            self.agent.addToKnownSites(self.agent.world.siteList[self.agent.siteInRangeIndex])
            # If the site is better than the one they were assessing, they assess it instead.
            if self.agent.estimateQuality(self.agent.world.siteList[self.agent.siteInRangeIndex]) > self.agent.estimatedQuality\
                    and self.agent.world.siteList[self.agent.siteInRangeIndex] is not self.agent.getHub():
                self.agent.assignSite(self.agent.world.siteList[self.agent.siteInRangeIndex])
                from model.states.AtNestState import AtNestState
                self.setState(AtNestState(self.agent), self.agent.getAssignedSitePosition())
                self.agent.setPhase(AssessPhase())
        elif self.agent.shouldReturnToNest():
            from model.states.AtNestState import AtNestState
            self.setState(AtNestState(self.agent), self.agent.getAssignedSitePosition())
        elif self.agent.isTooFarAway(self.agent.getHub()):
            self.goBackTowardSite(self.agent.getHub())

        # If an agent nearby is transporting, get carried by that agent.
        for i in range(0, len(neighborList)):
            if neighborList[i].getState() == TRANSPORT:
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

    def toString(self):
        return "SEARCH"

    def getColor(self):
        return SEARCH_COLOR
