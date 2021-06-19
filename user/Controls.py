
import numpy as np
import pygame

from colony.ColonyExceptions import GameOver


class Controls:

    def __init__(self, timer, agentList, world):
        self.timer = timer
        self.agentList = agentList
        self.world = world
        self.selectedAgents = []
        self.selectedAgentsPositions = []
        self.selectRectCorner = None
        self.selectRect = None
        self.clickedSites = []
        self.dragSite = None

    def drawChanges(self):
        if len(self.selectedAgents) > 0:
            self.world.drawSelectedAgentInfo(self.selectedAgents[0])
        if len(self.clickedSites) > 0:
            self.world.drawSelectedSiteInfo(self.clickedSites[0], len(self.selectedAgents) > 0, self.selectedAgentsPositions)
        if self.selectRectCorner is not None:
            self.selectRect = self.world.drawSelectRect(self.selectRectCorner, pygame.mouse.get_pos())

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.pause()
            else:
                self.handleEvent(event)
            if self.dragSite is not None:
                self.dragSite.pos = pygame.mouse.get_pos()

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.mouseUp(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouseDown(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.go(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            self.go(pygame.mouse.get_pos())
            self.assignSelectedAgents(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            self.speedUp()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            self.slowDown()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
            self.half()
        if event.type == pygame.QUIT:
            pygame.quit()
            self.timer.cancel()
            raise GameOver("Exited Successfully")

    def select(self, mousePos):
        # Unselect all agents and sites
        for a in self.agentList:
            a.unselect()
        for s in self.world.siteList:
            s.unselect()
        # get a list of all objects that are under the mouse cursor
        self.selectedAgents = [s for s in self.agentList if s.agentRect.collidepoint(mousePos)]
        self.clickedSites = [s for s in self.world.siteList if s.siteRect.collidepoint(mousePos)]
        if len(self.selectedAgents) > 0:
            self.selectedAgents[0].select()
            print(self.selectedAgents[0])
        if len(self.clickedSites) > 0:
            self.clickedSites[0].select()
            self.selectedAgentsPositions = []
            for agent in self.agentList:
                if agent.assignedSite is self.clickedSites[0]:
                    self.selectedAgentsPositions.append(agent.pos)
                    agent.select()
                    self.selectedAgents.append(agent)

    def mouseUp(self, mousePos):
        self.dragSite = None
        self.select(mousePos)
        if self.selectRectCorner is not None and np.abs(mousePos[0] - self.selectRectCorner[0]) > 1\
                and np.abs(mousePos[1] - self.selectRectCorner[1]) > 1:
            self.wideSelect()
        self.selectRectCorner = None

    def mouseDown(self, mousePos):
        self.clickedSites = [s for s in self.world.siteList if s.siteRect.collidepoint(mousePos)]
        if len(self.clickedSites) > 0:
            self.drag()
        else:
            self.startSelectRect(mousePos)

    def drag(self):
        self.dragSite = self.clickedSites[0]

    def startSelectRect(self, mousePos):
        self.selectRectCorner = mousePos

    def wideSelect(self):
        # get a list of all objects that are under the mouse cursor
        self.selectedAgents = [s for s in self.agentList if s.agentRect.colliderect(self.selectRect)]
        self.clickedSites = [s for s in self.world.siteList if s.siteRect.colliderect(self.selectRect)]
        for a in self.selectedAgents:
            a.select()
        for s in self.clickedSites:
            s.select()

    def half(self):
        for i in range(len(self.selectedAgents) - 1, int(np.round(len(self.selectedAgents) / 2) - 1), -1):
            self.selectedAgents[i].unselect()
            self.selectedAgents.remove(self.selectedAgents[i])
            print(len(self.selectedAgents))

    def go(self, mousePos):
        print(str(mousePos))
        for a in self.agentList:
            if a.isSelected:
                a.target = mousePos
                from states.GoState import GoState
                a.setState(GoState(a))

    def assignSelectedAgents(self, mousePos):
        sitesUnderMouse = [s for s in self.world.siteList if s.siteRect.collidepoint(mousePos)]
        if len(sitesUnderMouse) > 0:
            for a in self.agentList:
                if a.isSelected:
                    a.assignSite(sitesUnderMouse[0])

    def speedUp(self):
        for a in self.agentList:
            a.speed *= 1.2
            a.speedCoefficient *= 1.2

    def slowDown(self):
        for a in self.agentList:
            a.speed /= 1.2
            a.speedCoefficient /= 1.2

    def pause(self):
        self.world.drawPause()
        pygame.display.flip()
        self.timer.pause(self.handleEvent)
