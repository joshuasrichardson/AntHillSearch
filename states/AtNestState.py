from Constants import *
from states.FollowState import FollowState
from states.LeadForwardState import LeadForwardState
from states.SearchState import SearchState
from states.phases.CommitPhase import CommitPhase
from states.phases.AssessPhase import AssessPhase
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
                AssessPhase.acceptOrReject(self)
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
            # if neighborList[i].getState() == REVERSE_TANDEM: TODO: REVERSE_TANDEM
            #     self.getCarried(neighborList[i])
            #     return
            if neighborList[i].getState() == LEAD_FORWARD and neighborList[i].estimatedQuality > self.agent.estimatedQuality:
                if self.agent.shouldFollow():
                    self.tryFollowing(neighborList[i])
                    return

    def tryFollowing(self, leader):
        if leader.numFollowers < MAX_FOLLOWERS:
            self.agent.leadAgent = leader
            self.agent.leadAgent.incrementFollowers()
            self.setState(FollowState(self.agent), self.agent.leadAgent.pos)
