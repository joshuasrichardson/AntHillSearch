import random

import numpy as np
import pygame
from pygame.constants import KEYDOWN, MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, K_SPACE, K_a, K_f, K_s, K_h, \
    K_RIGHT, K_LEFT, K_UP, K_DOWN, K_EQUALS, K_MINUS, K_c, K_x, K_DELETE, K_SLASH, K_PERIOD, K_ESCAPE, KMOD_SHIFT, \
    KMOD_CTRL, K_BACKSPACE, K_RETURN, KMOD_ALT, K_z, K_k, K_r, K_w, K_p, K_o

from config import Config
from Constants import AT_NEST, TRANSPORT, STATES_LIST, ASSIGN_NAME, NO_MARKER_NAME, \
    SET_STATE_NAME, GO_NAME, DEAD, STOP_AVOID_NAME, MEDIUM_QUALITY
from display import Display
from display.Display import getDestinationMarker, getAssignmentMarker
from model.builder import AgentBuilder
from model.phases.ExplorePhase import ExplorePhase
from model.states.NumToStateConverter import numToState
from model.states.SearchState import SearchState

from typing import Dict
from collections.abc import Callable


class Controls:
    """ Lets the user interact with the interface """

    def __init__(self, agentList, world, disp):
        """ agentList - a list of all the agents in the simulation
        world - the world with objects for the user to interact with
        selectRect - the rectangle used to select agents and sites
        disp - the display for the simulation that handles drawing things on the screen """
        self.simDisp = disp

        self.world = world

        self.agentList = agentList
        self.selectedAgent = None
        self.selectedAgents = []
        self.selectedAgentIndex = 0

        self.selectedSites = []
        self.dragSite = None
        self.oldRect = None
        self.potentialQuality = 0

        self.keyCommandMap: Dict[int, Callable[list, None]] = {
            K_a: self.assignSelectedAgents,
            K_c: self.createSite,
            K_f: self.speedUp,
            K_h: self.half,
            K_k: self.kill,
            K_o: self.options,
            K_p: self.playOrPause,
            K_r: self.removeAvoids,
            K_s: self.slowDown,
            K_w: self.addCheckPoint,
            K_x: self.createAgent,
            K_z: self.avoid,
            K_SPACE: self.go,
            K_UP: self.raiseQuality,
            K_DOWN: self.lowerQuality,
            K_RIGHT: self.next,
            K_LEFT: self.previous,
            K_EQUALS: self.expand,
            K_MINUS: self.shrink,
            K_DELETE: self.delete,
            K_SLASH: self.delete,
            K_PERIOD: self.removeSiteCommands,
            K_ESCAPE: self.unselectAll,
        }

    def setPotentialQuality(self, quality):
        self.potentialQuality = quality
        self.simDisp.potentialQuality = quality

    def handleEvents(self):
        dx, dy = Display.getZoomedSize(*Display.moveScreen())
        if self.simDisp.selectRect.isSelecting([dx, dy]) and (dx != 0 or dy != 0):
            self.simDisp.selectRect.moveCorner(dx, dy)
        for event in pygame.event.get():
            self.handleEvent(event)

    def handleEvent(self, event):
        mousePos = pygame.mouse.get_pos()
        # When the screen moves, the mouse position needs to be adjusted to make up for it with some controls
        adjustedMousePos = Display.getReadjustedPos(mousePos[0], mousePos[1])
        if self.simDisp.handleEvent(event):
            if event.type == MOUSEMOTION:
                self.mouseMotion(adjustedMousePos)
            elif event.type == MOUSEBUTTONUP:
                self.mouseUp(event, mousePos, adjustedMousePos)
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.mouseDown(mousePos, adjustedMousePos)
            elif event.type == KEYDOWN:
                self.keyDown(event, adjustedMousePos)

    def handleLastEvents(self):
        Display.moveScreen()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP and pygame.key.get_mods() & KMOD_CTRL:
                self.zoom(event)
            elif event.type == MOUSEBUTTONUP and (event.button == 1 or event.button == 3) \
                    or event.type == KEYDOWN and not pygame.key.get_mods() & KMOD_CTRL:
                return True
        return False

    def mouseMotion(self, adjustedMousePos):
        if self.dragSite is not None:
            self.world.setSitePosition(self.dragSite, adjustedMousePos)
        self.simDisp.collidesWithWorldObject = self.collidesWithWorldObject(adjustedMousePos)

    def collidesWithWorldObject(self, pos):
        for agent in self.agentList:
            if agent.getRect().collidepoint(pos):
                return True
        for site in self.world.siteList:
            if site.collides(pos):
                return True
        return False

    def mouseUp(self, event, mousePos, adjustedMousePos):
        print(f"mousePos: {mousePos}, adjPos: {adjustedMousePos}")
        if event.button == 1:
            self.putDownDragSite()
            self.unselectAll(adjustedMousePos)
            if self.simDisp.selectRect.isSelecting(mousePos):
                self.wideSelect(mousePos)
            else:
                self.select(adjustedMousePos)
            self.simDisp.selectRect.setCorner(None)
        elif event.button == 3:
            self.go(adjustedMousePos)
        elif pygame.key.get_mods() & KMOD_CTRL:
            self.zoom(event)

    def mouseDown(self, mousePos, adjustedMousePos):
        self.selectedSites = [s for s in self.world.siteList if s.siteRect.collidepoint(adjustedMousePos)]
        self.simDisp.numSelectedSites = len(self.selectedSites)
        if len(self.selectedSites) > 0 and self.simDisp.selectSitesButton.activated:
            self.startDrag()
        else:
            self.simDisp.selectRect.setCorner(list(mousePos))

    def keyDown(self, event, adjustedMousePos):
        key = event.key
        try:
            self.keyCommandMap[key](adjustedMousePos)
        except KeyError:
            pass
        if len(self.selectedSites) > 0 and not pygame.key.get_mods() & KMOD_SHIFT and \
                not pygame.key.get_mods() & KMOD_CTRL and not pygame.key.get_mods() & KMOD_ALT:
            if event.unicode.isnumeric():
                self.appendNumber(int(event.unicode))
            elif key == K_BACKSPACE:
                self.deleteLastDigit()
            elif key == K_RETURN and self.simDisp.shouldDrawQuality:
                self.setSiteQuality()
        else:
            self.setPotentialQuality(0)
            self.simDisp.shouldDrawQuality = False
            if pygame.key.get_mods() & KMOD_SHIFT:
                self.selectAgentGroup(key)
            elif pygame.key.get_mods() & KMOD_CTRL:
                self.updateAgentGroup(key)
            elif pygame.key.get_mods() & KMOD_ALT:
                self.setAgentsStates(key)
            elif event.unicode.isnumeric():
                self.unselectAll(adjustedMousePos)
                self.selectAgentGroup(key)

    def getNumLivingSelectedAgents(self):
        numLiving = 0
        for agent in self.selectedAgents:
            if agent.getStateNumber() != DEAD:
                numLiving += 1
        return numLiving

    def addToExecutedEvents(self, eventName):
        self.simDisp.commandHistBox.addExecutedCommand(eventName, self.simDisp.timer.getRemainingTimeOrRounds())

    @staticmethod
    def zoom(event):
        if not pygame.key.get_mods() & pygame.KMOD_CAPS:
            if event.button == 4:
                Display.zoomIn()
            elif event.button == 5:
                Display.zoomOut()

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

    def unselectAll(self, _):
        self.setPotentialQuality(0)
        self.simDisp.shouldDrawQuality = False
        self.selectedAgent = None
        # Unselect all agents and sites
        for a in self.agentList:
            a.unselect()
        for s in self.world.siteList:
            s.unselect()
        self.selectedAgents = []
        self.selectedSites = []
        self.simDisp.numSelectedAgents = 0
        self.simDisp.numSelectedSites = 0

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
            self.simDisp.numSelectedAgents = 0
            self.selectAgent2(selectedAgents[0])
            if self.simDisp.selectAgentsButton.activated:  # self.shouldSelectAgents:
                self.selectedAgent.mainSelect()

    def selectAgent2(self, agent):
        if self.simDisp.selectAgentsButton.activated:
            self.selectedAgent = agent
            self.selectedAgent.select()
            self.selectedAgents.append(self.selectedAgent)
            self.selectedAgentIndex = len(self.selectedAgents) - 1
        if self.simDisp.selectAgentsSitesButton.activated:
            self.selectAgentsSite(agent)

    def selectSite(self, mousePos):
        selectedSites = [s for s in self.world.siteList if s.siteRect.collidepoint(mousePos)]

        if len(selectedSites) > 0:
            if self.simDisp.selectSitesButton.activated:
                selectedSites[0].select()
                self.selectedSites = [selectedSites[0]]
                self.simDisp.numSelectedSites = 1
            self.selectSitesAgents(selectedSites)
            if len(self.selectedAgents) > 0:
                self.selectedAgent = self.selectedAgents[0]
                self.selectedAgent.mainSelect()

    def wideSelect(self, mousePos):
        # get a list of all objects that are under the mouse cursor
        self.simDisp.selectRect.draw(mousePos)
        left, top = Display.getReadjustedPos(self.simDisp.selectRect.rect.left, self.simDisp.selectRect.rect.top)
        w, h = Display.getUnzoomedSize(self.simDisp.selectRect.rect.w, self.simDisp.selectRect.rect.h)
        rect = pygame.Rect(left, top, w, h)
        agent = self.selectAgents(rect)
        self.selectSites(rect)
        if self.simDisp.selectAgentsSitesButton.activated:
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
            if self.simDisp.selectAgentsButton.activated:
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

    def selectAgents(self, rect):
        selectedAgents = [a for a in self.agentList if a.getRect().colliderect(rect) and (Config.DRAW_FAR_AGENTS or
                                                                                          a.isCloseToHub())]
        if self.simDisp.selectAgentsButton.activated:
            self.selectedAgents = selectedAgents
            self.simDisp.numSelectedAgents = len(self.selectedAgents)

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
        if self.simDisp.selectSitesButton.activated:
            self.selectedSites = selectedSites
            self.simDisp.numSelectedSites = len(self.selectedSites)

        for s in self.selectedSites:
            s.select()

        if len(selectedSites) > 0:
            self.selectSitesAgents(selectedSites)

    def selectSitesAgents(self, sites):
        if self.simDisp.selectSitesAgentsButton.activated:
            for agent in self.agentList:
                if not agent.isSelected and agent.assignedSite in sites:
                    agent.select()
                    self.selectedAgents.append(agent)
            if len(self.selectedAgents) > 0:
                self.selectedAgent = self.selectedAgents[0]
                self.selectedAgent.mainSelect()
        if not self.simDisp.selectSitesButton.activated:
            self.selectedSites.clear()

    def selectAgentsSite(self, agent):
        if agent is not None and agent.assignedSite is not None and \
                agent.assignedSite not in self.selectedSites:
            self.selectedSites.append(agent.assignedSite)
            agent.assignedSite.select()

    def half(self, _):
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
        self.simDisp.numSelectedAgents = len(self.selectedAgents)

    def next(self, _):
        if self.simDisp.pauseButton.isPaused and self.simDisp.optionsScreen.visible:
            self.simDisp.optionsScreen.next()
        elif len(self.selectedAgents) > 1:
            self.nextAgent()

    def nextAgent(self):
        if len(self.selectedAgents) > 0:
            self.selectedAgentIndex += 1
            self.selectedAgent.unMainSelect()
            self.selectedAgent = self.selectedAgents[self.selectedAgentIndex % len(self.selectedAgents)]
            self.selectedAgent.mainSelect()

    def previous(self, _):
        if self.simDisp.pauseButton.isPaused and self.simDisp.optionsScreen.visible:
            self.simDisp.optionsScreen.prev()
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
        if self.simDisp.commandSiteAgentsButton.activated:
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
        if self.simDisp.commandSiteAgentsButton.activated:
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

    def kill(self, pos):
        self.addToExecutedEvents(f"Killed {self.getNumLivingSelectedAgents()} agents")
        for agent in self.selectedAgents:
            agent.die()

    def removeSiteCommands(self, _):
        self.setSelectedSitesCommand(None, None, None, NO_MARKER_NAME)

    def setSelectedSitesCommand(self, command, arg, marker, markerName):
        if self.simDisp.commandSiteAgentsButton.activated:
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

    def speedUp(self, pos):
        self.addToExecutedEvents("Sped Agents up")
        for a in self.agentList:
            a.speed *= 1.2
            a.speedCoefficient *= 1.2

    def slowDown(self, pos):
        self.addToExecutedEvents("Slowed Agents down")
        for a in self.agentList:
            a.speed /= 1.2
            a.speedCoefficient /= 1.2

    def raiseQuality(self, pos):
        for site in self.selectedSites:
            site.setQuality(site.getQuality() + 1)
            self.addToExecutedEvents(f"Raised site at {site.getPosition()}'s quality to {site.getQuality()}")
            site.setColor(site.getQuality())

    def lowerQuality(self, pos):
        for site in self.selectedSites:
            site.setQuality(site.getQuality() - 1)
            self.addToExecutedEvents(f"Lowered site at {site.getPosition()}'s quality to {site.getQuality()}")
            site.setColor(site.getQuality())

    def expand(self, pos):
        for site in self.selectedSites:
            site.setRadius(site.getRadius() + 1)
            self.addToExecutedEvents(f"Expanded site at {site.getPosition()}'s radius to {site.getRadius()}")

    def shrink(self, pos):
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

    def delete(self, pos):
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
        self.simDisp.numSelectedAgents = 0

    def appendNumber(self, number):
        if self.potentialQuality == 0 or self.potentialQuality > 25 or (self.potentialQuality == 25 and number > 5):
            self.setPotentialQuality(number)
        else:
            self.setPotentialQuality(self.potentialQuality * 10)
            self.setPotentialQuality(self.potentialQuality + number)
        self.simDisp.shouldDrawQuality = True

    def deleteLastDigit(self):
        if self.potentialQuality < 10:
            self.simDisp.shouldDrawQuality = False
        self.setPotentialQuality(int(self.potentialQuality / 10))

    def setSiteQuality(self):
        for site in self.selectedSites:
            if not site.isHub():
                self.addToExecutedEvents(f"Set quality of site at {site.getPosition()} to {self.potentialQuality}")
            site.setQuality(self.potentialQuality)
            site.setColor(self.potentialQuality)
        self.setPotentialQuality(0)
        self.simDisp.shouldDrawQuality = False

    @staticmethod
    def shouldDrawPlayButton():
        return True

    def playOrPause(self, _):
        self.simDisp.pauseButton.playOrPause()

    def play(self):
        pass

    def pause(self):
        self.simDisp.optionsScreen.hide()
        self.simDisp.timer.pause(self.handleEvent, self.simDisp.pauseButton.collides, self.simDisp.displayScreen)
        self.simDisp.optionsScreen.clear()
        self.simDisp.pauseButton.playOrPause()

    def options(self, _):
        if self.simDisp.pauseButton.isPaused:
            self.simDisp.optionsScreen.change()
