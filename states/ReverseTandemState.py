from Constants import *
from states.State import State
from states.TransportState import TransportState


class ReverseTandemState(State):

    def __init__(self, agent):
        super().__init__(agent)
        self.state = REVERSE_TANDEM
        self.color = REVERSE_TANDEM_COLOR

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.assignedSite.getPosition())
        # TODO: Lead back to a previous site to have them help transport
        self.setState(TransportState(self.agent), self.agent.assignedSite.getPosition())
