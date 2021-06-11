from Constants import *
from states.SearchState import SearchState
from states.State import State


class FollowState(State):

    def __init__(self, agent):
        super().__init__(agent)
        self.state = FOLLOW
        self.color = FOLLOW_COLOR

    def changeState(self, neighborList) -> None:
        if self.agent.leadAgent.getState() == LEAD_FORWARD or self.agent.leadAgent.getState() == REVERSE_TANDEM:
            if self.agent.shouldGetLost():
                self.agent.leadAgent = None
                self.setState(SearchState(self.agent), None)
            else:
                self.agent.updateFollowPosition()
                if self.agent.phase == COMMIT_PHASE and self.agent.leadAgent.getState() == REVERSE_TANDEM\
                        and self.agent.leadAgent.comingWithFollowers:
                    self.agent.knownSites.append(self.agent.leadAgent.siteToRecruitFrom)
                    self.agent.siteToRecruitFrom = self.agent.leadAgent.siteToRecruitFrom
                    from states.ReverseTandemState import ReverseTandemState
                    self.setState(ReverseTandemState(self.agent), self.agent.siteToRecruitFrom)
        else:
            # if they arrived at a nest:
            self.agent.leadAgent = None
            if self.agent.phase == EXPLORE_PHASE:
                self.agent.setPhase(ASSESS_PHASE)
            self.setState(SearchState(self.agent), None)
