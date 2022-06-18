from Constants import *
from model.phases.AssessPhase import AssessPhase
from model.states.AtNestState import AtNestState
from model.states.State import State


class CarriedState(State):
    """ State where an agent is being carried by a transporting committed agent toward that agent's site """

    def __init__(self, agent):
        """ agent - the agent that is in this state """
        super().__init__(agent)
        self.stateNumber = CARRIED

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.leadAgent.getPosition())
        if self.agent.leadAgent.getStateNumber() == TRANSPORT and not \
                self.agent.leadAgent.getRect().collidepoint(self.agent.leadAgent.assignedSite.pos):
            if not self.agent.world.agentList.__contains__(self.agent.leadAgent):
                from model.states.SearchState import SearchState
                self.setState(SearchState(self.agent), None)
            else:
                self.agent.updateFollowPosition()
        else:
            # if they arrived at a nest or the lead agent got lost and put them down or something:
            self.agent.addToKnownSites(self.agent.leadAgent.assignedSite)
            if self.agent.leadAgent.estimatedQuality > self.agent.estimatedQuality:
                self.agent.assignSite(self.agent.leadAgent.assignedSite)
            self.agent.leadAgent = None
            if self.agent.getPhaseNumber() != COMMIT:
                self.agent.setPhase(AssessPhase())
            self.setState(AtNestState(self.agent), self.agent.getAssignedSitePosition())

    def toString(self):
        return "CARRIED"

    def getColor(self):
        return CARRIED_COLOR
