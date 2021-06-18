from Constants import *
from states.RecruitState import RecruitState
from states.phases.CommitPhase import CommitPhase


class LeadForwardState(RecruitState):

    def __init__(self, agent):
        super().__init__(agent)
        self.state = LEAD_FORWARD
        self.color = LEAD_FORWARD_COLOR

    def arriveAtSite(self):
        if self.agent.quorumMet():  # If enough agents are at that site
            self.agent.setPhase(COMMIT_PHASE)  # Commit to the site
            CommitPhase.transportOrReverseTandem(self)
        else:
            from states.AtNestState import AtNestState
            self.setState(AtNestState(self.agent), self.agent.assignedSite.getPosition())  # Just be at the site and decide what to do next in the AT_NEST state
