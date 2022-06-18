from Constants import DEAD, DEAD_COLOR
from model.states.State import State


class DeadState(State):
    """ State where an agent has been killed by a predator and just stays in the same place till the
     end of the simulation """

    def __init__(self, agent):
        """ agent - the agent that is in this state """
        super().__init__(agent)
        self.stateNumber = DEAD

    def doStateActions(self, neighborList) -> None:
        pass

    def changeState(self, neighborList) -> None:
        pass

    def executeCommands(self):
        return True

    def toString(self):
        return "DEAD"

    def getColor(self):
        return DEAD_COLOR
