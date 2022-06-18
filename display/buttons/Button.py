import pygame

from Constants import WORDS_COLOR, BLUE
from config import Config
from display import Display


class Button:
    """ A generic button to be drawn on the screen and connected to an action that will be executed when the
     button is selected """

    def __init__(self, name, action, x, y, w=0, h=0, fontSize=int(Config.FONT_SIZE * 1.5)):
        """ name - the name of the button; may show up in the middle of the button if self.draw() isn't overridden
         action - an action that is executed when the box is clicked
         x - the left position of the box
         y - the right position of the box
         w - the width of the box
         h - the height of the box
         fontSize - size of the words to be written in the box """
        self.name = name
        self.font = pygame.font.SysFont('Comic Sans MS', fontSize)
        self.image = self.font.render(self.name, True, WORDS_COLOR).convert_alpha()
        w = self.image.get_width() if w == 0 else w
        h = self.image.get_height() if h == 0 else h
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action
        self.color = WORDS_COLOR
        self.x = x
        self.y = y
        self.yAdjustment = 0

    def draw(self):
        Display.blitImage(Display.screen, self.image, self.rect.topleft, False)

    def collides(self, pos):
        return self.rect.collidepoint(pos)

    def isOnHorizEdge(self, pos):
        return False

    def isOnVertEdge(self, pos):
        return False

    def changeColor(self, color):
        self.color = color
        self.image = self.font.render(self.name, True, color).convert_alpha()

    def adjustY(self, yAdjustment):
        self.yAdjustment += yAdjustment
        self.rect.top = self.y + self.yAdjustment

    def mouseButtonDown(self, pos):
        """ Handle the mouse down event and return whether other
        buttons should be disabled from handling this event """
        return self.collides(pos)

    def mouseButtonUp(self, pos):
        pass

    def update(self, pos):
        if self.collides(pos):
            self.changeColor(BLUE)
        else:
            self.changeColor(WORDS_COLOR)
