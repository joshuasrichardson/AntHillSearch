from Constants import *
from states.FollowState import FollowState
from states.LeadForwardState import LeadForwardState
from states.SearchState import SearchState
from states.phases.CommitPhase import CommitPhase
from states.State import State


class AtNestState(State):

    def __init__(self, agent):
        super().__init__(agent)
        self.state = AT_NEST
        self.color = AT_NEST_COLOR

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.assignedSite.getPosition())

        if self.agent.shouldSearch():
            self.setState(SearchState(self.agent), None)
            return

        if self.agent.phase == ASSESS_PHASE:
            if self.agent.isDoneAssessing():
                self.acceptOrReject()
                return

        if self.agent.phase == CANVAS_PHASE:
            if self.agent.shouldRecruit():
                self.setState(LeadForwardState(self.agent), self.agent.assignedSite.getPosition())
                return

        if self.agent.phase == COMMIT_PHASE:
            # Recruit, search, or follow
            if self.agent.shouldRecruit():
                CommitPhase.transportOrReverseTandem(self)
                return

        for i in range(0, len(neighborList)):
            if (neighborList[i].getState() == LEAD_FORWARD and neighborList[i].estimatedQuality > self.agent.estimatedQuality)\
                    or (neighborList[i].getState() == REVERSE_TANDEM and neighborList[i].estimatedQuality >= self.agent.estimatedQuality)\
                    and self.agent.shouldFollow():
                self.tryFollowing(neighborList[i])
                return

    def tryFollowing(self, leader):
        if leader.numFollowers < MAX_FOLLOWERS:
            self.agent.leadAgent = leader
            self.agent.leadAgent.incrementFollowers()
            self.setState(FollowState(self.agent), self.agent.leadAgent.pos)

    def acceptOrReject(self):
        # If they determine the site is good enough after they've been there long enough,
        if self.agent.estimatedQuality > MIN_ACCEPT_VALUE:
            # they enter the canvasing phase and start recruiting others.
            self.agent.setPhase(CANVAS_PHASE)
            from states.LeadForwardState import LeadForwardState
            self.setState(LeadForwardState(self.agent), self.agent.assignedSite.getPosition())
        else:
            self.agent.setPhase(EXPLORE_PHASE)
            from states.SearchState import SearchState
            self.setState(SearchState(self.agent), None)
