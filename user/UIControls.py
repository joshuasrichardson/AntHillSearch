from display.simulation.WorldDisplay import collidesWithEstimatedSite, collidesWithAgent
from user.Controls import Controls


class UIControls(Controls):

    def __init__(self, agentList, world):
        super().__init__(agentList, world)

    # def handleEvents(self):
    #     for agent in self.world.agentList:
    #         if agent.getRect().collidelist(self.world.getHubsRects()) == -1 and agent.isSelected:
    #             agent.unselect()
    #             self.selectedAgents.remove(agent)
    #             if agent is self.selectedAgent:
    #                 self.selectedAgent = None
    #     super().handleEvents()

    def collidesWithSelectable(self, mousePos, adjustedMousePos):
        return collidesWithEstimatedSite(self.world, adjustedMousePos) or \
               collidesWithAgent(self.world, adjustedMousePos) and self.byAHub(adjustedMousePos)

    def startDrag(self):
        pass

    def putDownDragSite(self):
        pass

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
