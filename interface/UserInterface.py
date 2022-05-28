from config import Config
from interface.LiveSimulation import LiveSimulation
from user.LimitedControls import LimitedControls
from user.UIControls import UIControls


class UserInterface(LiveSimulation):
    """ A class to run the interface for ants finding their new home after the old one broke """

    def __init__(self):
        super().__init__()

    # def update(self, agentRectList):
    #     super().update(agentRectList)
    #     self.userControls.moveScreen()

    def getControls(self):
        if Config.FULL_CONTROL:
            return UIControls(self.world.agentList, self.world)
        return LimitedControls(self.world.agentList, self.world)

    def applyConfiguration(self):
        super().applyConfiguration()
        Config.INTERFACE_NAME = "User"
        Config.DRAW_ESTIMATES = True
        Config.DRAW_FAR_AGENTS = False
        Config.SHOULD_DRAW_PATHS = False
