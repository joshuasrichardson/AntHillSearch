import pygame

from Constants import WORDS_COLOR
from config import Config
from display import Display


class Button:
    def __init__(self, name, action, x, y):
        self.name = name
        self.rect = pygame.Rect(x, y, 0, 0)
        self.action = action
        self.color = WORDS_COLOR
        self.x = x
        self.y = y
        self.yAdjustment = 0

    def draw(self):
        words = pygame.font.SysFont('Comic Sans MS', Config.FONT_SIZE * 2).render(self.name, True, self.color).convert_alpha()
        self.rect = pygame.Rect(*self.rect.topleft, words.get_width(), words.get_height())
        Display.blitImage(Display.screen, words, self.rect.topleft, adjust=False)

    def collides(self, pos):
        return self.rect.collidepoint(pos)

    def changeColor(self, color):
        self.color = color

    def adjustY(self, yAdjustment):
        self.yAdjustment += yAdjustment
        self.rect.top = self.y + self.yAdjustment
