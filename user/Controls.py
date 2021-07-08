import numpy as np
import pygame

from colony.ColonyExceptions import GameOver


class Controls:
    """ Lets the user interact with the simulation """

    def __init__(self, timer, agentList, world):
        self.timer = timer
        self.agentList = agentList
        self.world = world
        self.selectedAgent = None
        self.selectedAgents = []
        self.selectedAgentIndex = 0
        self.selectedAgentsPositions = []
        self.selectRectCorner = None
        self.selectRect = None
        self.selectedSite = None
        self.selectedSites = []
        self.selectedSiteIndex = 0
        self.dragSite = None

    def drawChanges(self):
        if self.selectedAgent is not None:
            self.world.drawSelectedAgentInfo(self.selectedAgent)
        if self.selectedSite is not None:
            self.world.drawSelectedSiteInfo(self.selectedSite, len(self.selectedAgents) > 0, self.selectedAgentsPositions)
        if self.selectRectCorner is not None:
            self.selectRect = self.world.drawSelectRect(self.selectRectCorner, pygame.mouse.get_pos())

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.pause()
            else:
                self.handleEvent(event)

    def handleEvent(self, event):
        if self.dragSite is not None:
            self.dragSite.pos = pygame.mouse.get_pos()
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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.next()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.previous()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.raiseQuality()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.lowerQuality()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
            self.expand()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
            self.shrink()
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
        self.selectedSites = [s for s in self.world.siteList if s.siteRect.collidepoint(mousePos)]
        if len(self.selectedAgents) > 0:
            self.selectedAgent = self.selectedAgents[0]
            self.selectedAgent.select()
            self.selectedAgent.isTheSelected = True
            self.selectedAgentIndex = 0
            if self.allSelectedAgentsAssignedToSameSite():
                self.selectedSite = self.selectedAgent.assignedSite
                self.selectedSite.select()
        if len(self.selectedSites) > 0:
            self.selectedSite = self.selectedSites[0]
            self.selectedSite.select()
            self.selectedSiteIndex = 0
            self.selectedAgentsPositions = []
            for agent in self.agentList:
                if agent.assignedSite is self.selectedSite:
                    self.selectedAgentsPositions.append(agent.pos)
                    agent.select()
                    self.selectedAgents.append(agent)

    def allSelectedAgentsAssignedToSameSite(self):
        for agent in self.selectedAgents:
            if agent.assignedSite is not self.selectedAgent.assignedSite:
                return False
        return True

    def mouseUp(self, mousePos):
        self.dragSite = None
        self.selectedAgent = None
        self.selectedSite = None
        self.select(mousePos)
        if self.selectRectCorner is not None and np.abs(mousePos[0] - self.selectRectCorner[0]) > 1\
                and np.abs(mousePos[1] - self.selectRectCorner[1]) > 1:
            self.wideSelect()
        self.selectRectCorner = None

    def mouseDown(self, mousePos):
        self.selectedSites = [s for s in self.world.siteList if s.siteRect.collidepoint(mousePos)]
        if len(self.selectedSites) > 0:
            self.selectedSite = self.selectedSites[0]
            self.drag()
        else:
            self.startSelectRect(mousePos)

    def drag(self):
        self.dragSite = self.selectedSite

    def startSelectRect(self, mousePos):
        self.selectRectCorner = mousePos

    def wideSelect(self):
        # get a list of all objects that are under the mouse cursor
        self.selectedAgents = [s for s in self.agentList if s.agentRect.colliderect(self.selectRect)]
        self.selectedSites = [s for s in self.world.siteList if s.siteRect.colliderect(self.selectRect)]
        if len(self.selectedAgents) > 0:
            self.selectedAgent = self.selectedAgents[0]
            self.selectedAgent.isTheSelected = True
            self.selectedAgentIndex = 0
            if self.allSelectedAgentsAssignedToSameSite():
                self.selectedSite = self.selectedAgent.assignedSite
                self.selectedSite.select()
        if len(self.selectedSites) > 0:
            self.selectedSite = self.selectedSites[0]
            self.selectedSite.isTheSelected = True
            self.selectedSiteIndex = 0
        for a in self.selectedAgents:
            a.select()
        for s in self.selectedSites:
            s.select()

    def half(self):
        for i in range(len(self.selectedAgents) - 1, int(np.round(len(self.selectedAgents) / 2) - 1), -1):
            self.selectedAgents[i].unselect()
            self.selectedAgents.remove(self.selectedAgents[i])
        print(len(self.selectedAgents))

    def next(self):
        if len(self.selectedAgents) > 1:
            self.nextAgent()
        else:
            self.nextSite()

    def nextAgent(self):
        if len(self.selectedAgents) > 0:
            self.selectedAgentIndex += 1
            self.selectedAgent.isTheSelected = False
            self.selectedAgent = self.selectedAgents[self.selectedAgentIndex % len(self.selectedAgents)]
            self.selectedAgent.isTheSelected = True

    def nextSite(self):
        if len(self.selectedSites) > 0:
            self.selectedSiteIndex += 1
            self.selectedSite = self.selectedSites[self.selectedSiteIndex % len(self.selectedSites)]

    def previous(self):
        if len(self.selectedAgents) > 1:
            self.previousAgent()
        else:
            self.previousSite()

    def previousAgent(self):
        if len(self.selectedAgents) > 0:
            self.selectedAgentIndex -= 1
            self.selectedAgent.isTheSelected = False
            self.selectedAgent = self.selectedAgents[self.selectedAgentIndex % len(self.selectedAgents)]
            self.selectedAgent.isTheSelected = True

    def previousSite(self):
        if len(self.selectedSites) > 0:
            self.selectedSiteIndex -= 1
            self.selectedSite = self.selectedSites[self.selectedSiteIndex % len(self.selectedSites)]

    def go(self, mousePos):
        print(str(mousePos))
        for a in self.selectedAgents:
            a.target = mousePos
            from states.GoState import GoState
            a.setState(GoState(a))

    def assignSelectedAgents(self, mousePos):
        sitesUnderMouse = [s for s in self.world.siteList if s.siteRect.collidepoint(mousePos)]
        if len(sitesUnderMouse) > 0:
            for a in self.selectedAgents:
                a.assignSite(sitesUnderMouse[0])

    def speedUp(self):
        for a in self.agentList:
            a.speed *= 1.2
            a.speedCoefficient *= 1.2

    def slowDown(self):
        for a in self.agentList:
            a.speed /= 1.2
            a.speedCoefficient /= 1.2

    def raiseQuality(self):
        for site in self.selectedSites:
            if site.quality < 255:
                site.quality += 1
                site.color = 255 - site.quality, site.quality, 0

    def lowerQuality(self):
        for site in self.selectedSites:
            if site.quality > 0:
                site.quality -= 1
                site.color = 255 - site.quality, site.quality, 0

    def expand(self):
        for site in self.selectedSites:
            site.radius += 1

    def shrink(self):
        for site in self.selectedSites:
            site.radius -= 1

    def pause(self):
        self.world.drawPause()
        pygame.display.flip()
        self.timer.pause(self.handleEvent)
