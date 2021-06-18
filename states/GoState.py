from Constants import GO, GO_COLOR
from states.State import State


class GoState(State):

    def __init__(self, agent):
        super().__init__(agent)
        self.state = GO
        self.color = GO_COLOR

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.target)
        from math import isclose
        if isclose(self.agent.pos[0], self.agent.target[0], abs_tol=3) and\
                isclose(self.agent.pos[1], self.agent.target[1], abs_tol=3):
            from states.SearchState import SearchState
            self.setState(SearchState(self.agent), None)
