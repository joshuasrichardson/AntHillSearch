from config import Config
from interface.LiveSimulation import LiveSimulation


class EngineerInterface(LiveSimulation):
    """ A class to run the simulation for ants finding their new home after the old one broke.
     This interface allows the user to see as much as possible about what is going on in the simulation. """

    def applyConfiguration(self, numAgents=None, numSites=None, sitePositions=None, siteQualities=None):
        super().applyConfiguration()
        Config.INTERFACE_NAME = "Engineering"
        Config.DRAW_ESTIMATES = False
        Config.DRAW_FAR_AGENTS = True
        Config.SHOULD_DRAW_PATHS = False
