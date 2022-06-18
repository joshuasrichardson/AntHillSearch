from Constants import TRANSPORT, TRANSPORT_COLOR
from model.states.RecruitState import RecruitState


class TransportState(RecruitState):
    """ State where an agent goes to a previous site and picks up any searching agent it comes in contact with
    to carry it to the site the agent is committed to """

    def __init__(self, agent):
        """ agent - the agent that is in this state """
        super().__init__(agent)
        self.stateNumber = TRANSPORT

    def arriveAtSite(self, numNeighbors):
        if self.agent.shouldKeepTransporting():
            self.agent.transportOrReverseTandem(self)
        else:
            from model.states.SearchState import SearchState
            self.setState(SearchState(self.agent), self.agent.getAssignedSitePosition())

    def toString(self):
        return "TRANSPORT"

    def getColor(self):
        return TRANSPORT_COLOR
