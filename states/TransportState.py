from Constants import *
from states.RecruitState import RecruitState
from states.phases.CommitPhase import CommitPhase


class TransportState(RecruitState):

    def __init__(self, agent):
        super().__init__(agent)
        self.state = TRANSPORT
        self.color = TRANSPORT_COLOR

    def arriveAtSite(self):
        if self.agent.shouldKeepTransporting():
            CommitPhase.transportOrReverseTandem(self)
        else:
            from states.SearchState import SearchState
            self.setState(SearchState(self.agent), self.agent.assignedSite.getPosition())
