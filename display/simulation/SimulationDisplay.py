import pygame
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYUP, K_RETURN, K_BACKSPACE, K_ESCAPE, KMOD_CTRL

from config import Config
from display.mainmenu.MenuScreen import MenuScreen
from display.buttons.InputButton import InputButton
from display.simulation.ChatBox import ChatBox
from display.simulation.CommandHistBox import CommandHistBox


class SimulationDisplay(MenuScreen):

    def __init__(self, userControls):
        self.userControls = userControls
        self.userControls.initSimDisp(self)  # TODO: Take this out when we don't need it anymore
        self.chatBox = ChatBox()
        self.inputBox = InputButton(self.chatBox.rect.x + 10, self.chatBox.rect.y + self.chatBox.rect.h
                                    - Config.FONT_SIZE * 3, self.chatBox.rect.w - 20, Config.FONT_SIZE * 2, self)
        self.commandHistBox = CommandHistBox()
        self.adjustables = [self.chatBox, self.commandHistBox]
        super().__init__([self.chatBox, self.inputBox, self.commandHistBox])

    def handleEvent(self, event):
        super().handleEvent(event)
        pos = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                button.mouseButtonDown(pos)
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                for button in self.buttons:
                    button.mouseButtonUp(pos)
            elif not pygame.key.get_mods() & KMOD_CTRL:
                self.scroll(event.button, pos)
        if event.type == KEYUP:
            self.inputBox.input(event)
        else:
            self.userControls.handleEvent(event)

    def displayScreen(self):
        self.updateInputButton()
        for button in self.buttons:
            button.draw()

    def updateInputButton(self):
        self.inputBox.rect.centerx = self.chatBox.rect.centerx
        self.inputBox.rect.centery = self.chatBox.rect.y + self.chatBox.rect.h - Config.FONT_SIZE * 2

    def send(self, message):
        self.chatBox.addMessage(f"User: {message}")

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
        elif mouseButton == 5 or mouseButton == 7:
            for button in self.adjustables:
                if button.rect.collidepoint(pos):
                    button.scrollDown()

    def updateCursor(self):
        isResizing = False
        for resizable in self.adjustables:
            if resizable.resizing():
                isResizing = True
                break
        if not isResizing:
            super().updateCursor()
