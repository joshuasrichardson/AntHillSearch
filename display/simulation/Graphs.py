import pygame

from config import Config
from Constants import *
from display import Display


class SimulationGraphs:

    def __init__(self):

        self.font = pygame.font.SysFont('Comic Sans MS', Config.FONT_SIZE)  # The font used on the graphs

        self.screenBorder = None

        self.shouldDrawStateNumbers = False

    def drawStateNumbers(self):
        if self.shouldDrawStateNumbers:
            pos = list(pygame.mouse.get_pos())
            for i, state in enumerate(STATES_LIST):
                if i == GO:
                    break
                img = self.font.render(str(i) + ": " + state, True, WORDS_COLOR).convert_alpha()
                Display.screen.blit(img, pos)
                pos[1] += Config.FONT_SIZE

    def drawScreenBorder(self):
        if self.screenBorder is not None:
            Display.drawRect(Display.screen, ORANGE, pygame.Rect(self.screenBorder), 1, True)
