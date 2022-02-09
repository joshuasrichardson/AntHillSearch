from config import Config
from interface.LiveSimulation import LiveSimulation


class EmpiricalTestingInterface(LiveSimulation):
    """ A class to run the interface for ants finding their new home after the old one broke """

    def __init__(self):
        super().__init__()

    def recordDisplays(self):
        if Config.SHOULD_RECORD:
            self.recorder.recordTime(self.timer.getRemainingTime())
            self.recorder.recordShouldDrawGraphs(True)
            self.recorder.recordExecutedCommands([])
            self.recorder.recordScreenBorder(None, None, None, None)

    def runNextRound(self):
        self.update(self.getAgentRectList())

    def getScreen(self):
        return None

    def getGraphs(self, numAgents):
        return None

    @staticmethod
    def drawBorder():
        pass

    def applyConfiguration(self):
        super().applyConfiguration()
        Config.INTERFACE_NAME = "emp_testing"
        Config.SHOULD_DRAW = False
