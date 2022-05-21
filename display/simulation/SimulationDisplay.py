import pygame
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYUP, KMOD_CTRL, KEYDOWN, K_p

from Constants import GRAPHS_TOP_LEFT, SCREEN_COLOR
from config import Config
from display import Display
from display.buttons.PlayButton import PlayButton
from display.mainmenu.MenuScreen import MenuScreen
from display.buttons.InputButton import InputButton
from display.simulation.ChatBox import ChatBox
from display.simulation.CommandHistBox import CommandHistBox
from display.simulation.PhaseGraph import PhaseGraph
from display.simulation.StateGraph import StateGraph
from display.simulation.TimerDisplay import TimerDisplay
from display.simulation.WorldDisplay import drawWorldObjects


class SimulationDisplay(MenuScreen):

    def __init__(self, userControls, world, timer):
        self.userControls = userControls
        self.world = world
        self.timer = timer
        self.timerDisplay = TimerDisplay(timer)
        self.userControls.initSimDisp(self)  # TODO: Take this out when we don't need it anymore
        self.chatBox = ChatBox()
        self.inputBox = InputButton(self.chatBox.rect.x + 10, self.chatBox.rect.y + self.chatBox.rect.h
                                    - Config.FONT_SIZE * 3.5, self.chatBox.rect.w - 20, Config.FONT_SIZE * 3, self.chatBox)
        self.chatBox.setInput(self.inputBox)
        self.commandHistBox = CommandHistBox()
        self.stateGraph = StateGraph(world.states)
        self.phaseGraph = PhaseGraph(world.phases)
        self.pauseButton = PlayButton(self, Display.screen.get_width() - 60, GRAPHS_TOP_LEFT[1])
        self.adjustables = [self.inputBox, self.chatBox, self.commandHistBox]
        # First button is handled first but drawn last
        super().__init__([self.inputBox, self.chatBox, self.commandHistBox, self.stateGraph, self.phaseGraph,
                          self.pauseButton])

    def handleEvent(self, event):
        super().handleEvent(event)
        pos = pygame.mouse.get_pos()
        buttonIsSelected = False
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.mouseButtonDown(pos):
                    buttonIsSelected = True
                    break  # Skip the rest if one of the buttons handles it. We only want to press one at a time.
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                for button in self.buttons:
                    button.mouseButtonUp(pos)
            elif not pygame.key.get_mods() & KMOD_CTRL:
                self.scroll(event.button, pos)
        elif event.type == KEYUP:
            self.inputBox.input(event)
        if not self.inputBox.typing and not buttonIsSelected:
            if event.type == KEYDOWN and event.key == K_p:
                self.pauseButton.playOrPause()
            self.userControls.handleEvent(event)

    def displayScreen(self):
        if self.pauseButton.isPaused:
            self.drawPausedScreen()
        else:
            for button in reversed(self.buttons):
                button.draw()
            self.timerDisplay.drawRemainingTime()

    def drawPausedScreen(self):
        Display.screen.fill(SCREEN_COLOR)
        drawWorldObjects(self.world)
        self.userControls.drawChanges()
        for button in reversed(self.buttons):
            button.draw()
        self.timerDisplay.drawRemainingTime()
        Display.drawBorder()
        Display.drawPause(Display.screen)
        if self.userControls.shouldShowOptions:
            self.userControls.graphs.drawOptions()
        pygame.display.flip()

    def escape(self):
        pass

    def scrollUp(self, times=1):
        pass

    def scrollDown(self, times=1):
        pass

    def scroll(self, mouseButton, pos):
        if mouseButton == 4 or mouseButton == 6:
            for button in self.adjustables:
                if button.rect.collidepoint(pos):
                    button.scrollUp()
                    break  # Only scroll up on one
        elif mouseButton == 5 or mouseButton == 7:
            for button in self.adjustables:
                if button.rect.collidepoint(pos):
                    button.scrollDown()
                    break  # Only scroll up on one

    def updateCursor(self):
        isResizing = False
        for resizable in self.adjustables:
            if resizable.resizing():
                isResizing = True
                break
        if not isResizing:
            super().updateCursor()

    def shouldDrawPlayButton(self):
        return True

    def play(self):
        pass

    def pause(self):
        Display.drawPause(Display.screen)
        pygame.display.flip()
        self.timer.pause(self.handleEvent, self.pauseButton.collides, self.userControls.moveScreen)
        self.pauseButton.playOrPause()
