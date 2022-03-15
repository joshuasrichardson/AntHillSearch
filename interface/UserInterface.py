from config import Config
from Constants import UI_CONTROL_OPTIONS
from display.Graphs import SimulationGraphs
from interface.LiveSimulation import LiveSimulation
from user.LimitedControls import LimitedControls
from user.UIControls import UIControls


class UserInterface(LiveSimulation):
    """ A class to run the interface for ants finding their new home after the old one broke """

    def __init__(self):
        super().__init__()

    def update(self, agentRectList):
        self.graphs.setRemainingTime(self.getNumRounds())
        super().update(agentRectList)
        self.userControls.moveScreen()

    def getGraphs(self, numAgents):
        return SimulationGraphs(numAgents, UI_CONTROL_OPTIONS)

    def getControls(self):
        if Config.FULL_CONTROL:
            return UIControls(self.timer, self.world.agentList, self.world, self.graphs)
        return LimitedControls(self.timer, self.world.agentList, self.world, self.graphs)

    def applyConfiguration(self):
        super().applyConfiguration()
        Config.INTERFACE_NAME = "User"
        Config.DRAW_ESTIMATES = True
        Config.DRAW_FAR_AGENTS = False
        Config.SHOULD_DRAW_PATHS = False
