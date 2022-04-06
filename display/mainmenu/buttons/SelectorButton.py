import pygame

from ColonyExceptions import BackException
from Constants import WORDS_COLOR
from config import Config
from display import Display
from display.mainmenu.buttons.Button import Button


class SelectorButton(Button):

    def __init__(self, optionName, optionValue, x, y, selector, action=None):
        if action is None:
            action = self.select
        super().__init__(optionName, action, x, y)
        self.optionName = optionName
        self.optionValue = optionValue
        self.font = pygame.font.SysFont('Comic Sans MS', Config.LARGE_FONT_SIZE)  # TODO: Bring this up to Button
        self.image = self.font.render(self.optionName, True, WORDS_COLOR).convert_alpha()
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.selector = selector

    def select(self):
        self.selector.option = self.optionValue
        raise BackException()

    def draw(self):
        Display.blitImage(Display.screen, self.image, self.rect.topleft, False)

    def changeColor(self, color):
        super().changeColor(color)
        self.image = self.font.render(self.optionName, True, color).convert_alpha()
