import numpy as np

from Constants import *
from phases.AssessPhase import AssessPhase
from states.State import State


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
            self.agent.angle = self.agent.angle + self.agent.angularVelocity

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.target)
        siteWithinRange = self.agent.getAgentRect().collidelist(self.agent.world.siteRectList)
        # If agent finds a site within range then assess it

        if siteWithinRange != -1:
            self.agent.addToKnownSites(self.agent.world.siteList[siteWithinRange])
            # If the site is better than the one they were assessing, they assess it instead.
            if self.agent.estimateQuality(self.agent.world.siteList[siteWithinRange]) > self.agent.estimatedQuality\
                    and self.agent.world.siteList[siteWithinRange] is not self.agent.getHub():
                self.agent.assignSite(self.agent.world.siteList[siteWithinRange])
                from states.AtNestState import AtNestState
                self.setState(AtNestState(self.agent), self.agent.getAssignedSitePosition())
                self.agent.setPhase(AssessPhase())
        elif self.agent.shouldReturnToNest():
            from states.AtNestState import AtNestState
            self.setState(AtNestState(self.agent), self.agent.getAssignedSitePosition())
        elif self.agent.isTooFarAway(self.agent.assignedSite):
            self.goBackTowardSite(self.agent.assignedSite)

        # If an agent nearby is transporting, get carried by that agent.
        for i in range(0, len(neighborList)):
            if neighborList[i].getState() == TRANSPORT:
                self.getCarried(neighborList[i])
                return

    def getCarried(self, transporter):
        if transporter.numFollowers < MAX_FOLLOWERS:
            self.agent.leadAgent = transporter
            self.agent.leadAgent.incrementFollowers()
            from states.CarriedState import CarriedState
            self.setState(CarriedState(self.agent), self.agent.leadAgent.pos)

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
        self.agent.angle = self.agent.angle - (1.1 * np.pi)

    def toString(self):
        return "SEARCH"

    def getColor(self):
        return SEARCH_COLOR
