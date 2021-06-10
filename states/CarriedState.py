from Constants import *
from states.SearchState import SearchState
from states.State import State


class CarriedState(State):

    def __init__(self, agent):
        super().__init__(agent)
        self.state = CARRIED
        self.color = CARRIED_COLOR

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.leadAgent.pos)
        if self.agent.leadAgent.getState() == TRANSPORT and not \
                self.agent.agentRect.collidepoint(self.agent.leadAgent.assignedSite.pos):
            self.agent.updateFollowPosition()
        else:
            # if they arrived at a nest or the lead agent got lost and put them down or something:
            self.agent.leadAgent = None
            if self.agent.phase != COMMIT_PHASE:
                self.agent.setPhase(ASSESS_PHASE)
            self.setState(SearchState(self.agent), None)
