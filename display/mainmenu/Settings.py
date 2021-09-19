import pygame
from pygame import MOUSEBUTTONUP, QUIT, MOUSEMOTION

from ColonyExceptions import GameOver
from display import Display
from Constants import *


class Settings:

    def __init__(self):
        self.values = [["Convergence Fraction", CONVERGENCE_FRACTION],
                       ["Simulation Duration", SIM_DURATION],
                       ["Font Size", FONT_SIZE],
                       ["Large Font Size", LARGE_FONT_SIZE],
                       ["Number of Hubs", NUM_HUBS],
                       ["Hub Locations", HUB_LOCATIONS],
                       ["Hub Radii", HUB_RADII],
                       ["Hub Agent Counts", HUB_AGENT_COUNTS],
                       ["Number of Sites", NUM_SITES],
                       ["Site Positions", SITE_POSITIONS],
                       ["Site Qualities", SITE_QUALITIES],
                       ["Site Radii", SITE_RADII],
                       ["Should Record", SHOULD_RECORD],
                       ["Default Site Radius", SITE_RADIUS],
                       ["Site No Closer Than", SITE_NO_CLOSER_THAN],
                       ["Site No Farther Than", SITE_NO_FARTHER_THAN],
                       ["Agent Image", AGENT_IMAGE],
                       ["Max Search Distance", MAX_SEARCH_DIST]]
        self.valueRects = [pygame.Rect(0, 0, 0, 0),
                           pygame.Rect(0, 0, 0, 0),
                           pygame.Rect(0, 0, 0, 0),
                           pygame.Rect(0, 0, 0, 0),
                           pygame.Rect(0, 0, 0, 0),
                           pygame.Rect(0, 0, 0, 0),
                           pygame.Rect(0, 0, 0, 0),
                           pygame.Rect(0, 0, 0, 0),
                           pygame.Rect(0, 0, 0, 0),
                           pygame.Rect(0, 0, 0, 0),
                           pygame.Rect(0, 0, 0, 0),
                           pygame.Rect(0, 0, 0, 0),
                           pygame.Rect(0, 0, 0, 0),
                           pygame.Rect(0, 0, 0, 0),
                           pygame.Rect(0, 0, 0, 0),
                           pygame.Rect(0, 0, 0, 0),
                           pygame.Rect(0, 0, 0, 0),
                           pygame.Rect(0, 0, 0, 0)]
        self.backButton = pygame.Rect(0, 0, 0, 0)

    def run(self):
        try:
            reading = True
            while reading:
                Display.screen.fill(SCREEN_COLOR)
                Display.writeCenterPlus(Display.screen, "Settings", LARGE_FONT_SIZE, -6 * LARGE_FONT_SIZE)
                self.showSettings()
                self.drawBackButton()
                pygame.display.flip()
                reading = self.handleEvents()
        except GameOver:
            pass

    def showSettings(self):
        x = 200
        for i, value in enumerate(self.values):
            self.valueRects[i] = Display.write(Display.screen, value[0] + ": " + str(value[1]), int(FONT_SIZE * 1.5), x, 100 + i * FONT_SIZE * 2.3)

    def drawBackButton(self):
        backImg = pygame.font.SysFont('Comic Sans MS', FONT_SIZE * 2).render("<- BACK", True, WORDS_COLOR).convert_alpha()
        self.backButton = pygame.Rect(50, 50, backImg.get_width(), backImg.get_height())
        Display.screen.blit(backImg, self.backButton.topleft)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                return self.mouseButtonPressed(pygame.mouse.get_pos())
            elif event.type == MOUSEMOTION:
                self.setMouse()
            if event.type == QUIT:
                pygame.quit()
                raise GameOver("Game Over")
        return True

    def mouseButtonPressed(self, pos):
        if self.backButton.collidepoint(pos):
            return False
        return True

    def setMouse(self):
        if self.collidesWithSelectable(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def collidesWithSelectable(self, pos):
        if self.backButton.collidepoint(pos):
            return True
        for rect in self.valueRects:
            if rect.collidepoint(pos):
                return True
        return False
