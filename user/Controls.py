import random

import numpy as np
import pygame
from pygame.constants import KEYDOWN, K_p, MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, K_SPACE, K_a, K_f, K_s, K_h, \
    K_RIGHT, K_LEFT, K_UP, K_DOWN, K_EQUALS, K_MINUS, K_c, K_x, K_DELETE, K_SLASH, K_PERIOD, K_g, K_ESCAPE, KMOD_SHIFT, \
    KMOD_CTRL, K_BACKSPACE, K_RETURN, K_o, QUIT, KMOD_ALT, K_z, K_k, K_r, K_w

from config import Config
from Constants import SCREEN_COLOR, BORDER_COLOR, AT_NEST, TRANSPORT, STATES_LIST, ASSIGN_NAME, NO_MARKER_NAME, \
    SET_STATE_NAME, GO_NAME, BLUE, DEAD, STOP_AVOID_NAME, MEDIUM_QUALITY
from display import Display
from display.simulation.WorldDisplay import drawWorldObjects, collidesWithSite, collidesWithAgent, drawPotentialQuality
from ColonyExceptions import GameOver
from display.Display import getDestinationMarker, getAssignmentMarker
from model.builder import AgentBuilder
from model.phases.ExplorePhase import ExplorePhase
from model.states.NumToStateConverter import numToState
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
        self.selectedSites = []
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
        Display.drawBorder()
        Display.drawPause(Display.screen)
        if self.shouldShowOptions:
            self.graphs.drawOptions()
        pygame.display.flip()

    def drawChanges(self):
        if len(self.selectedAgents) > 0:  # Display the number of agents that are selected by the mouse
            pos = pygame.mouse.get_pos()
            Display.write(Display.screen, str(len(self.selectedAgents)), Config.FONT_SIZE,
                          pos[0] + Config.FONT_SIZE, pos[1] + Config.FONT_SIZE, BLUE)
            if len(self.selectedAgents) > 1 and self.graphs.shouldDrawGraphs:
                Display.write(Display.screen, "Cut the number of selected ants in half by pressing 'H'",
                              Config.FONT_SIZE, Display.origWidth - 420, 4 * Config.FONT_SIZE, BLUE)
        if len(self.selectedSites) > 0 and self.shouldDrawQuality:
            drawPotentialQuality(self.world, self.potentialQuality)
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
        if self.shouldMoveHistBoxTop:
            self.graphs.setHistBoxTop(mousePos[1])
        if event.type == MOUSEMOTION:
            self.mouseMotion(mousePos, adjustedMousePos)
        elif event.type == MOUSEBUTTONUP:
            print(f"mousePos: {mousePos}, adjPos: {adjustedMousePos}")
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
            elif key == K_w:
                self.addCheckPoint(adjustedMousePos)
            elif key == K_z:
                self.avoid(adjustedMousePos)
            elif key == K_r:
                self.removeAvoids(adjustedMousePos)
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
                self.setSelectedSitesCommand(None, None, None, NO_MARKER_NAME)
            elif key == K_g:
                self.graphs.shouldDrawGraphs = not self.graphs.shouldDrawGraphs
            elif key == K_ESCAPE:
                self.unselectAll()
            elif key == K_k:
                self.kill()
            elif len(self.selectedSites) > 0 and not pygame.key.get_mods() & KMOD_SHIFT and \
                    not pygame.key.get_mods() & KMOD_CTRL and not pygame.key.get_mods() & KMOD_ALT:
                if event.unicode.isnumeric():
                    self.appendNumber(int(event.unicode))
                elif key == K_BACKSPACE:
                    self.deleteLastDigit()
                elif key == K_RETURN and self.shouldDrawQuality:
                    self.setSiteQuality()
            else:
                self.potentialQuality = 0
                self.shouldDrawQuality = False
                if pygame.key.get_mods() & KMOD_SHIFT:
                    self.selectAgentGroup(key)
                elif pygame.key.get_mods() & KMOD_CTRL:
                    self.updateAgentGroup(key)
                elif pygame.key.get_mods() & KMOD_ALT:
                    self.setAgentsStates(key)
                elif event.unicode.isnumeric():
                    self.unselectAll()
                    self.selectAgentGroup(key)
        self.graphs.shouldDrawStateNumbers = pygame.key.get_mods() & KMOD_ALT and len(self.selectedAgents) > 0
        if self.paused:
            self.draw()
            if event.type == KEYDOWN and event.key == K_o:
                self.shouldShowOptions = not self.shouldShowOptions
            if event.type == MOUSEBUTTONUP:
                if self.graphs.collidesWithCloseButton(mousePos, self.paused):
                    self.shouldShowOptions = False
                elif self.graphs.collidesWithExitButton(mousePos, self.paused):
                    self.paused = False
                    self.timer.cancel()
                    raise GameOver("Game Over")
        if event.type == QUIT:
            pygame.quit()
            self.timer.cancel()
            raise GameOver("Exiting")

    def handleFinishEvents(self):
        self.moveScreen()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP and pygame.key.get_mods() & KMOD_CTRL:
                self.zoom(event)
            elif event.type == MOUSEBUTTONUP and (event.button == 1 or event.button == 3) \
                    or event.type == KEYDOWN and not pygame.key.get_mods() & KMOD_CTRL:
                return True
        return False

    def mouseMotion(self, mousePos, adjustedMousePos):
        # Set the cursor image
        if self.dragSite is not None:
            self.world.setSitePosition(self.dragSite, adjustedMousePos)
        elif self.graphs.collidesWithCommandHistBoxTop(mousePos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
        elif self.collidesWithSelectable(mousePos, adjustedMousePos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def collidesWithSelectable(self, mousePos, adjustedMousePos):
        return collidesWithSite(self.world, adjustedMousePos) or collidesWithAgent(self.world, adjustedMousePos) or \
                self.graphs.collidesWithAnyButton(mousePos, self.paused)

    def getNumLivingSelectedAgents(self):
        numLiving = 0
        for agent in self.selectedAgents:
            if agent.getStateNumber() != DEAD:
                numLiving += 1
        return numLiving

    def moveScreen(self):
        if not pygame.key.get_mods() & pygame.KMOD_CAPS:
            Display.moveScreen(pygame.mouse.get_pos())
        if self.paused:
            self.draw()

    def addToExecutedEvents(self, eventName):
        self.graphs.addExecutedCommand(eventName)

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
        elif self.graphs.collidesWithOptionsButton(mousePos, self.paused):
            self.shouldShowOptions = not self.shouldShowOptions
        elif self.graphs.collidesWithNextButton(mousePos, self.paused):
            self.graphs.nextScreen()
        elif self.graphs.collidesWithPreviousButton(mousePos, self.paused):
            self.graphs.previousScreen()
        elif self.graphs.collidesWithPauseButton(mousePos):
            self.pause()
        else:
            self.select(adjustedMousePos)
        self.selectRectCorner = None

    def mouseDown(self, mousePos, adjustedMousePos):
        self.selectedSites = [s for s in self.world.siteList if s.siteRect.collidepoint(adjustedMousePos)]
        if len(self.selectedSites) > 0 and self.shouldSelectSites:
            self.startDrag()
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

    def startDrag(self):
        if Config.HUB_CAN_MOVE or not self.world.getHubs().__contains__(self.selectedSites[0]):
            self.oldRect = self.selectedSites[0].getSiteRect().copy()
            self.dragSite = self.selectedSites[0]

    def putDownDragSite(self):
        if self.dragSite is not None:
            if self.dragSite.getSiteRect().center != self.oldRect.center:
                self.addToExecutedEvents(f"Moved site from {self.oldRect.center} to {self.dragSite.getPosition()}")
                self.dragSite.wasFound = False
            self.world.siteRectList = [self.dragSite.getSiteRect() if r is self.oldRect else r for r in self.world.siteRectList]
            self.world.hubsRects = [self.dragSite.getSiteRect() if r is self.oldRect else r for r in self.world.hubsRects]
        self.dragSite = None

    def unselectAll(self):
        self.potentialQuality = 0
        self.shouldDrawQuality = False
        self.shouldMoveHistBoxTop = False
        self.selectedAgent = None
        # Unselect all agents and sites
        for a in self.agentList:
            a.unselect()
        for s in self.world.siteList:
            s.unselect()
        self.selectedAgents = []
        self.selectedSites = []

    def select(self, mousePos):
        # get a list of all objects that are under the mouse cursor
        if Config.DRAW_FAR_AGENTS or self.byAHub(mousePos):
            self.selectAgent(mousePos)
            self.selectSite(mousePos)

    def byAHub(self, pos):
        for hub in self.world.getHubs():
            if self.world.isClose(pos, hub.getPosition(), Config.HUB_OBSERVE_DIST):
                return True
        return False

    def selectAgent(self, mousePos):
        selectedAgents = [a for a in self.agentList if a.getRect().collidepoint(mousePos)]

        if len(selectedAgents) > 0:
            self.selectedAgents = []
            self.selectAgent2(selectedAgents[0])
            if self.shouldSelectAgents:
                self.selectedAgent.mainSelect()

    def selectAgent2(self, agent):
        if self.shouldSelectAgents:
            self.selectedAgent = agent
            self.selectedAgent.select()
            self.selectedAgents.append(self.selectedAgent)
            self.selectedAgentIndex = len(self.selectedAgents) - 1
        if self.shouldSelectAgentSites:
            self.selectAgentsSite(agent)

    def selectSite(self, mousePos):
        selectedSites = [s for s in self.world.siteList if s.siteRect.collidepoint(mousePos)]

        if len(selectedSites) > 0:
            if self.shouldSelectSites:
                selectedSites[0].select()
                self.selectedSites = [selectedSites[0]]
            self.selectSite2(selectedSites)
            if len(self.selectedAgents) > 0:
                self.selectedAgent = self.selectedAgents[0]
                self.selectedAgent.mainSelect()

    def startSelectRect(self, mousePos):
        if not self.graphs.collidesWithAnyButton(mousePos, self.paused):
            self.selectRectCorner = mousePos

    def wideSelect(self, mousePos):
        # get a list of all objects that are under the mouse cursor
        self.selectRect = self.drawSelectRect(mousePos)
        left, top = Display.getReadjustedPos(self.selectRect.left, self.selectRect.top)
        w, h = Display.getUnzoomedSize(self.selectRect.w, self.selectRect.h)
        rect = pygame.Rect(left, top, w, h)
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
            if not agent.isSelected:
                self.selectAgent2(agent)
        if len(agentGroup) >= len(self.selectedAgents) > 0:
            if self.shouldSelectAgents:
                self.selectedAgent.mainSelect()

    def updateAgentGroup(self, key):
        index = key - 48
        if not 0 <= index <= 9:
            return
        self.addToExecutedEvents(f"Set agent group {index} to have {len(self.selectedAgents)} agents.")
        self.world.updateGroup(index, self.selectedAgents)

    def setAgentsStates(self, key):
        stateNum = key - 48
        if not AT_NEST <= stateNum <= TRANSPORT:
            return
        for agent in self.selectedAgents:
            if agent.getStateNumber() != DEAD and agent.checkLeadAgent(agent, stateNum):
                agent.setState(numToState(stateNum, agent))
        self.setSelectedSitesCommand(self.setStateCommand, stateNum, stateNum, SET_STATE_NAME)

    @staticmethod
    def setStateCommand(agent, state):
        if agent.checkLeadAgent(agent, state):
            if agent.getStateNumber() != DEAD:
                agent.setState(numToState(state, agent))

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
        selectedAgents = [a for a in self.agentList if a.getRect().colliderect(rect) and (Config.DRAW_FAR_AGENTS or
                                                                                          a.isCloseToHub())]
        if self.shouldSelectAgents:
            self.selectedAgents = selectedAgents

        for a in self.selectedAgents:
            a.select()

        if len(self.selectedAgents) > 0:
            self.selectedAgent = self.selectedAgents[0]
            self.selectedAgent.mainSelect()
            self.selectedAgentIndex = 0

        if len(selectedAgents) > 0:
            return selectedAgents[0]

        return None

    def selectSites(self, rect):
        selectedSites = [s for s in self.world.siteList if s.siteRect.colliderect(rect) and
                         (s.wasFound or Config.DRAW_FAR_AGENTS)]
        if self.shouldSelectSites:
            self.selectedSites = selectedSites

        for s in self.selectedSites:
            s.select()

        if len(selectedSites) > 0:
            self.selectSite2(selectedSites)

    def selectSite2(self, sites):
        if self.shouldSelectSiteAgents:
            for agent in self.agentList:
                if not agent.isSelected and sites.__contains__(agent.assignedSite):
                    agent.select()
                    self.selectedAgents.append(agent)
            if len(self.selectedAgents) > 0:
                self.selectedAgent = self.selectedAgents[0]
                self.selectedAgent.mainSelect()
        if not self.shouldSelectSites:
            self.selectedSites.clear()

    def selectAgentsSite(self, agent):
        if agent is not None and agent.assignedSite is not None and \
                not self.selectedSites.__contains__(agent.assignedSite):
            self.selectedSites.append(agent.assignedSite)
            agent.assignedSite.select()

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

    def nextAgent(self):
        if len(self.selectedAgents) > 0:
            self.selectedAgentIndex += 1
            self.selectedAgent.unMainSelect()
            self.selectedAgent = self.selectedAgents[self.selectedAgentIndex % len(self.selectedAgents)]
            self.selectedAgent.mainSelect()

    def previous(self):
        if self.paused and self.shouldShowOptions:
            self.graphs.previousScreen()
        elif len(self.selectedAgents) > 1:
            self.previousAgent()

    def previousAgent(self):
        if len(self.selectedAgents) > 0:
            self.selectedAgentIndex -= 1
            self.selectedAgent.unMainSelect()
            self.selectedAgent = self.selectedAgents[self.selectedAgentIndex % len(self.selectedAgents)]
            self.selectedAgent.mainSelect()

    def addCheckPoint(self, mousePos):
        if len(self.selectedAgents) > 0:
            pos = [int(mousePos[0]), int(mousePos[1])]
            self.addToExecutedEvents(f"Added check point at {pos} for {self.getNumLivingSelectedAgents()} agents")
        for agent in self.selectedAgents:
            agent.checkPoints.append(mousePos)
        if self.shouldCommandSiteAgents:
            if len(self.selectedSites) > 0:
                pos = [int(mousePos[0]), int(mousePos[1])]
                self.addToExecutedEvents(f"Added check point at {pos} for {len(self.selectedSites)} sites")
            for site in self.selectedSites:
                site.checkPoints.append(mousePos)

    def go(self, mousePos):
        if len(self.selectedAgents) > 0:
            pos = [int(mousePos[0]), int(mousePos[1])]
            self.addToExecutedEvents(f"Sent {self.getNumLivingSelectedAgents()} agents to {pos}")
        marker = getDestinationMarker(mousePos)
        self.setSelectedSitesCommand(self.goCommand, list(mousePos), marker, GO_NAME)
        for agent in self.selectedAgents:
            self.goCommand(agent, mousePos)

    @staticmethod
    def goCommand(agent, mousePos):
        if agent.getStateNumber() != DEAD:
            agent.setTarget(list(mousePos))
            from model.states.GoState import GoState
            agent.setState(GoState(agent))

    def avoid(self, pos):
        if len(self.selectedAgents) > 0:
            pos = [int(pos[0]), int(pos[1])]
            self.addToExecutedEvents(f"{self.getNumLivingSelectedAgents()} agents started avoiding {pos}")
        for a in self.selectedAgents:
            self.avoidCommand(a, pos)
        if self.shouldCommandSiteAgents:
            if len(self.selectedSites) > 0:
                pos = [int(pos[0]), int(pos[1])]
                self.addToExecutedEvents(f"{len(self.selectedSites)} sites started avoiding {pos}")
            for site in self.selectedSites:
                site.areasToAvoid.append(pos)
                if len(site.areasToAvoid) > Config.MAX_NUM_AVOIDS:
                    self.addToExecutedEvents(f"Removed command to avoid {site.areasToAvoid.pop(0)}")

    @staticmethod
    def avoidCommand(agent, mousePos):
        if agent.getStateNumber() != DEAD:
            agent.avoid(mousePos)

    def removeAvoids(self, pos):
        if len(self.selectedAgents) > 0:
            pos = [int(pos[0]), int(pos[1])]
            self.addToExecutedEvents(f"{self.getNumLivingSelectedAgents()} agents stopped avoiding {pos}")
        self.setSelectedSitesCommand(self.removeAvoidCommand, list(pos), None, STOP_AVOID_NAME)
        for a in self.selectedAgents:
            self.removeAvoidCommand(a, pos)

    @staticmethod
    def removeAvoidCommand(agent, pos):
        for i, place in enumerate(reversed(agent.placesToAvoid)):
            if abs(place[0] - pos[0]) < 100 and abs(place[1] - pos[1]) < 100:
                agent.stopAvoiding(i)

    @staticmethod
    def assignCommand(agent, mousePos):
        if agent.getStateNumber() != DEAD:
            sitesUnderMouse = [s for s in agent.world.siteList if s.siteRect.collidepoint(mousePos)]
            if len(sitesUnderMouse) > 0:
                agent.addToKnownSites(sitesUnderMouse[0])
                agent.assignSite(sitesUnderMouse[0])

    def kill(self):
        self.addToExecutedEvents(f"Killed {self.getNumLivingSelectedAgents()} agents")
        for agent in self.selectedAgents:
            agent.die()

    def setSelectedSitesCommand(self, command, arg, marker, markerName):
        if self.shouldCommandSiteAgents:
            for site in self.selectedSites:
                if arg is not None:
                    try:
                        pos = [int(arg[0]), int(arg[1])]
                        self.addToExecutedEvents(f"Set site at {site.getPosition()}'s command point to {pos}")
                    except TypeError:
                        self.addToExecutedEvents(f"Set site at {site.getPosition()}'s command to {STATES_LIST[arg]}")
                else:
                    self.addToExecutedEvents(f"Removed site at {site.getPosition()}'s command")
                site.setCommand(command, arg, marker, markerName)

    def setSiteCommand(self, site, markerNameArgNum):
        markerName, arg, stateNum = markerNameArgNum
        if markerName != site.markerName:
            if markerName == NO_MARKER_NAME:
                site.setCommand(None, None, None, markerName)
            elif markerName == GO_NAME:
                site.setCommand(self.goCommand, arg, getDestinationMarker(arg), markerName)
            elif markerName == ASSIGN_NAME:
                site.setCommand(self.assignCommand, arg, getAssignmentMarker(arg), markerName)
            elif markerName == SET_STATE_NAME:
                site.setCommand(self.setStateCommand, arg, stateNum, markerName)

    def assignSelectedAgents(self, mousePos):
        sitesUnderMouse = [s for s in self.world.siteList if s.siteRect.collidepoint(mousePos)]
        if len(sitesUnderMouse) > 0:
            marker = getAssignmentMarker(mousePos)
            if len(self.selectedAgents) > 0:
                self.addToExecutedEvents(f"Assigned {self.getNumLivingSelectedAgents()} agents to site at {sitesUnderMouse[0].getPosition()}")
            for a in self.selectedAgents:
                if a.getStateNumber() != DEAD:
                    a.marker = marker
                    a.addToKnownSites(sitesUnderMouse[0])
                    a.assignSite(sitesUnderMouse[0])

            self.setSelectedSitesCommand(self.assignCommand, list(mousePos), marker, ASSIGN_NAME)

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
            self.addToExecutedEvents(f"Raised site at {site.getPosition()}'s quality to {site.getQuality()}")
            site.setColor(site.getQuality())

    def lowerQuality(self):
        for site in self.selectedSites:
            site.setQuality(site.getQuality() - 1)
            self.addToExecutedEvents(f"Lowered site at {site.getPosition()}'s quality to {site.getQuality()}")
            site.setColor(site.getQuality())

    def expand(self):
        for site in self.selectedSites:
            site.setRadius(site.getRadius() + 1)
            self.addToExecutedEvents(f"Expanded site at {site.getPosition()}'s radius to {site.getRadius()}")

    def shrink(self):
        for site in self.selectedSites:
            site.setRadius(site.getRadius() - 1)
            self.addToExecutedEvents(f"Shrunk site at {site.getPosition()}'s radius to {site.getRadius()}")

    def createSite(self, position):
        self.world.createSite(position[0], position[1], Config.SITE_RADIUS, MEDIUM_QUALITY, len(self.world.getHubs()))
        pos = [int(position[0]), int(position[1])]
        self.addToExecutedEvents(f"Created site at {pos}")

    def createAgent(self, position):
        agent = AgentBuilder.getNewAgent(self.world, self.world.getClosestHub(position), position)
        agent.setState(SearchState(agent))
        agent.setAngle(random.uniform(0, 2 * np.pi))
        agent.assignedSite.incrementCount(agent.getHubIndex())
        agent.speedCoefficient = self.world.agentList[0].speedCoefficient
        agent.speed = self.world.agentList[0].uncommittedSpeed * agent.speedCoefficient
        self.world.addAgent(agent)
        pos = [int(position[0]), int(position[1])]
        self.addToExecutedEvents(f"Created agent at {pos}")

    def delete(self):
        self.deleteSelectedSites()
        self.deleteSelectedAgents()

    def deleteSelectedSites(self):
        i = 0
        while len(self.selectedSites) > 0:
            site = self.selectedSites[i]
            if not site.isHub():
                self.addToExecutedEvents(f"Deleted site at {site.getPosition()}")
                for agent in self.agentList:
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

    def deleteSelectedAgents(self):
        if len(self.selectedAgents) > 0:
            self.addToExecutedEvents(f"Deleted {(len(self.selectedAgents))} agents")
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
            if not site.isHub():
                self.addToExecutedEvents(f"Set quality of site at {site.getPosition()} to {self.potentialQuality}")
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
