from Constants import *
from model.phases.CommitPhase import CommitPhase
from model.states.RecruitState import RecruitState


class LeadForwardState(RecruitState):
    """ State where an agent goes to known sites and starts recruiting other agents to a better site it found """

    def __init__(self, agent):
        """ agent - the agent that is in this state """
        super().__init__(agent)
        self.stateNumber = LEAD_FORWARD

    def arriveAtSite(self, neighborList):
        if self.agent.quorumMet(neighborList):  # If enough agents are at that site
            self.agent.setPhase(CommitPhase())  # Commit to the site
            self.agent.transportOrReverseTandem(self)
        else:
            from model.states.AtNestState import AtNestState
            self.setState(AtNestState(self.agent), self.agent.getAssignedSitePosition())  # Just be at the site and decide what to do next in the AT_NEST state

    def toString(self):
        return "LEAD_FORWARD"

    def getColor(self):
        return LEAD_FORWARD_COLOR
