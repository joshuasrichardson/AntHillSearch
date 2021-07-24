import random

import numpy as np
import pygame

from Constants import SITE_RADIUS, SCREEN_COLOR
from colony.Agents import Agent
from colony.ColonyExceptions import GameOver
from phases.ExplorePhase import ExplorePhase
from states.SearchState import SearchState


# TODO: Break into multiple classes (such as AgentControls, SiteControls and Controls)


class Controls:
    """ Lets the user interact with the simulation """

    def __init__(self, timer, agentList, world, graphs):
        self.graphs = graphs
        self.timer = timer
        self.agentList = agentList
        self.world = world
        self.selectedAgent = None
        self.selectedAgents = []
        self.selectedAgentIndex = 0
        self.selectedSitesAgentsPositions = []
        self.selectRectCorner = None
        self.selectRect = None
        self.selectedSite = None
        self.selectedSites = []
        self.selectedSiteIndex = 0
        self.dragSite = None
        self.oldRect = None
        self.potentialQuality = 0
        self.shouldDrawQuality = False
        self.shouldSelectAgents = True
        self.shouldSelectSites = True
        self.shouldSelectSiteAgents = False
        self.shouldSelectAgentSites = False
        self.paused = False
        self.shouldShowOptions = False

    def draw(self):
        self.world.screen.fill(SCREEN_COLOR)
        self.graphs.drawStateGraph(self.world.states)
        self.graphs.drawPhaseGraph(self.world.phases)
        self.graphs.drawPredictionsGraph(self.world.siteList)
        self.world.drawWorldObjects()
        self.drawChanges()
        for agent in self.world.agentList:
            agent.drawAgent(self.world.screen)
        self.graphs.drawPause()
        if self.shouldShowOptions:
            self.graphs.drawOptions()
        pygame.display.flip()

    def drawChanges(self):
        if self.selectedAgent is not None:
            self.graphs.drawSelectedAgentInfo(self.selectedAgent)
        if self.selectedSite is not None:
            self.graphs.drawSelectedSiteInfo(self.selectedSite, self.selectedSitesAgentsPositions)
            if self.shouldDrawQuality:
                self.world.drawPotentialQuality(self.potentialQuality)
        if self.selectRectCorner is not None:
            self.selectRect = self.drawSelectRect(pygame.mouse.get_pos())
        self.graphs.drawSelectionOptions(self.shouldSelectAgents, self.shouldSelectSites, self.shouldSelectSiteAgents,
                                         self.shouldSelectAgentSites, self.shouldShowOptions, self.paused)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.pause()
            else:
                self.handleEvent(event)

    def handleEvent(self, event):
        if self.dragSite is not None:
            self.world.setSitePosition(self.dragSite, pygame.mouse.get_pos())
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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            self.createAgent(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE \
                or event.type == pygame.KEYDOWN and event.key == pygame.K_SLASH:
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
        if self.paused:
            self.draw()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                self.shouldShowOptions = not self.shouldShowOptions
        if event.type == pygame.QUIT:
            pygame.quit()
            self.timer.cancel()
            raise GameOver("Exited Successfully")

    def mouseUp(self, mousePos):
        if self.dragSite is not None:
            if self.dragSite.getSiteRect != self.oldRect:
                self.dragSite.wasFound = False
            self.world.siteRectList = [self.dragSite.getSiteRect() if r is self.oldRect else r for r in self.world.siteRectList]
        self.dragSite = None
        self.selectedAgent = None
        self.selectedSite = None
        self.unselectAll()
        if self.selectRectCorner is not None and np.abs(mousePos[0] - self.selectRectCorner[0]) > 1\
                and np.abs(mousePos[1] - self.selectRectCorner[1]) > 1:
            self.wideSelect()
        elif self.graphs.collidesWithSelectAgentsButton(mousePos):
            self.shouldSelectAgents = not self.shouldSelectAgents
        elif self.graphs.collidesWithSelectSitesButton(mousePos):
            self.shouldSelectSites = not self.shouldSelectSites
        elif self.graphs.collidesWithSelectAgentsSitesButton(mousePos):
            self.shouldSelectAgentSites = not self.shouldSelectAgentSites
        elif self.graphs.collidesWithSelectSitesAgentsButton(mousePos):
            self.shouldSelectSiteAgents = not self.shouldSelectSiteAgents
        elif self.graphs.collidesWithOptionsButton(mousePos):
            self.shouldShowOptions = not self.shouldShowOptions
        else:
            self.select(mousePos)
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

    def unselectAll(self):
        # Unselect all agents and sites
        for a in self.agentList:
            a.unselect()
        for s in self.world.siteList:
            s.unselect()
        self.selectedAgents = []
        self.selectedSites = []
        self.selectedSitesAgentsPositions = []

    def select(self, mousePos):
        # get a list of all objects that are under the mouse cursor
        self.selectAgent(mousePos)
        self.selectSite(mousePos)

    def selectAgent(self, mousePos):
        selectedAgents = [a for a in self.agentList if a.getAgentRect().collidepoint(mousePos)]

        if len(selectedAgents) > 0:
            if self.shouldSelectAgents:
                self.selectedAgent = selectedAgents[0]
                self.selectedAgent.select()
                self.selectedAgent.isTheSelected = True
                self.selectedAgents = [self.selectedAgent]
                self.selectedAgentIndex = 0
            if self.shouldSelectAgentSites:
                self.selectedSite = selectedAgents[0].assignedSite
                self.selectedSite.select()
                self.selectedSite.isTheSelected = True

    def selectSite(self, mousePos):
        selectedSites = [s for s in self.world.siteList if s.siteRect.collidepoint(mousePos)]

        if len(selectedSites) > 0:
            if self.shouldSelectSites:
                self.selectedSite = selectedSites[0]
                self.selectedSite.select()
                self.selectedSites = [self.selectedSite]
            self.selectSite2()
            if len(self.selectedAgents) > 0:
                self.selectedAgent = self.selectedAgents[0]
                self.selectedAgent.isTheSelected = True

    def startSelectRect(self, mousePos):
        self.selectRectCorner = mousePos

    def wideSelect(self):
        # get a list of all objects that are under the mouse cursor
        self.selectRect = self.drawSelectRect(pygame.mouse.get_pos())
        agent = self.selectAgents()
        self.selectSites()
        if self.shouldSelectAgentSites:
            self.selectAgentsSite(agent)

    def drawSelectRect(self, mousePos):
        if self.selectRectCorner[0] < mousePos[0]:
            left = self.selectRectCorner[0]
        else:
            left = mousePos[0]
        if self.selectRectCorner[1] < mousePos[1]:
            top = self.selectRectCorner[1]
        else:
            top = mousePos[1]
        width = np.abs(self.selectRectCorner[0] - mousePos[0])
        height = np.abs(self.selectRectCorner[1] - mousePos[1])
        return pygame.draw.rect(self.world.screen, (128, 128, 128), pygame.Rect(left, top, width, height))

    def selectAgents(self):
        selectedAgents = [a for a in self.agentList if a.getAgentRect().colliderect(self.selectRect)]
        if self.shouldSelectAgents:
            self.selectedAgents = selectedAgents

        for a in self.selectedAgents:
            a.select()

        if len(self.selectedAgents) > 0:
            self.selectedAgent = self.selectedAgents[0]
            self.selectedAgent.isTheSelected = True
            self.selectedAgentIndex = 0

        if len(selectedAgents) > 0:
            return selectedAgents[0]

        return None

    def selectSites(self):
        selectedSites = [s for s in self.world.siteList if s.siteRect.colliderect(self.selectRect)]
        if self.shouldSelectSites:
            self.selectedSites = selectedSites

        for s in self.selectedSites:
            s.select()

        if len(selectedSites) > 0:
            self.selectedSite = selectedSites[0]
            self.selectSite2()

    def selectSite2(self):
        if self.shouldSelectSites:
            self.selectedSite.isTheSelected = True
            self.selectedSiteIndex = 0
            self.selectedSitesAgentsPositions = []
        for agent in self.agentList:
            if agent.assignedSite is self.selectedSite:
                self.selectedSitesAgentsPositions.append(agent.pos)
                if self.shouldSelectSiteAgents:
                    agent.select()
                    self.selectedAgents.append(agent)
        if self.shouldSelectSiteAgents and len(self.selectedAgents) > 0:
            self.selectedAgent = self.selectedAgents[0]
            self.selectedAgent.isTheSelected = True
        if not self.shouldSelectSites:
            self.selectedSite = None
            self.selectedSitesAgentsPositions = []

    def selectAgentsSite(self, agent):
        if agent is not None:
            self.selectedSite = agent.assignedSite
            self.selectedSite.isTheSelected = True
            self.selectedSite.select()

    def half(self):
        for i in range(len(self.selectedAgents) - 1, int(np.round(len(self.selectedAgents) / 2) - 1), -1):
            if self.selectedAgents[i] is not self.selectedAgent:
                self.selectedAgents[i].unselect()
                self.selectedAgents.remove(self.selectedAgents[i])

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
            self.updateSelectedSitesAgentsPositions()

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
            self.updateSelectedSitesAgentsPositions()

    def updateSelectedSitesAgentsPositions(self):
        self.selectedSitesAgentsPositions = []
        for agent in self.agentList:
            if agent.assignedSite is self.selectedSite:
                self.selectedSitesAgentsPositions.append(agent.pos)

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
                a.addToKnownSites(sitesUnderMouse[0])
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
        self.world.createSite(position[0], position[1], SITE_RADIUS, 256 / 2)

    def createAgent(self, position):
        agent = Agent(self.world, self.world.getHub(), startingPosition=position)
        agent.setState(SearchState(agent))
        agent.angle = random.uniform(0, 2 * np.pi)
        agent.assignedSite.incrementCount()
        self.world.addAgent(agent)

    def delete(self):
        self.deleteSelectedSites()
        self.deleteSelectedAgents()

    def deleteSelectedSites(self):
        i = 0
        while len(self.selectedSites) > 0:
            site = self.selectedSites[i]
            print("Deleting: " + str(site))
            for agent in self.agentList:
                if agent.assignedSite is site and site is not self.world.getHub():
                    agent.assignSite(self.world.getHub())
                    agent.setPhase(ExplorePhase())
                    agent.setState(SearchState(agent))
                if agent.knownSites.__contains__(site) and site is not self.world.getHub():
                    agent.knownSites.remove(site)
            self.world.removeSite(site)
            self.selectedSites.remove(site)
        self.selectedSite = None

    def deleteSelectedAgents(self):
        self.world.deleteSelectedAgents()
        self.selectedAgents = []
        self.selectedAgent = None

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
        self.graphs.drawPause()
        pygame.display.flip()
        self.paused = True
        self.timer.pause(self.handleEvent)
        self.paused = False
