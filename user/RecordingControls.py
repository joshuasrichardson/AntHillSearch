from user.Controls import Controls


class RecordingControls(Controls):

    def __init__(self, agentList, world, selectRect, disp, changeDelay):
        super().__init__(agentList, world, selectRect, disp)
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

    def speedUp(self, pos):
        self.changeDelay(-0.025)

    def slowDown(self, pos):
        self.changeDelay(0.025)

    def raiseQuality(self, pos):
        pass

    def lowerQuality(self, pos):
        pass

    def expand(self, pos):
        pass

    def shrink(self, pos):
        pass

    def createSite(self, position):
        pass

    def createAgent(self, position):
        pass

    def delete(self, pos):
        pass

    def appendNumber(self, number):
        pass

    def deleteLastDigit(self):
        pass

    def setSiteQuality(self):
        pass

    def kill(self, pos):
        pass

    def avoid(self, pos):
        pass
