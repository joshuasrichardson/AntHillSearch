from user.UIControls import UIControls


class LimitedControls(UIControls):
    """ Controls that only allow the user to do some limited actions """

    def __init__(self, agentList, world,  disp):
        """ agentList - a list of all the agents in the simulation
        world - the world with objects for the user to interact with
        selectRect - the rectangle used to select agents and sites
        disp - the display for the simulation that handles drawing things on the screen """
        super().__init__(agentList, world,  disp)

    def go(self, mousePos):
        """ Go is the only command the limited users can use on the agents """
        super().go(mousePos)

    def assignSelectedAgents(self, mousePos):
        pass

    def addCheckPoint(self, mousePos):
        pass

    def avoid(self, pos):
        pass

    def setAgentsStates(self, key):
        pass
