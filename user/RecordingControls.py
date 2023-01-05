from user.Controls import Controls


class RecordingControls(Controls):

    def __init__(self, agentList, world, disp, changeDelay):
        """ agentList - a list of all the agents in the simulation
        world - the world with objects for the user to interact with
        selectRect - the rectangle used to select agents and sites
        disp - the display for the simulation that handles drawing things on the screen
        changeDelay - a function used to change how much time is added between each round of the simulation """
        super().__init__(agentList, world, disp)
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

    def addCheckPoint(self, mousePos):
        pass
