import pygame
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYUP, K_RETURN, K_BACKSPACE, K_ESCAPE, KMOD_CTRL

from config import Config
from display.mainmenu.MenuScreen import MenuScreen
from display.mainmenu.buttons.InputButton import InputButton
from display.simulation.ChatBox import ChatBox


class SimulationDisplay(MenuScreen):

    def __init__(self, userControls):
        self.userControls = userControls
        self.chatBox = ChatBox()
        self.inputBox = InputButton(self.chatBox.rect.x + 10, self.chatBox.rect.y + self.chatBox.rect.h
                                    - Config.FONT_SIZE * 3, self.chatBox.rect.w - 20, Config.FONT_SIZE * 2, self)
        self.scrollables = [self.chatBox]
        super().__init__([self.chatBox, self.inputBox])

    def handleEvent(self, event):
        super().handleEvent(event)
        pos = pygame.mouse.get_pos()
        if self.collidesWithSelectable(pos) or self.inputBox.typing:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    button.mouseButtonDown(pos)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    for button in self.buttons:
                        button.mouseButtonUp(pos)
                elif not pygame.key.get_mods() & KMOD_CTRL:
                    self.scroll(event.button, pos)
            if event.type == KEYUP and self.inputBox.typing:
                if event.key == K_RETURN:
                    self.inputBox.enter()
                elif event.key == K_BACKSPACE:
                    self.inputBox.backspace()
                elif event.key == K_ESCAPE:
                    self.inputBox.escape()
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

    def scroll(self, mouseButton, pos):
        if mouseButton == 4 or mouseButton == 6:
            for button in self.scrollables:
                if button.rect.collidepoint(pos):
                    button.scrollUp()
        elif mouseButton == 5 or mouseButton == 7:
            for button in self.scrollables:
                if button.rect.collidepoint(pos):
                    button.scrollDown()
