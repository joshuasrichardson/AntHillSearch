import time

import pygame
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYUP, K_RETURN

from config import Config
from display import Display
from display.mainmenu.MenuScreen import MenuScreen
from display.mainmenu.buttons.InputButton import InputButton
from display.simulation.ChatBox import ChatBox


class SimulationDisplay(MenuScreen):

    def __init__(self, userControls):
        self.userControls = userControls
        self.chatBox = ChatBox()
        self.inputBox = InputButton(self.chatBox.rect.x + 10, self.chatBox.rect.y + self.chatBox.rect.h
                                    - Config.FONT_SIZE * 3, self.chatBox.rect.w - 20, Config.FONT_SIZE * 2, self)
        super().__init__([self.chatBox, self.inputBox])

    def handleEvent(self, event):
        super().handleEvent(event)
        pos = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN:
            for button in self.buttons:
                # print(f"button: {button.name}")
                button.mouseButtonDown(pos)
        elif event.type == MOUSEBUTTONUP:
            for button in self.buttons:
                button.mouseButtonUp(pos)
        if event.type == KEYUP and self.inputBox.typing:
            if event.key == K_RETURN:
                self.inputBox.enter()
            else:
                self.inputBox.type(event.unicode)
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
        self.chatBox.addMessage("User", message)

    def escape(self):
        pass

    def scrollUp(self, times=1):
        pass

    def scrollDown(self, times=1):
        pass
