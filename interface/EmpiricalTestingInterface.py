from config import Config
from interface.LiveSimulation import LiveSimulation


class EmpiricalTestingInterface(LiveSimulation):
    """ A class to run the simulation for ants finding their new home after the old one broke without drawing
     anything on the screen. The results are simply printed out at the end of each simulation """

    def __init__(self, resultsFileName=None, numAgents=None, numSites=None, sitePositions=None, siteQualities=None):
        super().__init__(numAgents, numSites, sitePositions, siteQualities)
        Config.RESULTS_FILE_NAME = resultsFileName

    def recordDisplays(self):
        if Config.SHOULD_RECORD:
            self.recorder.recordTime(self.timer.getRemainingTimeOrRounds())

    def save(self):
        if not Config.ONLY_RECORD_LAST:
            super().save()

    def runNextRound(self):
        self.update(self.getAgentRectList())
        self.timer.nextRound()

    def getScreen(self):
        return None

    def applyConfiguration(self, numAgents=None, numSites=None, sitePositions=None, siteQualities=None):
        Config.HUB_AGENT_COUNTS = numAgents
        Config.NUM_SITES = numSites
        Config.SITE_POSITIONS = sitePositions
        Config.SITE_QUALITIES = siteQualities
        Config.INTERFACE_NAME = "Empirical_Testing"
        Config.SHOULD_DRAW = False
