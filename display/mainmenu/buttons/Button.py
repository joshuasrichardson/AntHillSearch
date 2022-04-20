import pygame

from Constants import WORDS_COLOR
from config import Config
from display import Display


class Button:

    def __init__(self, name, action, x, y, fontSize=int(Config.FONT_SIZE * 1.5), screen=None):
        self.name = name
        self.font = pygame.font.SysFont('Comic Sans MS', fontSize)
        self.image = self.font.render(self.name, True, WORDS_COLOR).convert_alpha()
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
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

    def changeColor(self, color):
        self.color = color
        self.image = self.font.render(self.name, True, color).convert_alpha()

    def adjustY(self, yAdjustment):
        self.yAdjustment += yAdjustment
        self.rect.top = self.y + self.yAdjustment
