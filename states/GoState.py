from Constants import GO, GO_COLOR
from states.State import State


class GoState(State):
    """ State where an agent must keep moving toward a point specified by the user until the agent gets there.
    This state is entered when the user selects an agent, points the mouse where they want the agent to go, and
    pushes the space bar """

    def __init__(self, agent):
        super().__init__(agent)
        self.state = GO
        self.color = GO_COLOR

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.target)
        distance = self.agent.speed
        if distance < 3:
            distance = 3
        from math import isclose
        if isclose(self.agent.pos[0], self.agent.target[0], abs_tol=distance) and\
                isclose(self.agent.pos[1], self.agent.target[1], abs_tol=distance):
            from states.SearchState import SearchState
            self.setState(SearchState(self.agent), None)
