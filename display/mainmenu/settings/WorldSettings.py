import pygame

from config import Config
from display import WorldDisplay, Display
from display.mainmenu.MenuScreen import MenuScreen
from display.mainmenu.buttons.BackButton import BackButton
from display.mainmenu.buttons.Button import Button
from model.World import World
from Constants import *


class WorldSettings(Button, MenuScreen):

    def __init__(self, x, y):
        super().__init__("World Settings", self.showWorld, x, y)
        self.buttons = [BackButton()]
        self.world = self.generateWorld()
        self.shouldDrawWorld = False
        self.numDraws = 0

    def draw(self):
        """ Draw the button that allows the user to see all settings """
        if self.shouldDrawWorld:
            if self.numDraws > 100:
                self.generateWorld()
                self.numDraws = 0
            WorldDisplay.drawWorldObjects(self.world, True)
            Display.write(Display.screen, int(Config.SIM_DURATION), int(Config.FONT_SIZE * 1.5), Display.origWidth - 100, 50)
            self.numDraws += 1
        img = pygame.font.SysFont('Comic Sans MS', Config.FONT_SIZE * 2)\
            .render("Draw current world", True, self.color).convert_alpha()
        self.rect = pygame.Rect(200, self.rect.top, img.get_width(), img.get_height())
        Display.blitImage(Display.screen, img, self.rect.topleft, adjust=False)

    def generateWorld(self):
        self.world = World(Config.NUM_HUBS, Config.NUM_SITES, Config.HUB_LOCATIONS,
                           Config.HUB_RADII, Config.HUB_AGENT_COUNTS, Config.SITE_POSITIONS,
                           Config.SITE_QUALITIES, Config.SITE_RADII, Config.SITE_RADIUS,
                           Config.NUM_PREDATORS, Config.PRED_POSITIONS, Config.NUM_LADYBUGS,
                           Config.LADYBUG_POSITIONS)
        WorldDisplay.initFog(self.world.getHubs())
        x = WorldDisplay.fog.get_width() / 2
        y = WorldDisplay.fog.get_height() / 2
        pygame.draw.circle(WorldDisplay.fog, TRANSPARENT, [x, y], Config.MAX_SEARCH_DIST, 0)
        for site in self.world.siteList:
            site.wasFound = True
        return self.world

    def showWorld(self):
        self.shouldDrawWorld = not self.shouldDrawWorld
