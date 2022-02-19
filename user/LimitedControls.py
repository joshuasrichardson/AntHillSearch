from user.UIControls import UIControls


class LimitedControls(UIControls):
    """ Controls that only allow the user to do some limited actions """

    def __init__(self, timer, agentList, world, graphs):
        super().__init__(timer, agentList, world, graphs)

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
