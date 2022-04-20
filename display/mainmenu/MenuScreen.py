import pygame
from pygame import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONUP, MOUSEMOTION

from ColonyExceptions import GameOver, BackException
from Constants import SCREEN_COLOR, BLUE, WORDS_COLOR
from display import Display


class MenuScreen:
    def __init__(self, buttons, screen=None):
        self.buttons = buttons
        self.screen = screen

    def run(self):
        try:
            while True:
                self.displayScreen()
                pygame.display.flip()  # Display drawn things on the screen
                self.handleEvents()  # Handle user input and stop reading if they chose the back button or exit
        except BackException:
            pass

    def displayScreen(self):
        try:
            self.screen.fill(SCREEN_COLOR)  # Fill in the background
            for button in self.buttons:
                button.draw()
        except AttributeError:
            self.screen = Display.screen
            self.displayScreen()

    def handleEvents(self):
        """ Handle user input """
        for event in pygame.event.get():
            print(str(event))
            self.handleEvent(event)

    def handleEvent(self, event):
        if event.type == MOUSEBUTTONUP:
            if event.button == 4:
                self.scrollUp()
            elif event.button == 5:
                self.scrollDown()
            elif event.button == 6:
                self.scrollUp(3)
            elif event.button == 7:
                self.scrollDown(3)
            elif event.button == 1:
                self.mouseButtonPressed(pygame.mouse.get_pos())
        elif event.type == MOUSEMOTION:
            self.updateButtonColors()
            self.updateCursor()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            self.escape()
        elif event.type == QUIT:
            self.exit()

    def escape(self):
        raise BackException()

    def mouseButtonPressed(self, pos):
        for button in self.buttons:
            if button.collides(pos):
                button.action()

    def scrollUp(self, times=1):
        for button in self.buttons:
            button.adjustY(10 * times)

    def scrollDown(self, times=1):
        for button in self.buttons:
            button.adjustY(-10 * times)

    def updateButtonColors(self):
        for button in self.buttons:
            if button.collides(pygame.mouse.get_pos()):
                button.changeColor(BLUE)
            else:
                button.changeColor(WORDS_COLOR)

    def updateCursor(self):
        """ Change the style of the mouse """
        cursorStyle = pygame.SYSTEM_CURSOR_HAND if self.collidesWithSelectable(pygame.mouse.get_pos()) \
            else pygame.SYSTEM_CURSOR_ARROW
        pygame.mouse.set_cursor(cursorStyle)

    def collidesWithSelectable(self, pos):
        for button in self.buttons:
            if button.collides(pos):
                return True
        return False

    @staticmethod
    def exit():
        """ Close the pygame window and exit the program """
        pygame.quit()
        raise GameOver("Exiting")
