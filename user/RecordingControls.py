from user.Controls import Controls


class RecordingControls(Controls):

    def __init__(self, timer, agentList, world, graphs, changeDelay):
        super().__init__(timer, agentList, world, graphs)
        self.changeDelay = changeDelay

    def startDrag(self):
        pass

    def putDownDragSite(self):
        pass

    def go(self, mousePos):
        pass

    def setSelectedSitesCommand(self, command, arg, marker, markerName):
        pass

    def assignSelectedAgents(self, mousePos):
        pass

    def speedUp(self):
        self.changeDelay(-0.025)

    def slowDown(self):
        self.changeDelay(0.025)

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

    def kill(self):
        pass

    def avoid(self, pos):
        pass
