from Constants import *
from states.RecruitState import RecruitState
from states.TransportState import TransportState


class ReverseTandemState(RecruitState):
    """ State where a committed agent leads other committed agents to one of their previous sites to help
     recruit and then leads agent to the site they are committed to """

    def __init__(self, agent):
        super().__init__(agent)
        self.state = REVERSE_TANDEM
        self.color = REVERSE_TANDEM_COLOR

    def arriveAtSite(self):
        self.setState(TransportState(self.agent), self.agent.assignedSite.getPosition())
