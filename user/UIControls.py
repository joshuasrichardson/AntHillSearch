from display.WorldDisplay import collidesWithEstimatedSite, collidesWithAgent
from user.Controls import Controls


class UIControls(Controls):

    def __init__(self, timer, agentList, world, graphs):
        super().__init__(timer, agentList, world, graphs)

    def handleEvents(self):
        for agent in self.world.agentList:
            if agent.getRect().collidelist(self.world.getHubsRects()) == -1 and agent.isSelected:
                agent.unselect()
                self.selectedAgents.remove(agent)
                if agent is self.selectedAgent:
                    self.selectedAgent = None
        super().handleEvents()

    def collidesWithSelectable(self, mousePos, adjustedMousePos):
        return collidesWithEstimatedSite(self.world, adjustedMousePos) or \
               collidesWithAgent(self.world, adjustedMousePos) and self.byAHub(adjustedMousePos) or \
               self.graphs.collidesWithAnyButton(mousePos, self.paused)

    def drag(self):
        pass

    def putDownDragSite(self):
        pass

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
