import pygame

from Constants import WORDS_COLOR, BLUE, FONT_SIZE_NAME
from display import Display


class SettingCategory:
    def __init__(self, name, rect, settingMenu):
        self.name = name
        self.rect = rect
        self.top = self.rect.top
        self.settingMenu = settingMenu
        self.isVisible = True
        self.yAdjustment = 0

    def adjustY(self, yAdjustment):
        self.yAdjustment = yAdjustment
        self.rect.top = self.top + self.yAdjustment

    def write(self):
        collides = self.rect.collidepoint(pygame.mouse.get_pos())
        arrow = 'v' if self.isVisible else '>'
        return Display.write(Display.screen, f"{arrow} {self.name}", int(self.settingMenu.data[FONT_SIZE_NAME] * 2),
                             self.rect.left, self.rect.top, BLUE if collides else WORDS_COLOR)
