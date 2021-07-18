import copy
import numpy as np
from abc import ABC, abstractmethod
from Constants import SEARCH


class State(ABC):
    """ An abstract base class for the states the agents can be in """

    def __init__(self, agent):
        self.agent = agent

    def setState(self, state, target):
        self.agent.target = target
        self.move(state)
        self.agent.state = state
        if self.agent.isSelected:
            print("Set State target:" + str(target))

    def move(self, state) -> None:
        if state.state == SEARCH:  # If changing state to search from something else, set angle randomly
            self.agent.angularVelocity = 0
            self.agent.angle = np.random.uniform(0, np.pi * 2, 1)
        else:  # Move toward target
            self.agent.angle = np.arctan2(self.agent.target[1] - self.agent.pos[1], self.agent.target[0] - self.agent.pos[0])

    @abstractmethod
    def changeState(self, neighborList) -> None:
        pass

    def copy(self, agent):
        state = copy.copy(self)
        state.agent = agent
        return state
