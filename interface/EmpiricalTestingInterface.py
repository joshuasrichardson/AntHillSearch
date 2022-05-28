from config import Config
from interface.LiveSimulation import LiveSimulation


class EmpiricalTestingInterface(LiveSimulation):
    """ A class to run the interface for ants finding their new home after the old one broke """

    def __init__(self):
        super().__init__()

    def recordDisplays(self):
        if Config.SHOULD_RECORD:
            self.recorder.recordTime(self.timer.getRemainingTimeOrRounds())

    def runNextRound(self):
        self.update(self.getAgentRectList())
        self.timer.nextRound()

    def getScreen(self):
        return None

    def applyConfiguration(self):
        super().applyConfiguration()
        Config.INTERFACE_NAME = "Empirical_Testing"
        Config.SHOULD_DRAW = False
