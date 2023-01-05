from config import Config
from interface.LiveSimulation import LiveSimulation
from user.LimitedControls import LimitedControls
from user.UIControls import UIControls


class UserInterface(LiveSimulation):
    """ A class to run the simulation for ants finding their new home after the old one broke.
     This interface gives the user the perspective of only knowing what could be known from the hub.
     For example, none of the site or agent positions are known, until agents come back and report them. """

    def __init__(self):
        super().__init__()

    def getControls(self):
        if Config.FULL_CONTROL:
            return UIControls(self.world.agentList, self.world, self.simDisp)
        return LimitedControls(self.world.agentList, self.world, self.simDisp)

    def applyConfiguration(self, numAgents=None, numSites=None, sitePositions=None, siteQualities=None):
        super().applyConfiguration()
        Config.INTERFACE_NAME = "User"
        Config.DRAW_ESTIMATES = True
        Config.DRAW_FAR_AGENTS = False
        Config.SHOULD_DRAW_PATHS = False
