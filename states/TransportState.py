from Constants import *
from states.RecruitState import RecruitState


class TransportState(RecruitState):
    """ State where an agent goes to a previous site and picks up any searching agent it comes in contact with
    to carry it to the site the agent is committed to """

    def __init__(self, agent):
        super().__init__(agent)
        self.state = TRANSPORT

    def arriveAtSite(self):
        if self.agent.shouldKeepTransporting():
            self.agent.transportOrReverseTandem(self)
        else:
            from states.SearchState import SearchState
            self.setState(SearchState(self.agent), self.agent.getAssignedSitePosition())

    def toString(self):
        return "TRANSPORT"

    def getColor(self):
        return TRANSPORT_COLOR
