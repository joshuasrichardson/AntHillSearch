from Constants import *
from phases.AssessPhase import AssessPhase
from states.AtNestState import AtNestState
from states.State import State


class CarriedState(State):
    """ State where an agent is being carried by a transporting committed agent toward that agent's site """

    def __init__(self, agent):
        super().__init__(agent)
        self.state = CARRIED

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.leadAgent.pos)
        if self.agent.leadAgent.getState() == TRANSPORT and not \
                self.agent.leadAgent.getAgentRect().collidepoint(self.agent.leadAgent.assignedSite.pos):
            if not self.agent.world.agentList.__contains__(self.agent.leadAgent):
                from states.SearchState import SearchState
                self.setState(SearchState(self.agent), None)
            else:
                self.agent.updateFollowPosition()
        else:
            # if they arrived at a nest or the lead agent got lost and put them down or something:
            self.agent.knownSites.add(self.agent.leadAgent.assignedSite)
            if self.agent.leadAgent.estimatedQuality > self.agent.estimatedQuality:
                self.agent.assignSite(self.agent.leadAgent.assignedSite)
            self.agent.leadAgent = None
            if self.agent.getPhaseNumber() != COMMIT:
                self.agent.setPhase(AssessPhase())
            self.setState(AtNestState(self.agent), self.agent.assignedSite.pos)

    def toString(self):
        return "CARRIED"

    def getColor(self):
        return CARRIED_COLOR
