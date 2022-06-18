import pygame
from pygame import KMOD_ALT

from Constants import STATES_LIST, WORDS_COLOR, GO
from config import Config
from display import Display
from display.buttons.Button import Button


class StateNumDisplay(Button):
    """ A display used to show the possible states and their corresponding numbers when the user holds down ALT """

    def __init__(self):
        super().__init__("State Numbers", lambda: None, 0, 0, fontSize=Config.FONT_SIZE)

    def draw(self):
        if pygame.key.get_mods() & KMOD_ALT:
            pos = list(pygame.mouse.get_pos())
            for i, state in enumerate(STATES_LIST):
                if i == GO:
                    break
                img = self.font.render(str(i) + ": " + state, True, WORDS_COLOR).convert_alpha()
                Display.screen.blit(img, pos)
                pos[1] += Config.FONT_SIZE

    def collides(self, pos):
        return False
