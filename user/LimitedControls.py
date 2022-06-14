from user.UIControls import UIControls


class LimitedControls(UIControls):
    """ Controls that only allow the user to do some limited actions """

    def __init__(self, agentList, world, selectRect, disp):
        super().__init__(agentList, world, selectRect, disp)

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
