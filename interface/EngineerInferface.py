from config import Config
from interface.LiveSimulation import LiveSimulation


class EngineerInterface(LiveSimulation):
    """ A class to run the simulation for ants finding their new home after the old one broke """

    def __init__(self):
        super().__init__()

    def update(self, agentRectList):
        super().update(agentRectList)
        self.userControls.moveScreen()

    def applyConfiguration(self):
        super().applyConfiguration()
        Config.INTERFACE_NAME = "Engineering"
        Config.DRAW_ESTIMATES = False
        Config.DRAW_FAR_AGENTS = True
        Config.SHOULD_DRAW_PATHS = False
