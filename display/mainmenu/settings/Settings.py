import json
from functools import reduce

from pygame import MOUSEBUTTONUP, QUIT, MOUSEMOTION, KEYDOWN, K_ESCAPE

from ColonyExceptions import GameOver
from Constants import *
from display.mainmenu.settings.BooleanSetting import BooleanSetting
from display.mainmenu.settings.DrawingFunctions import *
from display.mainmenu.settings.IntegerSetting import IntegerSetting
from display.mainmenu.settings.ListSetting import ListSetting
from display.mainmenu.settings.PercentageSetting import PercentageSetting
from display.mainmenu.settings.PositionSetting import PositionSetting
from display.mainmenu.settings.SettingCategory import SettingCategory
from display.mainmenu.settings.StringSetting import StringSetting
from display.mainmenu.settings.WorldSettings import WorldSettings


class Settings:
    """ A tab accessible from the main menu that allows the user to change certain settings for the simulation.
    Not all settings are able to be changed here. See Constants.py for more settings. """

    def __init__(self):
        # The rectangles that make values selectable
        self.backButton = pygame.Rect(0, 0, 0, 0)  # Button to go back to the main menu
        self.data = {}  # The data about the settings to be recorded to settings.json
        self.setDataUsingConfig()  # Set the values on the screen to match the values in settings.json
        self.settingsY = 90  # The y position of the word "Settings" on the screen
        self.categoryYs = []

        x = 200
        self.y = 100
        self.settings = [
            PercentageSetting(CONVERGENCE_FRACTION_NAME, "Convergence Fraction", 0, x, self.nextY(True), drawConvergenceFraction, self),
            BooleanSetting(USE_ROUNDS_AS_DURATION_NAME, "Use Rounds as Duration", 0, x, self.nextY(), drawRoundsAsDuration, self),
            IntegerSetting(SIM_DURATION_NAME, "Simulation Duration", 0, x, self.nextY(), showSimDuration, self),
            PercentageSetting(FLOOD_ZONE_COVERAGE_NAME, "Flood Zone Coverage", 0, x, self.nextY(), drawConvergenceFraction, self),
            PositionSetting(FLOOD_ZONE_CORNERS_NAME, "Flood Zone Corners", 0, x, self.nextY(), drawHubsPositions, self),
            IntegerSetting(FONT_SIZE_NAME, "Font Size", 0, x, self.nextY(), showFontSize, self),
            IntegerSetting(LARGE_FONT_SIZE_NAME, "Large Font Size", 0, x, self.nextY(), showLargeFontSize, self),
            BooleanSetting(SHOULD_RECORD_NAME, "Should Record", 0, x, self.nextY(), drawShouldRecord, self),
            BooleanSetting(RECORD_ALL_NAME, "Record All", 0, x, self.nextY(), drawShouldRecord, self),
            BooleanSetting(FULL_CONTROL_NAME, "Full Control", 0, x, self.nextY(), drawControls, self),
            BooleanSetting(DISTRACTED_NAME, "Distracted", 0, x, self.nextY(), drawDistraction, self),
            IntegerSetting(NUM_HUBS_NAME, "Number of Hubs", 1, x, self.nextY(True), drawNumHubs, self),
            PositionSetting(HUB_LOCATIONS_NAME, "Hub Locations", 1, x, self.nextY(), drawHubsPositions, self),
            ListSetting(HUB_RADII_NAME, "Hub Radii", 1, x, self.nextY(), drawHubsRadii, self),
            ListSetting(HUB_AGENT_COUNTS_NAME, "Hub Agent Counts", 1, x, self.nextY(), drawHubsCounts, self),
            IntegerSetting(NUM_SITES_NAME, "Number of Sites", 2, x, self.nextY(True), drawNumSites, self),
            PositionSetting(SITE_POSITIONS_NAME, "Site Positions", 2, x, self.nextY(), drawSitesPositions, self),
            ListSetting(SITE_RADII_NAME, "Site Radii", 2, x, self.nextY(), drawSitesRadii, self),
            ListSetting(SITE_QUALITIES_NAME, "Site Qualities", 2, x, self.nextY(), drawSitesQualities, self),
            IntegerSetting(SITE_RADIUS_NAME, "Default Site Radius", 2, x, self.nextY(), drawSiteRadius, self),
            IntegerSetting(SITE_NO_CLOSER_THAN_NAME, "Site No Closer Than", 2, x, self.nextY(), drawNoCloserThan, self),
            IntegerSetting(SITE_NO_FARTHER_THAN_NAME, "Site No Farther Than", 2, x, self.nextY(), drawNoFartherThan, self),
            IntegerSetting(MAX_SEARCH_DIST_NAME, "Max Search Distance", 3, x, self.nextY(True), drawSearchArea, self),
            StringSetting(AGENT_IMAGE_NAME, "Agent Image", 3, x, self.nextY(), drawAgents, self, getOtherFile),
            IntegerSetting(NUM_PREDATORS_NAME, "Number of Predators", 4, x, self.nextY(True), drawPredators, self),
            PositionSetting(PRED_POSITIONS_NAME, "Predator Positions", 4, x, self.nextY(), drawPredPositions, self),
            IntegerSetting(NUM_LADYBUGS_NAME, "Number of Ladybugs", 4, x, self.nextY(), drawLadybugs, self),
            PositionSetting(LADYBUG_POSITIONS_NAME, "Ladybug Positions", 4, x, self.nextY(), drawLadybugPositions, self)
        ]
        self.worldSettings = None

        self.categories = [
            SettingCategory("General", pygame.Rect(x, self.categoryYs[0], 100, 25), self),
            SettingCategory("Hubs", pygame.Rect(x, self.categoryYs[1], 100, 25), self),
            SettingCategory("Sites", pygame.Rect(x, self.categoryYs[2], 100, 25), self),
            SettingCategory("Agents", pygame.Rect(x, self.categoryYs[3], 100, 25), self),
            SettingCategory("Bugs", pygame.Rect(x, self.categoryYs[4], 100, 25), self)
        ]

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

    def run(self):
        self.worldSettings = WorldSettings(self)
        reading = True
        while reading:  # While the user is reading the settings (or hasn't tried to exit)
            Display.screen.fill(SCREEN_COLOR)  # Fill in the background
            self.worldSettings.showWorld(self.settingsY - 20)  # Draw the world with the current settings or a button to enable this
            self.showSettings()  # Draw the setting the user can select and change
            self.drawBackButton()  # Draw the button used to return to the main menu
            pygame.display.flip()  # Display drawn things on the screen
            reading = self.handleEvents()  # Handle user input and stop reading if they chose the back button or exit

    def showSettings(self):
        """ Write each value on the screen """
        if not self.worldSettings.shouldDrawWorld:
            Display.writeCenterPlus(Display.screen, "Settings", self.data["LARGE_FONT_SIZE"],
                                    -Display.origHeight / 2 + self.settingsY)
            yAdjustment = 0
            yAdjustments = []
            for i, category in enumerate(self.categories):
                category.adjustY(-yAdjustment)
                category.write()
                if not category.isVisible:
                    yAdjustment += reduce(lambda x, y: x + y, [25 for setting in self.settings if setting.categoryIndex == i])
                yAdjustments.append(yAdjustment)
            for setting in self.settings:
                if self.categories[setting.categoryIndex].isVisible:
                    setting.adjustY(-yAdjustments[setting.categoryIndex])
                    setting.write()
            # TODO: Indicate that they can scroll up or down if they have settings that are off the screen
            # if self.settings[len(self.settings) - 1].rect.top > Display.origHeight:
            #     Display.writeCenter(Display.screen, 'v')

    def drawBackButton(self):
        """ Draw the button that allows the user to return to the main menu """
        color = BLUE if self.backButton.collidepoint(pygame.mouse.get_pos()) else WORDS_COLOR
        backImg = pygame.font.SysFont('Comic Sans MS', self.data[FONT_SIZE_NAME] * 2).render("<- BACK", True, color).convert_alpha()
        self.backButton = pygame.Rect(50, 50, backImg.get_width(), backImg.get_height())
        Display.screen.blit(backImg, self.backButton.topleft)

    def handleEvents(self):
        """ Handle user input """
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if event.button == 4:
                    self.scrollUp()
                elif event.button == 5:
                    self.scrollDown()
                elif event.button == 6:
                    self.scrollUp(3)
                elif event.button == 7:
                    self.scrollDown(3)
                elif event.button == 1:
                    return self.mouseButtonPressed(pygame.mouse.get_pos())
            elif event.type == MOUSEMOTION:
                self.updateCursor()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return False
            if event.type == QUIT:
                pygame.quit()
                raise GameOver("Exiting")
        return True

    def mouseButtonPressed(self, pos):
        """ What to do when the mouse button has been clicked """
        for category in self.categories:
            if category.rect.collidepoint(pos):
                category.isVisible = not category.isVisible
        if self.backButton.collidepoint(pos):
            if self.worldSettings.shouldDrawWorld:
                self.worldSettings.shouldDrawWorld = False
                return True
            else:
                return False
        if not self.worldSettings.shouldDrawWorld:
            if self.worldSettings.showWorldButton.collidepoint(pos):
                self.worldSettings.shouldDrawWorld = not self.worldSettings.shouldDrawWorld
                return True
            for setting in self.settings:
                if setting.rect.collidepoint(pos) and self.categories[setting.categoryIndex].isVisible:
                    value = setting.getUserInput()
                    self.write(setting.key, value)
                    self.setDataUsingConfig()
                    setting.updateRect()
                    break
        return True

    def updateCursor(self):
        """ Change the style of the mouse """
        cursorStyle = pygame.SYSTEM_CURSOR_HAND if self.collidesWithSelectable(pygame.mouse.get_pos()) \
            else pygame.SYSTEM_CURSOR_ARROW
        pygame.mouse.set_cursor(cursorStyle)

    def collidesWithSelectable(self, pos):
        """ Returns whether the position is overlapping with something that can be selected """
        if self.backButton.collidepoint(pos):
            return True
        if not self.worldSettings.shouldDrawWorld:
            if self.worldSettings.showWorldButton.collidepoint(pos):
                return True
            for setting in self.settings:
                if setting.rect.collidepoint(pos):
                    return True
        return False

    def scrollUp(self, times=1):
        self.settingsY += 10 * times
        for category in self.categories:
            category.rect.top += 10 * times
            category.top += 10 * times
        for setting in self.settings:
            setting.rect.top += 10 * times
            setting.top += 10 * times

    def scrollDown(self, times=1):
        self.settingsY -= 10 * times
        for category in self.categories:
            category.rect.top -= 10 * times
            category.top -= 10 * times
        for setting in self.settings:
            setting.rect.top -= 10 * times
            setting.top -= 10 * times

    def write(self, key, value):
        self.data[key] = value
        with open(CONFIG_FILE_NAME, 'w') as file:
            json.dump(self.data, file)
