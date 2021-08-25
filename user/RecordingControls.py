from user.Controls import Controls


class RecordingControls(Controls):

    def __init__(self, timer, agentList, world, graphs):
        super().__init__(timer, agentList, world, graphs)

    def drag(self):
        pass

    def putDownDragSite(self):
        pass

    def go(self, mousePos):
        pass

    def setSelectedSitesCommand(self, command, mousePos, marker):
        pass

    def assignSelectedAgents(self, mousePos):
        pass

    def speedUp(self):
        pass  # TODO: Speed up the recording

    def slowDown(self):
        pass  # TODO: Slow down the recording

    def raiseQuality(self):
        pass

    def lowerQuality(self):
        pass

    def expand(self):
        pass

    def shrink(self):
        pass

    def createSite(self, position):
        pass

    def createAgent(self, position):
        pass

    def delete(self):
        pass

    def appendNumber(self, number):
        pass

    def deleteLastDigit(self):
        pass

    def setSiteQuality(self):
        pass
