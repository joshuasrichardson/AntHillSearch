from Constants import DEAD, DEAD_COLOR
from model.states.State import State


class DeadState(State):
    """ State where an agent has been killed by a predator and just stays in the same place till the
     end of the simulation """

    def __init__(self, agent):
        super().__init__(agent)
        self.stateNumber = DEAD

    def changeState(self, neighborList) -> None:
        pass

    def executeCommand(self):
        return True

    def toString(self):
        return "DEAD"

    def getColor(self):
        return DEAD_COLOR
