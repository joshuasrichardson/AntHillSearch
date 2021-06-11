import numpy as np

from Constants import *
from states.State import State


class SearchState(State):

    def __init__(self, agent):
        super().__init__(agent)
        self.state = SEARCH
        self.color = SEARCH_COLOR

    def move(self, state, target) -> None:
        if state.state != SEARCH:
            super().move(state, target)
            return
        # If going from search to search, just update angle
        self.agent.angularVelocity += np.random.normal(0, np.pi/200)
        self.agent.angle = self.agent.angle + self.agent.angularVelocity*TIME_STEP

    def changeState(self, neighborList) -> None:
        self.setState(self, None)
        siteWithinRange = self.agent.agentRect.collidelist(self.agent.siteObserveRectList)
        # If agent finds a site within range then assess it

        if self.sightIsInRange(siteWithinRange):
            self.agent.knownSites.append(self.agent.assignedSite)
            # If the site is better than the one they were assessing, they assess it instead.
            if self.agent.siteList[siteWithinRange].getQuality() > self.agent.estimatedQuality:
                self.agent.assignSite(self.agent.siteList[siteWithinRange])
                from states.AtNestState import AtNestState
                self.setState(AtNestState(self.agent), self.agent.assignedSite.getPosition())
                if self.agent.phase == EXPLORE_PHASE:
                    self.agent.setPhase(ASSESS_PHASE)
        elif self.agent.shouldReturnToNest():
            from states.AtNestState import AtNestState
            self.setState(AtNestState(self.agent), self.agent.assignedSite.getPosition())

        # If an agent nearby is transporting, get carried by that agent.
        for i in range(0, len(neighborList)):
            if neighborList[i].getState() == TRANSPORT:
                self.getCarried(neighborList[i])
                return

    def sightIsInRange(self, siteWithinRange):
        return siteWithinRange != -1 and self.agent.siteList[siteWithinRange] != self.agent.hub

    def getCarried(self, transporter):
        if transporter.numFollowers < MAX_FOLLOWERS:
            self.agent.leadAgent = transporter
            self.agent.leadAgent.incrementFollowers()
            from states.CarriedState import CarriedState
            self.setState(CarriedState(self.agent), self.agent.leadAgent.pos)
