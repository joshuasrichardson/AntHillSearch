import pygame

from display import WorldDisplay, Display
from model.World import World
from Constants import *


class WorldSettings:

    def __init__(self, menu):
        self.menu = menu
        self.world = self.generateWorld()
        self.shouldDrawWorld = False
        self.showWorldButton = pygame.Rect(0, 0, 0, 0)  # Button to show all settings
        self.numDraws = 0

    def generateWorld(self):
        world = World(self.menu.data[NUM_HUBS_NAME], self.menu.data[NUM_SITES_NAME], self.menu.data[HUB_LOCATIONS_NAME],
                      self.menu.data[HUB_RADII_NAME], self.menu.data[HUB_AGENT_COUNTS_NAME], self.menu.data[SITE_POSITIONS_NAME],
                      self.menu.data[SITE_QUALITIES_NAME], self.menu.data[SITE_RADII_NAME], self.menu.data[SITE_RADIUS_NAME],
                      self.menu.data[NUM_PREDATORS_NAME], self.menu.data[PRED_POSITIONS_NAME])
        WorldDisplay.initFog(world.getHubs())
        x = WorldDisplay.fog.get_width() / 2
        y = WorldDisplay.fog.get_height() / 2
        pygame.draw.circle(WorldDisplay.fog, TRANSPARENT, [x, y], self.menu.data[MAX_SEARCH_DIST_NAME], 0)
        for site in world.siteList:
            site.wasFound = True
        return world

    def showWorld(self):
        if self.shouldDrawWorld:
            if self.numDraws > 100:
                self.world = self.generateWorld()
                self.numDraws = 0
            WorldDisplay.drawWorldObjects(self.world, True)
            Display.write(Display.screen, self.menu.data[SIM_DURATION_NAME], int(self.menu.data[FONT_SIZE_NAME] * 1.5), Display.origWidth - 100, 50)
            self.numDraws += 1
        else:
            self.drawShowWorldButton()

    def drawShowWorldButton(self):
        """ Draw the button that allows the user to see all settings """
        color = BLUE if self.showWorldButton.collidepoint(pygame.mouse.get_pos()) else WORDS_COLOR
        img = pygame.font.SysFont('Comic Sans MS', self.menu.data["FONT_SIZE"] * 2).render("Draw current world", True, color).convert_alpha()
        self.showWorldButton = pygame.Rect(200, 50, img.get_width(), img.get_height())
        Display.screen.blit(img, self.showWorldButton.topleft)
