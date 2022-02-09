from config import Config
from display.Graphs import SimulationGraphs
from interface.LiveSimulation import LiveSimulation


class EngineerInterface(LiveSimulation):
    """ A class to run the simulation for ants finding their new home after the old one broke """

    def __init__(self):
        super().__init__()

    def update(self, agentRectList):
        self.graphs.setRemainingTime(self.timer.getRemainingTime())
        super().update(agentRectList)
        self.userControls.moveScreen()

    def getGraphs(self, numAgents):
        return SimulationGraphs(numAgents)

    def applyConfiguration(self):
        super().applyConfiguration()
        Config.INTERFACE_NAME = "engineering"
        Config.DRAW_ESTIMATES = False
        Config.DRAW_FAR_AGENTS = True
        Config.SHOULD_DRAW_PATHS = False
