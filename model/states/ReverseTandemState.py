from Constants import *
from model.states.RecruitState import RecruitState
from model.states.TransportState import TransportState


class ReverseTandemState(RecruitState):
    """ State where a committed agent leads other committed agents to one of their previous sites to help
     recruit and then leads agent to the site they are committed to """

    def __init__(self, agent):
        """ agent - the agent that is in this state """
        super().__init__(agent)
        self.stateNumber = REVERSE_TANDEM

    def arriveAtSite(self, numNeighbors):
        self.setState(TransportState(self.agent), self.agent.getAssignedSitePosition())

    def toString(self):
        return "REVERSE_TANDEM"

    def getColor(self):
        return REVERSE_TANDEM_COLOR
