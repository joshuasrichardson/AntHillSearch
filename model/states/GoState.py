from Constants import GO, GO_COLOR
from model.states.State import State


class GoState(State):
    """ State where an agent must keep moving toward a point specified by the user until the agent gets there.
    This state is entered when the user selects an agent, points the mouse where they want the agent to go, and
    pushes the space bar """

    def __init__(self, agent):
        """ agent - the agent that is in this state """
        super().__init__(agent)
        self.stateNumber = GO
        self.destination = agent.target
        self.agent.setTarget(self.getNextCheckPoint())

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.target)
        distance = self.agent.speed
        if distance < 3:
            distance = 3
        from math import isclose
        if isclose(self.agent.pos[0], self.agent.target[0], abs_tol=distance) and\
                isclose(self.agent.pos[1], self.agent.target[1], abs_tol=distance):
            if self.agent.target == self.destination:
                from model.states.SearchState import SearchState
                self.setState(SearchState(self.agent), None)
            else:
                self.agent.setTarget(self.getNextCheckPoint())
        if self.agent.siteInRangeIndex != -1:
            self.agent.addToKnownSites(self.agent.world.siteList[self.agent.siteInRangeIndex])
            # If the site is better than the one they were assessing, they assess it instead.

    def getNextCheckPoint(self):
        if len(self.agent.checkPoints) > 0:
            return self.agent.checkPoints.pop(0)
        return self.destination

    def toString(self):
        return "GO"

    def getColor(self):
        return GO_COLOR
