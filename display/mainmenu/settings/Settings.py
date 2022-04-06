import json

import Utils
from Constants import *
from display.mainmenu.buttons.BackButton import BackButton
from display.mainmenu.MenuScreen import MenuScreen
from display.mainmenu.buttons.Title import Title
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
    Not all settings are able to be changed here. See Constants.py for more settings. """

    def __init__(self):
        # The rectangles that make values selectable
        self.data = {}  # The data about the settings to be recorded to settings.json
        self.setDataUsingConfig()  # Set the values on the screen to match the values in settings.json
        self.settingsY = 90  # The y position of the word "Settings" on the screen
        self.categoryYs = []

        x = 200
        self.y = 100
        self.settings = [
            PercentageSetting(CONVERGENCE_FRACTION_NAME, "Convergence Fraction", x, self.nextY(True), drawConvergenceFraction, self),
            BooleanSetting(USE_ROUNDS_AS_DURATION_NAME, "Use Rounds as Duration", x, self.nextY(), drawRoundsAsDuration, self),
            IntegerSetting(SIM_DURATION_NAME, "Simulation Duration", x, self.nextY(), showSimDuration, self),
            PercentageSetting(FLOOD_ZONE_COVERAGE_NAME, "Flood Zone Coverage", x, self.nextY(), drawFloodZone, self),
            PositionSetting(FLOOD_ZONE_CORNERS_NAME, "Flood Zone Corners", x, self.nextY(), drawFloodZone, self),
            IntegerSetting(FONT_SIZE_NAME, "Font Size", x, self.nextY(), showFontSize, self),
            IntegerSetting(LARGE_FONT_SIZE_NAME, "Large Font Size", x, self.nextY(), showLargeFontSize, self),
            BooleanSetting(SHOULD_RECORD_NAME, "Should Record", x, self.nextY(), drawShouldRecord, self),
            BooleanSetting(RECORD_ALL_NAME, "Record All", x, self.nextY(), drawShouldRecord, self),
            BooleanSetting(FULL_CONTROL_NAME, "Full Control", x, self.nextY(), drawControls, self),
            BooleanSetting(DISTRACTED_NAME, "Distracted", x, self.nextY(), drawDistraction, self),
            IntegerSetting(NUM_HUBS_NAME, "Number of Hubs", x, self.nextY(True), drawNumHubs, self),
            PositionSetting(HUB_LOCATIONS_NAME, "Hub Locations", x, self.nextY(), drawHubsPositions, self),
            ListSetting(HUB_RADII_NAME, "Hub Radii", x, self.nextY(), drawHubsRadii, self),
            ListSetting(HUB_AGENT_COUNTS_NAME, "Hub Agent Counts", x, self.nextY(), drawHubsCounts, self),
            IntegerSetting(NUM_SITES_NAME, "Number of Sites", x, self.nextY(True), drawNumSites, self),
            PositionSetting(SITE_POSITIONS_NAME, "Site Positions", x, self.nextY(), drawSitesPositions, self),
            ListSetting(SITE_RADII_NAME, "Site Radii", x, self.nextY(), drawSitesRadii, self),
            ListSetting(SITE_QUALITIES_NAME, "Site Qualities", x, self.nextY(), drawSitesQualities, self),
            IntegerSetting(SITE_RADIUS_NAME, "Default Site Radius", x, self.nextY(), drawSiteRadius, self),
            IntegerSetting(SITE_NO_CLOSER_THAN_NAME, "Site No Closer Than", x, self.nextY(), drawNoCloserThan, self),
            IntegerSetting(SITE_NO_FARTHER_THAN_NAME, "Site No Farther Than", x, self.nextY(), drawNoFartherThan, self),
            IntegerSetting(MAX_SEARCH_DIST_NAME, "Max Search Distance", x, self.nextY(True), drawSearchArea, self),
            StringSetting(AGENT_IMAGE_NAME, "Agent Image", x, self.nextY(), drawAgents, self, getOtherFile),
            IntegerSetting(NUM_PREDATORS_NAME, "Number of Predators", x, self.nextY(True), drawPredators, self),
            PositionSetting(PRED_POSITIONS_NAME, "Predator Positions", x, self.nextY(), drawPredPositions, self),
            IntegerSetting(NUM_LADYBUGS_NAME, "Number of Ladybugs", x, self.nextY(), drawLadybugs, self),
            PositionSetting(LADYBUG_POSITIONS_NAME, "Ladybug Positions", x, self.nextY(), drawLadybugPositions, self)
        ]

        self.categories = [
            SettingCategory("General", x, self.categoryYs[0], self.settings[0:11], self.settings, self.adjustCategoryPos),
            SettingCategory("Hubs", x, self.categoryYs[1], self.settings[11:15], self.settings[11:], self.adjustCategoryPos),
            SettingCategory("Sites", x, self.categoryYs[2], self.settings[15:22], self.settings[15:], self.adjustCategoryPos),
            SettingCategory("Agents", x, self.categoryYs[3], self.settings[22:24], self.settings[22:], self.adjustCategoryPos),
            SettingCategory("Bugs", x, self.categoryYs[4], self.settings[24:], self.settings[24:], self.adjustCategoryPos)
        ]

        self.worldSettings = WorldSettings(200, self.settingsY - 20)

        super().__init__([Title("Settings", 90),
                          BackButton(),
                          self.worldSettings,
                          *self.settings,
                          *self.categories])

    def adjustCategoryPos(self, category, adjustment):
        start = self.categories.index(category) + 1
        for i in range(start, len(self.categories)):
            self.categories[i].adjustY(adjustment)

    def nextY(self, newCategory=False):
        if newCategory:
            self.y += 35
            self.categoryYs.append(self.y)
            self.y += 30
        y = self.y
        self.y += 25
        return y

    def setDataUsingConfig(self):
        """ Set the values on the screen to match the values in settings.json """
        try:
            with open(CONFIG_FILE_NAME, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print(f"File '{CONFIG_FILE_NAME}' was not found")
        except json.decoder.JSONDecodeError:
            print(f"File '{CONFIG_FILE_NAME}' is empty")

    def save(self, key, value):
        self.data[key] = value
        with open(CONFIG_FILE_NAME, 'w') as file:
            json.dump(self.data, file)
        Utils.copyJsonToConfig()
        self.worldSettings.generateWorld()
