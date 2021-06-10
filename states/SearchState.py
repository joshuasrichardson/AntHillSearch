import numpy as np

from Constants import *
from states.phases.AssessPhase import AssessPhase
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

        if self.agent.phase == EXPLORE_PHASE:
            if siteWithinRange != -1 and self.agent.siteList[siteWithinRange] != self.agent.hub:
                self.agent.knownSites.append(self.agent.assignedSite)
                self.agent.assignSite(self.agent.siteList[siteWithinRange])
                self.agent.setPhase(ASSESS_PHASE)
                from states.AtNestState import AtNestState
                self.setState(AtNestState(self.agent), self.agent.assignedSite.getPosition())
            # Else if timeout then switch to resting
            elif self.agent.shouldReturnToNest():
                from states.AtNestState import AtNestState
                self.setState(AtNestState(self.agent), self.agent.assignedSite.getPosition())

        else:
            if siteWithinRange != -1 and self.agent.siteList[siteWithinRange] != self.agent.hub:
                self.agent.knownSites.append(self.agent.assignedSite)
                # If the site is better than the one they were assessing, they assess it instead.
                if self.agent.siteList[siteWithinRange].getQuality() > self.agent.estimatedQuality:
                    self.agent.assignSite(self.agent.siteList[siteWithinRange])
                    from states.AtNestState import AtNestState
                    self.setState(AtNestState(self.agent), self.agent.assignedSite.getPosition())
            elif self.agent.shouldReturnToNest():  # Else if timeout then go back to continue assessing the site
                from states.AtNestState import AtNestState
                self.setState(AtNestState(self.agent), self.agent.assignedSite.getPosition())
            elif self.agent.phase == ASSESS_PHASE and self.agent.isDoneAssessing():
                AssessPhase.acceptOrReject(self)

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
