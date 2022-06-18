import pygame
from pygame import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONUP, MOUSEMOTION

from ColonyExceptions import GameOver, BackException
from Constants import SCREEN_COLOR
from display import Display


class MenuScreen:
    """ A generic screen for the simulation. Displays the screen and handles some events. Also
    contains a list of buttons that it can select when the user clicks on them. """

    def __init__(self, buttons):
        """ buttons - the buttons to be managed by this screen """
        self.buttons = buttons

    def run(self):
        """ Starts a loop that displays the screen and handles user input until the user goes back to a previous
         screen or exits the program """
        try:
            while True:
                self.displayScreen()
                pygame.display.flip()  # Display drawn things on the screen
                self.handleEvents()  # Handle user input and stop reading if they chose the back button or exit
        except BackException:
            pass

    def displayScreen(self):
        Display.screen.fill(SCREEN_COLOR)  # Fill in the background
        for button in self.buttons:
            button.draw()

    def handleEvents(self):
        """ Handle user input """
        for event in pygame.event.get():
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
            self.updateButtons()
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
            button.mouseButtonUp(pos)

    def scrollUp(self, times=1):
        for button in self.buttons:
            button.adjustY(10 * times)

    def scrollDown(self, times=1):
        for button in self.buttons:
            button.adjustY(-10 * times)

    def updateButtons(self):
        pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(pos)

    def updateCursor(self):
        """ Change the style of the mouse """
        pos = pygame.mouse.get_pos()
        if self.collidesWithHorizEdge(pos):
            if self.collidesWithVertEdge(pos):
                cursorStyle = pygame.SYSTEM_CURSOR_SIZEALL
            else:
                cursorStyle = pygame.SYSTEM_CURSOR_SIZENS
        elif self.collidesWithVertEdge(pos):
            cursorStyle = pygame.SYSTEM_CURSOR_SIZEWE
        elif self.collidesWithSelectable(pos):
            cursorStyle = pygame.SYSTEM_CURSOR_HAND
        else:
            cursorStyle = pygame.SYSTEM_CURSOR_ARROW
        pygame.mouse.set_cursor(cursorStyle)

    def collidesWithSelectable(self, pos):
        for button in self.buttons:
            if button.collides(pos):
                return True
        return False

    def collidesWithHorizEdge(self, pos):
        for button in self.buttons:
            if button.isOnHorizEdge(pos):
                return True
        return False

    def collidesWithVertEdge(self, pos):
        for button in self.buttons:
            if button.isOnVertEdge(pos):
                return True
        return False

    @staticmethod
    def exit():
        """ Close the pygame window and exit the program """
        pygame.quit()
        raise GameOver("Exiting")
