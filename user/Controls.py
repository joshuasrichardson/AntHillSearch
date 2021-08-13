import random
from datetime import datetime

import numpy as np
import pygame
from pygame.constants import *

from Constants import SITE_RADIUS, SCREEN_COLOR, BORDER_COLOR, HUB_OBSERVE_DIST
from display import Display
from display.AgentDisplay import drawAgent
from display.WorldDisplay import drawWorldObjects, collidesWithSite, collidesWithAgent, drawPotentialQuality
from model.Agent import Agent
from ColonyExceptions import GameOver
from display.Display import getDestinationMarker
from model.phases.ExplorePhase import ExplorePhase
from model.states.SearchState import SearchState


class Controls:
    """ Lets the user interact with the interface """

    def __init__(self, timer, agentList, world, graphs):
        self.graphs = graphs
        self.timer = timer
        self.agentList = agentList
        self.world = world
        self.selectedAgent = None
        self.selectedAgents = []
        self.selectedAgentIndex = 0
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
        self.shouldCommandSiteAgents = False
        self.paused = False
        self.shouldShowOptions = False
        self.shouldMoveHistBoxTop = False

    def draw(self):
        Display.screen.fill(SCREEN_COLOR)
        drawWorldObjects(self.world)
        self.graphs.drawStateGraph(self.world.states)
        self.graphs.drawPhaseGraph(self.world.phases)
        self.graphs.drawPredictionsGraph(self.world.siteList)
        self.graphs.drawExecutedCommands()
        self.graphs.drawRemainingTime()
        self.graphs.drawPlayButton()
        self.drawChanges()
        for agent in self.world.agentList:
            drawAgent(agent, Display.screen)
        Display.drawPause(Display.screen)
        if self.shouldShowOptions:
            self.graphs.drawOptions()
        pygame.display.flip()

    def drawChanges(self):
        if self.selectedSite is not None and self.shouldDrawQuality:
            drawPotentialQuality(self.world, self.potentialQuality, self.graphs.font)
        if self.selectRectCorner is not None:
            self.selectRect = self.drawSelectRect(pygame.mouse.get_pos())
        self.graphs.drawSelectionOptions(self.shouldSelectAgents, self.shouldSelectSites, self.shouldSelectSiteAgents,
                                         self.shouldSelectAgentSites, self.shouldCommandSiteAgents, self.shouldShowOptions,
                                         self.paused)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_p:
                self.pause()
            else:
                self.handleEvent(event)

    def handleEvent(self, event):
        mousePos = pygame.mouse.get_pos()
        if self.dragSite is not None:
            self.world.setSitePosition(self.dragSite, mousePos)
        if self.shouldMoveHistBoxTop:
            self.graphs.setHistBoxTop(mousePos[1])
        if event.type == MOUSEMOTION:
            self.mouseMotion(mousePos)
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.mouseUp(mousePos)
            elif event.button == 3:
                self.go(mousePos)
            else:
                self.scroll(event)
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.mouseDown(mousePos)
        elif event.type == KEYDOWN:
            key = event.key
            if key == K_SPACE:
                self.go(mousePos)
            elif key == K_a:
                self.assignSelectedAgents(mousePos)
            elif key == K_f:
                self.speedUp()
            elif key == K_s:
                self.slowDown()
            elif key == K_h:
                self.half()
            elif key == K_RIGHT:
                self.next()
            elif key == K_LEFT:
                self.previous()
            elif key == K_UP:
                self.raiseQuality()
            elif key == K_DOWN:
                self.lowerQuality()
            elif key == K_EQUALS:
                self.expand()
            elif key == K_MINUS:
                self.shrink()
            elif key == K_c:
                self.createSite(mousePos)
            elif key == K_x:
                self.createAgent(mousePos)
            elif key == K_DELETE or key == K_SLASH:
                self.delete()
            elif key == K_PERIOD:
                self.setSelectedSitesCommand(None, None, None)
            elif key == K_g:
                self.graphs.shouldDrawGraphs = not self.graphs.shouldDrawGraphs
            elif key == K_ESCAPE:
                self.unselectAll()
            elif len(self.selectedSites) > 0 and not pygame.key.get_mods() & KMOD_SHIFT and \
                    not pygame.key.get_mods() & KMOD_CTRL:
                if event.unicode.isnumeric():
                    self.appendNumber(int(event.unicode))
                elif key == K_BACKSPACE:
                    self.deleteLastDigit()
                elif key == K_RETURN:
                    self.setSiteQuality()
            else:
                self.potentialQuality = 0
                self.shouldDrawQuality = False
                if pygame.key.get_mods() & KMOD_SHIFT:
                    self.selectAgentGroup(key)
                elif pygame.key.get_mods() & KMOD_CTRL:
                    self.updateAgentGroup(key)
                elif event.unicode.isnumeric():
                    self.unselectAll()
                    self.selectAgentGroup(key)
        if self.paused:
            self.draw()
            if event.type == KEYDOWN and event.key == K_o:
                self.shouldShowOptions = not self.shouldShowOptions
        if event.type == QUIT:
            pygame.quit()
            self.timer.cancel()
            raise GameOver("Exited Successfully")

    def mouseMotion(self, mousePos):
        if self.graphs.collidesWithCommandHistBoxTop(mousePos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
        elif collidesWithSite(self.world, mousePos) or collidesWithAgent(self.world, mousePos) or \
                self.graphs.collidesWithAnyButton(mousePos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def addToExecutedEvents(self, eventName):
        now = datetime.now()
        hour = '{:02d}'.format(now.hour)
        minute = '{:02d}'.format(now.minute)
        second = '{:02d}'.format(now.second)
        self.graphs.addExecutedCommand(hour + ":" + minute + ":" + second + ": " + eventName)

    def mouseUp(self, mousePos):
        self.putDownDragSite()
        self.unselectAll()
        if self.selectRectCorner is not None and np.abs(mousePos[0] - self.selectRectCorner[0]) > 1\
                and np.abs(mousePos[1] - self.selectRectCorner[1]) > 1:
            self.wideSelect(mousePos)
        elif self.graphs.collidesWithSelectAgentsButton(mousePos):
            self.shouldSelectAgents = not self.shouldSelectAgents
        elif self.graphs.collidesWithSelectSitesButton(mousePos):
            self.shouldSelectSites = not self.shouldSelectSites
        elif self.graphs.collidesWithSelectAgentsSitesButton(mousePos):
            self.shouldSelectAgentSites = not self.shouldSelectAgentSites
        elif self.graphs.collidesWithSelectSitesAgentsButton(mousePos):
            self.shouldSelectSiteAgents = not self.shouldSelectSiteAgents
        elif self.graphs.collidesWithCommandSiteAgentsButton(mousePos):
            self.shouldCommandSiteAgents = not self.shouldCommandSiteAgents
        elif self.graphs.collidesWithOptionsButton(mousePos):
            self.shouldShowOptions = not self.shouldShowOptions
        elif self.graphs.collidesWithNextButton(mousePos):
            self.graphs.nextScreen()
        elif self.graphs.collidesWithPreviousButton(mousePos):
            self.graphs.previousScreen()
        elif self.graphs.collidesWithPauseButton(mousePos):
            self.pause()
        else:
            self.select(mousePos)
        self.selectRectCorner = None

    def mouseDown(self, mousePos):
        self.selectedSites = [s for s in self.world.siteList if s.siteRect.collidepoint(mousePos)]
        if len(self.selectedSites) > 0:
            self.selectedSite = self.selectedSites[0]
            self.drag()
        elif self.graphs.collidesWithCommandHistBoxTop(mousePos):
            self.shouldMoveHistBoxTop = True
        else:
            self.startSelectRect(mousePos)

    def scroll(self, event):
        if event.button == 4:
            self.graphs.scrollUp()
        elif event.button == 5:
            self.graphs.scrollDown()

    def drag(self):
        if self.world.hubCanMove or self.selectedSite is not self.world.getHub():
            self.oldRect = self.selectedSite.getSiteRect().copy()
            self.dragSite = self.selectedSite

    def putDownDragSite(self):
        if self.dragSite is not None:
            if self.dragSite.getSiteRect().center != self.oldRect.center:
                self.addToExecutedEvents("Moved site from " + str(self.oldRect.center) + " to " + str(self.dragSite.getPosition()))
                self.dragSite.wasFound = False
            self.world.siteRectList = [self.dragSite.getSiteRect() if r is self.oldRect else r for r in self.world.siteRectList]
        self.dragSite = None

    def unselectAll(self):
        self.potentialQuality = 0
        self.shouldDrawQuality = False
        self.shouldMoveHistBoxTop = False
        self.world.setMarker(None)
        self.selectedAgent = None
        self.selectedSite = None
        # Unselect all agents and sites
        for a in self.agentList:
            a.unselect()
        for s in self.world.siteList:
            s.unselect()
        self.selectedAgents = []
        self.selectedSites = []

    def select(self, mousePos):
        # get a list of all objects that are under the mouse cursor
        if Display.canSelectAnywhere or self.getHubObserveRect().collidepoint(mousePos):
            self.selectAgent(mousePos)
            self.selectSite(mousePos)

    def selectAgent(self, mousePos):
        selectedAgents = [a for a in self.agentList if a.getAgentRect().collidepoint(mousePos)]

        if len(selectedAgents) > 0:
            self.selectedAgents = []
            self.selectAgent2(selectedAgents[0])
            if self.shouldSelectAgents:
                self.selectedAgent.isTheSelected = True
            if self.shouldSelectAgentSites:
                self.selectedSite.isTheSelected = True

    def selectAgent2(self, agent):
        if self.shouldSelectAgents:
            self.selectedAgent = agent
            self.selectedAgent.select()
            self.selectedAgents.append(self.selectedAgent)
            self.selectedAgentIndex = len(self.selectedAgents) - 1
        if self.shouldSelectAgentSites:
            self.selectedSite = agent.assignedSite
            self.selectedSite.select()

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
        if not self.graphs.collidesWithAnyButton(mousePos):
            self.selectRectCorner = mousePos

    def wideSelect(self, mousePos):
        # get a list of all objects that are under the mouse cursor
        self.selectRect = self.drawSelectRect(mousePos)
        agent = None
        if Display.canSelectAnywhere or self.selectRect.colliderect(self.getHubObserveRect()):
            agent = self.selectAgents()
            self.selectSites()
        if self.shouldSelectAgentSites:
            self.selectAgentsSite(agent)

    def selectAgentGroup(self, key):
        index = key - 48
        if not 0 <= index <= 9:
            return
        agentGroup = self.world.getGroup(index)
        for agent in agentGroup:
            self.selectAgent2(agent)
        if len(agentGroup) > 0:
            if self.shouldSelectAgents:
                self.selectedAgent.isTheSelected = True
            if self.shouldSelectAgentSites:
                self.selectedSite.isTheSelected = True

    def updateAgentGroup(self, key):
        index = key - 48
        if not 0 <= index <= 9:
            return
        self.addToExecutedEvents("Set agent group " + str(index) + " to have " + str(len(self.selectedAgents)) + " agents.")
        self.world.updateGroup(index, self.selectedAgents)

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
        return pygame.draw.rect(Display.screen, BORDER_COLOR, pygame.Rect(left, top, width, height), 1)

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

    def getHubObserveRect(self):
        hubRect = self.world.getHub().getSiteRect()
        r = self.world.getHub().radius
        return pygame.Rect(hubRect.left - (r + HUB_OBSERVE_DIST), hubRect.top - (r + HUB_OBSERVE_DIST),
                           hubRect.width + ((r + HUB_OBSERVE_DIST) * 2), hubRect.height + ((r + HUB_OBSERVE_DIST) * 2))

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
        for agent in self.agentList:
            if agent.assignedSite is self.selectedSite:
                if self.shouldSelectSiteAgents:
                    agent.select()
                    self.selectedAgents.append(agent)
        if self.shouldSelectSiteAgents and len(self.selectedAgents) > 0:
            self.selectedAgent = self.selectedAgents[0]
            self.selectedAgent.isTheSelected = True
        if not self.shouldSelectSites:
            self.selectedSite = None

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
        if self.paused and self.shouldShowOptions:
            self.graphs.nextScreen()
        elif len(self.selectedAgents) > 1:
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
        if self.paused and self.shouldShowOptions:
            self.graphs.previousScreen()
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
        if len(self.selectedAgents) > 0:
            self.addToExecutedEvents("Sent " + str(len(self.selectedAgents)) + " agents to " + str(mousePos))
        marker = getDestinationMarker(mousePos)
        self.setSelectedSitesCommand(self.goCommand, mousePos, marker)
        self.world.setMarker(marker)
        for a in self.selectedAgents:
            self.goCommand(a, mousePos)

    @staticmethod
    def goCommand(agent, mousePos):
        agent.target = mousePos
        from model.states.GoState import GoState
        agent.setState(GoState(agent))

    @staticmethod
    def assignCommand(agent, mousePos):
        sitesUnderMouse = [s for s in agent.world.siteList if s.siteRect.collidepoint(mousePos)]
        if len(sitesUnderMouse) > 0:
            agent.addToKnownSites(sitesUnderMouse[0])
            agent.assignSite(sitesUnderMouse[0])

    def setSelectedSitesCommand(self, command, mousePos, marker):
        if self.shouldCommandSiteAgents:
            for site in self.selectedSites:
                self.addToExecutedEvents("Set site at " + str(site.getPosition()) + "'s go point to " + str(mousePos))
                site.setCommand(command, mousePos, marker)

    def assignSelectedAgents(self, mousePos):
        sitesUnderMouse = [s for s in self.world.siteList if s.siteRect.collidepoint(mousePos)]
        if len(sitesUnderMouse) > 0:
            if len(self.selectedAgents) > 0:
                self.addToExecutedEvents("Assigned " + str(len(self.selectedAgents)) + " agents to site at " + str(sitesUnderMouse[0].getPosition()))
            for a in self.selectedAgents:
                a.addToKnownSites(sitesUnderMouse[0])
                a.assignSite(sitesUnderMouse[0])
        marker = getDestinationMarker(mousePos)  # TODO: Get a different marker
        self.setSelectedSitesCommand(self.assignCommand, mousePos, marker)

    def speedUp(self):
        self.addToExecutedEvents("Sped Agents up")
        for a in self.agentList:
            a.speed *= 1.2
            a.speedCoefficient *= 1.2

    def slowDown(self):
        self.addToExecutedEvents("Slowed Agents down")
        for a in self.agentList:
            a.speed /= 1.2
            a.speedCoefficient /= 1.2

    def raiseQuality(self):
        for site in self.selectedSites:
            site.setQuality(site.getQuality() + 1)
            self.addToExecutedEvents("Raised site at " + str(site.getPosition()) + "'s quality to " + str(site.getQuality()))
            site.setColor(site.getQuality())

    def lowerQuality(self):
        for site in self.selectedSites:
            site.setQuality(site.getQuality() - 1)
            self.addToExecutedEvents("Lowered site at " + str(site.getPosition()) + "'s quality to " + str(site.getQuality()))
            site.setColor(site.getQuality())

    def expand(self):
        for site in self.selectedSites:
            site.radius += 1
            self.addToExecutedEvents("Expanded site at " + str(site.getPosition()) + "'s radius to " + str(site.radius))

    def shrink(self):
        for site in self.selectedSites:
            site.radius -= 1
            self.addToExecutedEvents("Shrunk site at " + str(site.getPosition()) + "'s radius to " + str(site.radius))

    def createSite(self, position):
        self.world.createSite(position[0], position[1], SITE_RADIUS, 128)
        self.addToExecutedEvents("Created site at " + str(position))

    def createAgent(self, position):
        agent = Agent(self.world, self.world.getHub(), startingPosition=position)
        agent.setState(SearchState(agent))
        agent.setAngle(random.uniform(0, 2 * np.pi))
        agent.assignedSite.incrementCount()
        agent.speedCoefficient = self.world.agentList[0].speedCoefficient
        agent.speed = self.world.agentList[0].uncommittedSpeed * agent.speedCoefficient
        self.world.addAgent(agent)
        self.addToExecutedEvents("Created agent at " + str(position))

    def delete(self):
        self.deleteSelectedSites()
        self.deleteSelectedAgents()

    def deleteSelectedSites(self):
        i = 0
        while len(self.selectedSites) > 0:
            site = self.selectedSites[i]
            if site.getQuality() >= 0:
                self.addToExecutedEvents("Deleted site at " + str(site.getPosition()))
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
        if len(self.selectedAgents) > 0:
            self.addToExecutedEvents("Deleted " + str(len(self.selectedAgents)) + " agents")
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
            self.addToExecutedEvents("Set quality of site at " + str(site.getPosition()) + " to " + str(self.potentialQuality))
            site.setQuality(self.potentialQuality)
            site.setColor(self.potentialQuality)
        self.potentialQuality = 0
        self.shouldDrawQuality = False

    def pause(self):
        Display.drawPause(Display.screen)
        pygame.display.flip()
        self.paused = True
        self.timer.pause(self.handleEvent, self.graphs.collidesWithPauseButton)
        self.paused = False
