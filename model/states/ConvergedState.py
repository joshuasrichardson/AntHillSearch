from Constants import CONVERGED, CONVERGED_COLOR
from model.states.State import State


class ConvergedState(State):

    def __init__(self, agent):
        super().__init__(agent)
        self.state = CONVERGED

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.target)

    def toString(self):
        return "CONVERGED"

    def getColor(self):
        return CONVERGED_COLOR
