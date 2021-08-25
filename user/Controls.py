import random
from datetime import datetime

import numpy as np
import pygame
from pygame.constants import KEYDOWN, K_p, MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, K_SPACE, K_a, K_f, K_s, K_h, \
    K_RIGHT, K_LEFT, K_UP, K_DOWN, K_EQUALS, K_MINUS, K_c, K_x, K_DELETE, K_SLASH, K_PERIOD, K_g, K_ESCAPE, KMOD_SHIFT, \
    KMOD_CTRL, K_BACKSPACE, K_RETURN, K_o, QUIT

from Constants import SITE_RADIUS, SCREEN_COLOR, BORDER_COLOR, NUM_HUBS, MAX_SEARCH_DIST, COMMIT_COLOR
from display import Display
from display.AgentDisplay import drawAgent
from display.WorldDisplay import drawWorldObjects, collidesWithSite, collidesWithAgent, drawPotentialQuality
from ColonyExceptions import GameOver
from display.Display import getDestinationMarker
from model.builder import AgentBuilder, SiteSettings
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
            self.selectRect = self.drawSelectRect(pygame.mouse.get_pos())  # The displayed rect and selectRect need to be different when the screen moves
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
        # When the screen moves, the mouse position needs to be adjusted to make up for it with some of the controls
        adjustedMousePos = Display.getReadjustedPos(mousePos[0], mousePos[1])
        if self.dragSite is not None:
            self.world.setSitePosition(self.dragSite, adjustedMousePos)
        if self.shouldMoveHistBoxTop:
            self.graphs.setHistBoxTop(mousePos[1])
        if event.type == MOUSEMOTION:
            self.mouseMotion(mousePos, adjustedMousePos)
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.mouseUp(mousePos, adjustedMousePos)
            elif event.button == 3:
                self.go(adjustedMousePos)
            else:
                if pygame.key.get_mods() & KMOD_CTRL:
                    self.zoom(event)
                else:
                    self.scroll(event)
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.mouseDown(mousePos, adjustedMousePos)
        elif event.type == KEYDOWN:
            key = event.key
            if key == K_SPACE:
                self.go(adjustedMousePos)
            elif key == K_a:
                self.assignSelectedAgents(adjustedMousePos)
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
                self.createSite(adjustedMousePos)
            elif key == K_x:
                self.createAgent(adjustedMousePos)
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

    def mouseMotion(self, mousePos, adjustedMousePos):
        # Set the cursor image
        if self.graphs.collidesWithCommandHistBoxTop(mousePos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
        elif collidesWithSite(self.world, adjustedMousePos) or collidesWithAgent(self.world, adjustedMousePos) or \
                self.graphs.collidesWithAnyButton(mousePos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def moveScreen(self):
        if not pygame.key.get_mods() & pygame.KMOD_CAPS:
            mousePos = pygame.mouse.get_pos()
            if mousePos[0] >= Display.screen.get_width() - 3 and Display.displacementX >= -MAX_SEARCH_DIST:
                Display.displacementX -= 25
                Display.addToDrawLast(Display.drawRightArrow, mousePos, COMMIT_COLOR, False)
            if mousePos[1] <= 3 and Display.displacementY <= MAX_SEARCH_DIST:
                Display.displacementY += 25
                Display.addToDrawLast(Display.drawUpArrow, mousePos, COMMIT_COLOR, False)
            if mousePos[0] <= 3 and Display.displacementX <= MAX_SEARCH_DIST:
                Display.displacementX += 25
                Display.addToDrawLast(Display.drawLeftArrow, mousePos, COMMIT_COLOR, False)
            if mousePos[1] >= Display.screen.get_height() - 30 and Display.displacementY >= -MAX_SEARCH_DIST:
                Display.displacementY -= 25
                Display.addToDrawLast(Display.drawDownArrow, mousePos, COMMIT_COLOR, False)
        if self.paused:
            self.draw()

    def addToExecutedEvents(self, eventName):
        now = datetime.now()
        hour = '{:02d}'.format(now.hour)
        minute = '{:02d}'.format(now.minute)
        second = '{:02d}'.format(now.second)
        self.graphs.addExecutedCommand(hour + ":" + minute + ":" + second + ": " + eventName)

    def mouseUp(self, mousePos, adjustedMousePos):
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
            self.select(adjustedMousePos)
        self.selectRectCorner = None

    def mouseDown(self, mousePos, adjustedMousePos):
        selectedSites = [s for s in self.world.siteList if s.siteRect.collidepoint(adjustedMousePos)]
        if len(selectedSites) > 0 and self.shouldSelectSites:
            self.selectedSite = selectedSites[0]
            self.drag()
        elif self.graphs.collidesWithCommandHistBoxTop(mousePos):
            self.shouldMoveHistBoxTop = True
        else:
            self.startSelectRect(mousePos)

    @staticmethod
    def zoom(event):
        if not pygame.key.get_mods() & pygame.KMOD_CAPS:
            if event.button == 4:
                Display.zoomIn()
            elif event.button == 5:
                Display.zoomOut()

    def scroll(self, event):
        if event.button == 4:
            self.graphs.scrollUp()
        elif event.button == 5:
            self.graphs.scrollDown()

    def drag(self):
        if SiteSettings.hubCanMove or not self.world.getHubs().__contains__(self.selectedSite):
            self.oldRect = self.selectedSite.getSiteRect().copy()
            self.dragSite = self.selectedSite

    def putDownDragSite(self):
        if self.dragSite is not None:
            if self.dragSite.getSiteRect().center != self.oldRect.center:
                self.addToExecutedEvents("Moved site from " + str(self.oldRect.center) + " to " + str(self.dragSite.getPosition()))
                self.dragSite.wasFound = False
            self.world.siteRectList = [self.dragSite.getSiteRect() if r is self.oldRect else r for r in self.world.siteRectList]
            self.world.hubsRects = [self.dragSite.getSiteRect() if r is self.oldRect else r for r in self.world.hubsRects]
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
        if Display.canSelectAnywhere or self.byAHub(mousePos):
            self.selectAgent(mousePos)
            self.selectSite(mousePos)

    def byAHub(self, pos):
        for rect in self.world.getHubsObserveRects():
            if rect.collidepoint(pos):
                return True
        return False

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
            self.selectSite2(selectedSites)
            if len(self.selectedAgents) > 0:
                self.selectedAgent = self.selectedAgents[0]
                self.selectedAgent.isTheSelected = True

    def startSelectRect(self, mousePos):
        if not self.graphs.collidesWithAnyButton(mousePos):
            self.selectRectCorner = mousePos

    def wideSelect(self, mousePos):
        # get a list of all objects that are under the mouse cursor
        self.selectRect = self.drawSelectRect(mousePos)
        left, top = Display.getReadjustedPos(self.selectRect.left, self.selectRect.top)
        w, h = Display.getUnzoomedSize(self.selectRect.w, self.selectRect.h)
        rect = pygame.Rect(left, top, w, h)
        agent = None
        if Display.canSelectAnywhere or self.selectRect.collidelist(self.world.getHubsObserveRects()) != -1:
            agent = self.selectAgents(rect)
            self.selectSites(rect)
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

    def selectAgents(self, rect):
        selectedAgents = [a for a in self.agentList if a.getAgentRect().colliderect(rect)]
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

    def selectSites(self, rect):
        selectedSites = [s for s in self.world.siteList if s.siteRect.colliderect(rect)]
        if self.shouldSelectSites:
            self.selectedSites = selectedSites

        for s in self.selectedSites:
            s.select()

        if len(selectedSites) > 0:
            self.selectedSite = selectedSites[0]
            self.selectSite2(selectedSites)

    def selectSite2(self, sites):
        if self.shouldSelectSites:
            self.selectedSite.isTheSelected = True
            self.selectedSiteIndex = 0
        if self.shouldSelectSiteAgents:
            for agent in self.agentList:
                if sites.__contains__(agent.assignedSite):
                    agent.select()
                    self.selectedAgents.append(agent)
            if len(self.selectedAgents) > 0:
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
        start = len(self.selectedAgents) - 1
        end = int(np.round(len(self.selectedAgents) / 2) - 1)
        try:
            for i in range(start, end, -1):
                if self.selectedAgents[i] is not self.selectedAgent:
                    self.selectedAgents[i].unselect()
                    self.selectedAgents.remove(self.selectedAgents[i])
                else:
                    end += 1
        except IndexError:
            pass

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
        elif len(self.selectedAgents) > 1:
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
            pos = [int(mousePos[0]), int(mousePos[1])]
            self.addToExecutedEvents("Sent " + str(len(self.selectedAgents)) + " agents to " + str(pos))
        marker = getDestinationMarker(mousePos)
        self.setSelectedSitesCommand(self.goCommand, list(mousePos), marker)
        self.world.setMarker(marker)
        for a in self.selectedAgents:
            self.goCommand(a, mousePos)

    @staticmethod
    def goCommand(agent, mousePos):
        agent.target = list(mousePos)
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
                pos = [int(mousePos[0]), int(mousePos[1])]
                self.addToExecutedEvents("Set site at " + str(site.getPosition()) + "'s go point to " + str(pos))
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
        self.setSelectedSitesCommand(self.assignCommand, list(mousePos), marker)

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
        self.world.createSite(position[0], position[1], SITE_RADIUS, 128, NUM_HUBS)
        pos = [int(position[0]), int(position[1])]
        self.addToExecutedEvents("Created site at " + str(pos))

    def createAgent(self, position):
        agent = AgentBuilder.getNewAgent(self.world, self.world.getHubs()[0], position)  # TODO: Make more flexible
        agent.setState(SearchState(agent))
        agent.setAngle(random.uniform(0, 2 * np.pi))
        agent.assignedSite.incrementCount(agent.getHubIndex())
        agent.speedCoefficient = self.world.agentList[0].speedCoefficient
        agent.speed = self.world.agentList[0].uncommittedSpeed * agent.speedCoefficient
        self.world.addAgent(agent)
        pos = [int(position[0]), int(position[1])]
        self.addToExecutedEvents("Created agent at " + str(pos))

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
                if not self.world.getHubs().__contains__(site):
                    if agent.assignedSite is site:
                        try:
                            agent.assignSite(agent.getHub())
                            agent.setPhase(ExplorePhase())
                            agent.setState(SearchState(agent))
                            agent.knownSites.remove(site)
                        except ValueError:
                            pass
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
            if site.getQuality() != -1:
                self.addToExecutedEvents("Set quality of site at " + str(site.getPosition()) + " to " + str(self.potentialQuality))
            site.setQuality(self.potentialQuality)
            site.setColor(self.potentialQuality)
        self.potentialQuality = 0
        self.shouldDrawQuality = False

    def pause(self):
        Display.drawPause(Display.screen)
        pygame.display.flip()
        self.paused = True
        self.timer.pause(self.handleEvent, self.graphs.collidesWithPauseButton, self.moveScreen)
        self.paused = False
