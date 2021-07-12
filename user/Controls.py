import random

import numpy as np
import pygame

from Constants import DEFAULT_SITE_SIZE, EXPLORE
from colony.Agents import Agent
from colony.ColonyExceptions import GameOver
from states.SearchState import SearchState


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
        self.oldRect = None
        self.potentialQuality = 0
        self.shouldDrawQuality = False

    def drawChanges(self):
        if self.selectedAgent is not None:
            self.world.drawSelectedAgentInfo(self.selectedAgent)
        if self.selectedSite is not None:
            self.world.drawSelectedSiteInfo(self.selectedSite, len(self.selectedAgents) > 0, self.selectedAgentsPositions)
            if self.shouldDrawQuality:
                self.world.drawPotentialQuality(self.potentialQuality)
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
            self.dragSite.setPosition(pygame.mouse.get_pos())
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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            self.createSite(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            self.createAgent(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
            self.delete()
        if len(self.selectedSites) > 0:
            if event.type == pygame.KEYDOWN and event.unicode.isnumeric():
                self.appendNumber(int(event.unicode))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                self.deleteLastDigit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.setSiteQuality()
        else:
            self.potentialQuality = 0
            self.shouldDrawQuality = False
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
            if len(self.selectedAgents) > 0:
                self.selectedAgent = self.selectedAgents[0]
                self.selectedAgent.isTheSelected = True

    def allSelectedAgentsAssignedToSameSite(self):
        for agent in self.selectedAgents:
            if agent.assignedSite is not self.selectedAgent.assignedSite:
                return False
        return True

    def mouseUp(self, mousePos):
        if self.dragSite is not None:
            print("Old Rect: " + str(self.oldRect))
            print("Drag Rect: " + str(self.dragSite.getSiteRect()))
            print("Old site rect list: " + str(self.world.siteRectList))
            self.world.siteRectList = [self.dragSite.getSiteRect() if r is self.oldRect else r for r in self.world.siteRectList]
            print("New site rect list: " + str(self.world.siteRectList))
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
        self.oldRect = self.selectedSite.getSiteRect()
        self.dragSite = self.selectedSite

    def startSelectRect(self, mousePos):
        self.selectRectCorner = mousePos

    def wideSelect(self):
        # get a list of all objects that are under the mouse cursor
        self.selectRect = self.world.drawSelectRect(self.selectRectCorner, pygame.mouse.get_pos())
        self.selectedAgents = [a for a in self.agentList if a.agentRect.colliderect(self.selectRect)]
        self.selectedSites = [s for s in self.world.siteList if s.siteRect.colliderect(self.selectRect)]

        for a in self.selectedAgents:
            a.select()
        for s in self.selectedSites:
            s.select()

        if len(self.selectedSites) > 0:
            self.selectedSite = self.selectedSites[0]
            self.selectedSite.isTheSelected = True
            self.selectedSiteIndex = 0
            self.selectedAgentsPositions = []
            for agent in self.agentList:
                if agent.assignedSite.isSelected:
                    self.selectedAgentsPositions.append(agent.pos)
                    agent.select()
                    self.selectedAgents.append(agent)

        if len(self.selectedAgents) > 0:
            self.selectedAgent = self.selectedAgents[0]
            self.selectedAgent.isTheSelected = True
            self.selectedAgentIndex = 0
            if self.allSelectedAgentsAssignedToSameSite():
                self.selectedSite = self.selectedAgent.assignedSite
                self.selectedSite.select()

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

    def createSite(self, position):
        self.world.createSite(position[0], position[1], DEFAULT_SITE_SIZE, 255 / 2)
        self.world.numSites += 1

    def createAgent(self, position):
        agent = Agent(self.world)
        agent.setState(SearchState(agent))
        agent.setPosition(position[0], position[1])
        agent.angle = random.uniform(0, 2 * np.pi)
        agent.assignedSite.incrementCount()
        self.world.addAgent(agent)

    def delete(self):
        self.deleteSelectedSites()
        self.deleteSelectedAgents()

    def deleteSelectedSites(self):
        print("All sites: " + str(self.selectedSites))
        i = 0
        while len(self.selectedSites) > 0:
            site = self.selectedSites[i]
            print("Deleting: " + str(site))
            for agent in self.agentList:
                agent.siteObserveRectList = self.world.siteRectList
                if agent.assignedSite is site and site is not self.world.hub:
                    agent.assignSite(self.world.hub)
                    agent.setPhase(EXPLORE)
                    agent.setState(SearchState(agent))
                if agent.knownSites.__contains__(site) and site is not self.world.hub:
                    agent.knownSites.remove(site)
            self.world.removeSite(site)
            self.selectedSites.remove(site)
        self.selectedSite = None

    def deleteSelectedAgents(self):
        self.world.deleteSelectedAgents()

    def appendNumber(self, number):
        if self.potentialQuality == 0 or self.potentialQuality > 25 or (self.potentialQuality == 25 and number > 5):
            self.potentialQuality = number
        else:
            self.potentialQuality *= 10
            self.potentialQuality += number
        self.shouldDrawQuality = True

    def deleteLastDigit(self):
        if self.potentialQuality < 10:
            self.shouldDrawQuality = False
        self.potentialQuality = int(self.potentialQuality / 10)

    def setSiteQuality(self):
        for site in self.selectedSites:
            print("Set quality of " + str(site) + " to " + str(self.potentialQuality))
            site.setQuality(self.potentialQuality)
            site.setColor(self.potentialQuality)

    def pause(self):
        self.world.drawPause()
        pygame.display.flip()
        self.timer.pause(self.handleEvent)
