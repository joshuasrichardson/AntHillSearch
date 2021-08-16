import numpy as np
from abc import ABC, abstractmethod
from Constants import SEARCH, AT_NEST, LEAD_FORWARD, FOLLOW, REVERSE_TANDEM, TRANSPORT, GO, CARRIED


def numToState(num, agent):
    if num == AT_NEST:
        from model.states.AtNestState import AtNestState
        return AtNestState(agent)
    if num == SEARCH:
        from model.states.SearchState import SearchState
        return SearchState(agent)
    if num == CARRIED:
        from model.states.CarriedState import CarriedState
        return CarriedState(agent)
    if num == FOLLOW:
        from model.states.FollowState import FollowState
        return FollowState(agent)
    if num == LEAD_FORWARD:
        from model.states.LeadForwardState import LeadForwardState
        return LeadForwardState(agent)
    if num == REVERSE_TANDEM:
        from model.states.ReverseTandemState import ReverseTandemState
        return ReverseTandemState(agent)
    if num == TRANSPORT:
        from model.states.TransportState import TransportState
        return TransportState(agent)
    if num == GO:
        from model.states.GoState import GoState
        return GoState(agent)


class State(ABC):
    """ An abstract base class for the states the agents can be in """

    def __init__(self, agent):
        self.agent = agent

    def setState(self, state, target):
        self.agent.target = target
        self.move(state)
        self.agent.state = state

    def move(self, state) -> None:
        if state.state == SEARCH:  # If changing state to search from something else, set angle randomly
            self.agent.angularVelocity = 0
            self.agent.setAngle(np.random.uniform(0, np.pi * 2, 1))
        else:  # Move toward target
            self.agent.setAngle(np.arctan2(self.agent.target[1] - self.agent.pos[1], self.agent.target[0] - self.agent.pos[0]))

    @abstractmethod
    def changeState(self, neighborList) -> None:
        pass

    @abstractmethod
    def toString(self):
        pass

    @abstractmethod
    def getColor(self):
        pass