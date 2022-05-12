import pygame
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYUP, KMOD_CTRL

from config import Config
from display.mainmenu.MenuScreen import MenuScreen
from display.buttons.InputButton import InputButton
from display.simulation.ChatBox import ChatBox
from display.simulation.CommandHistBox import CommandHistBox
from display.simulation.PhaseGraph import PhaseGraph
from display.simulation.StateGraph import StateGraph


class SimulationDisplay(MenuScreen):

    def __init__(self, userControls, world):
        self.userControls = userControls
        self.userControls.initSimDisp(self)  # TODO: Take this out when we don't need it anymore
        self.chatBox = ChatBox()
        self.inputBox = InputButton(self.chatBox.rect.x + 10, self.chatBox.rect.y + self.chatBox.rect.h
                                    - Config.FONT_SIZE * 3.5, self.chatBox.rect.w - 20, Config.FONT_SIZE * 3, self.chatBox)
        self.chatBox.setInput(self.inputBox)
        self.commandHistBox = CommandHistBox()
        self.stateGraph = StateGraph(world.states)
        self.phaseGraph = PhaseGraph(world.phases)
        self.adjustables = [self.inputBox, self.chatBox, self.commandHistBox]
        # First button is handled first but drawn last
        super().__init__([self.inputBox, self.chatBox, self.commandHistBox, self.stateGraph, self.phaseGraph])

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
            self.userControls.handleEvent(event)

    def displayScreen(self):
        for button in reversed(self.buttons):
            button.draw()

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
