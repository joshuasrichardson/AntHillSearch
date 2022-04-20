from Constants import BLUE
from config import Config
from display import Display
from display.simulation import FogDisplay, WorldDisplay
from display.mainmenu.MenuScreen import MenuScreen
from display.mainmenu.buttons.BackButton import BackButton
from display.mainmenu.buttons.Button import Button
from model.World import World


class WorldSettings(Button, MenuScreen):

    def __init__(self, x, y):
        super().__init__("Draw current world", self.showWorld, x, y)
        self.buttons = [BackButton()]
        self.world = None
        self.shouldDrawWorld = False
        self.numDraws = 100  # Start at 100 to make it generate a world on the first draw

    def draw(self):
        """ Draw the button that allows the user to see all settings """
        if self.shouldDrawWorld:
            if self.numDraws > 99:
                self.generateWorld()
                self.numDraws = 0
            WorldDisplay.drawWorldObjects(self.world, True)
            Display.write(Display.screen, int(Config.SIM_DURATION), int(Config.FONT_SIZE * 1.5), Display.origWidth - 100, 50)
            self.numDraws += 1
        super().draw()

    def generateWorld(self):
        self.world = World(Config.NUM_HUBS, Config.NUM_SITES, Config.HUB_POSITIONS,
                           Config.HUB_RADII, Config.HUB_AGENT_COUNTS, Config.SITE_POSITIONS,
                           Config.SITE_QUALITIES, Config.SITE_RADII, Config.SITE_RADIUS,
                           Config.NUM_PREDATORS, Config.PRED_POSITIONS, Config.NUM_LADYBUGS,
                           Config.LADYBUG_POSITIONS)
        FogDisplay.clearExplorableArea(self.world)
        for site in self.world.siteList:
            site.wasFound = True
        return self.world

    def showWorld(self):
        self.shouldDrawWorld = not self.shouldDrawWorld

    def changeColor(self, color):
        super().changeColor((50, 200, 50) if self.shouldDrawWorld and color != BLUE else color)
