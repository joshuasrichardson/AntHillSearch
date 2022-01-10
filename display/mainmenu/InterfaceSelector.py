import pygame
from pygame import MOUSEBUTTONUP, MOUSEMOTION, KEYDOWN, K_ESCAPE, QUIT

from ColonyExceptions import GameOver
from Constants import SCREEN_COLOR, WORDS_COLOR, LARGE_FONT_SIZE, SEARCH_COLOR
from display import Display
from interface.EngineerInferface import EngineerInterface
from interface.UserInterface import UserInterface


class InterfaceSelector:

    def __init__(self):
        self.font = pygame.font.SysFont('Comic Sans MS', LARGE_FONT_SIZE)
        self.uiImage = self.font.render("User Interface: Practice like you will play", True, WORDS_COLOR).convert_alpha()
        self.uiButton = pygame.Rect((Display.origWidth / 2) - (self.uiImage.get_width() / 2), Display.origHeight / 2 - 2 * self.uiImage.get_height(),
                                    self.uiImage.get_width(), self.uiImage.get_height())  # The button to select the User Interface
        self.eiImage = self.font.render("Engineer Interface: See everything that is happening", True, WORDS_COLOR).convert_alpha()
        self.eiButton = pygame.Rect(Display.origWidth / 2 - (self.eiImage.get_width() / 2), Display.origHeight / 2,
                                    self.eiImage.get_width(), self.eiImage.get_height())  # The button to select the Engineering Interface
        self.interface = None

    def chooseInterface(self):
        """ Let the user choose between the UserInterface and the EngineerInterface for the practice round """
        reading = True
        while reading:  # Keep going till the game is over
            Display.screen.fill(SCREEN_COLOR)  # Fill in the background
            Display.blitImage(Display.screen, self.uiImage, self.uiButton.topleft, False)
            Display.blitImage(Display.screen, self.eiImage, self.eiButton.topleft, False)
            pygame.display.flip()  # Have the things that have been drawn show up
            reading = self.handleEvents()  # Handle any user input
        return self.interface

    def handleEvents(self):
        """ Handle user input """
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                return self.mouseButtonPressed(pygame.mouse.get_pos())
            elif event.type == MOUSEMOTION:
                self.updateCursor()
                self.updateWords(pygame.mouse.get_pos())
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.interface = None
                return False
            if event.type == QUIT:
                pygame.quit()
                raise GameOver("Game Over")
        return True

    def mouseButtonPressed(self, pos):
        """ What to do when the mouse button has been clicked """
        if self.uiButton.collidepoint(pos):
            self.interface = UserInterface
            return False
        elif self.eiButton.collidepoint(pos):
            self.interface = EngineerInterface
            return False
        return True

    def updateWords(self, pos):
        if self.uiButton.collidepoint(pos):
            self.uiImage = self.font.render("User Interface: Practice like you will play", True, SEARCH_COLOR).convert_alpha()
        else:
            self.uiImage = self.font.render("User Interface: Practice like you will play", True, WORDS_COLOR).convert_alpha()
        if self.eiButton.collidepoint(pos):
            self.eiImage = self.font.render("Engineer Interface: See everything that is happening", True, SEARCH_COLOR).convert_alpha()
        else:
            self.eiImage = self.font.render("Engineer Interface: See everything that is happening", True, WORDS_COLOR).convert_alpha()

    def updateCursor(self):
        """ Change the style of the mouse """
        cursorStyle = pygame.SYSTEM_CURSOR_HAND if self.collidesWithSelectable(pygame.mouse.get_pos()) \
            else pygame.SYSTEM_CURSOR_ARROW
        pygame.mouse.set_cursor(cursorStyle)

    def collidesWithSelectable(self, pos):
        return self.uiButton.collidepoint(pos) or self.eiButton.collidepoint(pos)
