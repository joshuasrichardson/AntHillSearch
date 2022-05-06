import pygame

from Constants import WORDS_COLOR, BLUE
from config import Config
from display import Display


class Button:

    def __init__(self, name, action, x, y, w=0, h=0, fontSize=int(Config.FONT_SIZE * 1.5), screen=None):
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
        self.screen = screen

    def draw(self):
        try:
            Display.blitImage(self.screen, self.image, self.rect.topleft, False)
        except AttributeError:
            self.screen = Display.screen
            self.draw()

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
        pass

    def mouseButtonUp(self, pos):
        pass

    def update(self, pos):
        if self.collides(pos):
            self.changeColor(BLUE)
        else:
            self.changeColor(WORDS_COLOR)
