import json

import Utils
from Constants import *
from display.mainmenu.MenuScreen import MenuScreen
from display.buttons.Title import Title
from display.buttons.BackButton import BackButton
from display.buttons.Button import Button
from display.mainmenu.settings.BooleanSetting import BooleanSetting
from display.mainmenu.settings.DrawingFunctions import *
from display.mainmenu.settings.IntegerSetting import IntegerSetting
from display.mainmenu.settings.ListSetting import ListSetting
from display.mainmenu.settings.PercentageSetting import PercentageSetting
from display.mainmenu.settings.PositionSetting import PositionSetting
from display.mainmenu.settings.SettingCategory import SettingCategory
from display.mainmenu.settings.StringSetting import StringSetting
from display.mainmenu.settings.WorldSettings import WorldSettings


class Settings(MenuScreen):
    """ A tab accessible from the main menu that allows the user to change certain settings for the simulation.
    Settings are changed by clicking on them, typing a new value, and pressing enter. Click anywhere to cancel.
    Not all settings can be changed here. See Config.py and Constants.py for more settings. """

    def __init__(self):
        # The rectangles that make values selectable
        Utils.copyJsonToConfig()  # Make sure the Config values match config.json
        self.settingsY = 200  # The y position of the word "Settings" on the screen
        self.categoryYs = []

        x = 200
        self.y = self.settingsY + 10
        self.settings = [
            PercentageSetting(CONVERGENCE_FRACTION_NAME, "Convergence Fraction", x, self.nextY(True), drawConvergenceFraction, self.save),
            BooleanSetting(USE_ROUNDS_AS_DURATION_NAME, "Use Rounds as Duration", x, self.nextY(), drawRoundsAsDuration, self.save),
            IntegerSetting(SIM_DURATION_NAME, "Simulation Duration", x, self.nextY(), showSimDuration, self.save),
            StringSetting(FLOOD_ZONE_SHAPE_NAME, "Flood Zone Shape", x, self.nextY(), drawFloodZone, self.save, getNextShape),
            PercentageSetting(FLOOD_ZONE_COVERAGE_NAME, "Flood Zone Coverage", x, self.nextY(), drawFloodZone, self.save),
            PositionSetting(FLOOD_ZONE_CORNERS_NAME, "Flood Zone Corners", x, self.nextY(), drawFloodZone, self.save),
            IntegerSetting(FONT_SIZE_NAME, "Font Size", x, self.nextY(), showFontSize, self.save),
            IntegerSetting(LARGE_FONT_SIZE_NAME, "Large Font Size", x, self.nextY(), showLargeFontSize, self.save),
            BooleanSetting(SHOULD_RECORD_NAME, "Should Record", x, self.nextY(), drawShouldRecord, self.save),
            BooleanSetting(RECORD_ALL_NAME, "Record All", x, self.nextY(), drawShouldRecord, self.save),
            BooleanSetting(FULL_CONTROL_NAME, "Full Control", x, self.nextY(), drawControls, self.save),
            BooleanSetting(DISTRACTED_NAME, "Distracted", x, self.nextY(), drawDistraction, self.save),
            IntegerSetting(NUM_HUBS_NAME, "Number of Hubs", x, self.nextY(True), drawNumHubs, self.save),
            PositionSetting(HUB_POSITIONS_NAME, "Hub Locations", x, self.nextY(), drawHubsPositions, self.save),
            ListSetting(HUB_RADII_NAME, "Hub Radii", x, self.nextY(), drawHubsRadii, self.save),
            ListSetting(HUB_AGENT_COUNTS_NAME, "Hub Agent Counts", x, self.nextY(), drawHubsCounts, self.save),
            IntegerSetting(NUM_SITES_NAME, "Number of Sites", x, self.nextY(True), drawNumSites, self.save),
            PositionSetting(SITE_POSITIONS_NAME, "Site Positions", x, self.nextY(), drawSitesPositions, self.save),
            ListSetting(SITE_RADII_NAME, "Site Radii", x, self.nextY(), drawSitesRadii, self.save),
            ListSetting(SITE_QUALITIES_NAME, "Site Qualities", x, self.nextY(), drawSitesQualities, self.save),
            IntegerSetting(SITE_RADIUS_NAME, "Default Site Radius", x, self.nextY(), drawSiteRadius, self.save),
            IntegerSetting(SITE_NO_CLOSER_THAN_NAME, "Site No Closer Than", x, self.nextY(), drawNoCloserThan, self.save),
            IntegerSetting(SITE_NO_FARTHER_THAN_NAME, "Site No Farther Than", x, self.nextY(), drawNoFartherThan, self.save),
            IntegerSetting(MAX_SEARCH_DIST_NAME, "Max Search Distance", x, self.nextY(True), drawSearchArea, self.save),
            StringSetting(AGENT_IMAGE_NAME, "Agent Image", x, self.nextY(), drawAgents, self, getOtherFile),
            IntegerSetting(NUM_PREDATORS_NAME, "Number of Predators", x, self.nextY(True), drawPredators, self.save),
            PositionSetting(PRED_POSITIONS_NAME, "Predator Positions", x, self.nextY(), drawPredPositions, self.save),
            IntegerSetting(NUM_LADYBUGS_NAME, "Number of Ladybugs", x, self.nextY(), drawLadybugs, self.save),
            PositionSetting(LADYBUG_POSITIONS_NAME, "Ladybug Positions", x, self.nextY(), drawLadybugPositions, self.save),
            IntegerSetting(NUM_OBSTACLES_NAME, "Number of Obstacles", x, self.nextY(True), drawObstacles, self.save),
            PositionSetting(OBSTACLE_POSITIONS_NAME, "Obstacle Positions", x, self.nextY(), drawObstaclePositions, self.save)
        ]

        self.categories = [
            SettingCategory("General", x, self.categoryYs[0], self.settings[0:12], self.settings, self.adjustCategoryPos),
            SettingCategory("Hubs", x, self.categoryYs[1], self.settings[12:16], self.settings[12:], self.adjustCategoryPos),
            SettingCategory("Sites", x, self.categoryYs[2], self.settings[16:23], self.settings[16:], self.adjustCategoryPos),
            SettingCategory("Agents", x, self.categoryYs[3], self.settings[23:25], self.settings[23:], self.adjustCategoryPos),
            SettingCategory("Bugs", x, self.categoryYs[4], self.settings[25:29], self.settings[25:], self.adjustCategoryPos),
            SettingCategory("Obstacles", x, self.categoryYs[5], self.settings[29:], self.settings[29:], self.adjustCategoryPos)
        ]

        self.worldSettings = WorldSettings(200, self.settingsY - 40)

        super().__init__([self.worldSettings,
                          Title("Settings", self.settingsY),
                          BackButton(),
                          Button("Set all to default", self.setAllToDefault, 200, self.settingsY - 10),
                          *self.settings,
                          *self.categories])

    def setAllToDefault(self):
        Utils.resetConfig()
        with open(CONFIG_FILE_NAME, 'w') as file:
            data = {}
            for setting in self.settings:
                exec("from config import Config")
                setting.value = eval(f"Config.{setting.key}")
                setting.savedValue = setting.value
                data[setting.key] = setting.value
            json.dump(data, file)
        self.worldSettings.generateWorld()

    def adjustCategoryPos(self, category, adjustment):
        start = self.categories.index(category) + 1
        for i in range(start, len(self.categories)):
            self.categories[i].adjustY(adjustment)

    def nextY(self, newCategory=False):
        if newCategory:
            self.y += 20
            self.categoryYs.append(self.y)
            self.y += 30
        y = self.y
        self.y += 25
        return y

    def save(self, key, value):
        with open(CONFIG_FILE_NAME, 'r') as file:
            data = json.load(file)
        data[key] = value
        with open(CONFIG_FILE_NAME, 'w') as file:
            json.dump(data, file)
        Utils.copyJsonToConfig()
        self.worldSettings.generateWorld()
