import json

from pygame import MOUSEBUTTONUP, QUIT, MOUSEMOTION, KEYDOWN, K_ESCAPE

from ColonyExceptions import GameOver
from Constants import *
from display.mainmenu.settings.BooleanSetting import BooleanSetting
from display.mainmenu.settings.DrawingFunctions import *
from display.mainmenu.settings.IntegerSetting import IntegerSetting
from display.mainmenu.settings.ListSetting import ListSetting
from display.mainmenu.settings.PercentageSetting import PercentageSetting
from display.mainmenu.settings.PositionSetting import PositionSetting
from display.mainmenu.settings.StringSetting import StringSetting


class Settings:
    """ A tab accessible from the main menu that allows the user to change certain settings for the simulation.
    Not all settings are able to be changed here. See Constants.py for more settings. """

    def __init__(self):
        # The rectangles that make values selectable
        self.backButton = pygame.Rect(0, 0, 0, 0)  # Button to go back to the main menu
        self.data = {}  # The data about the settings to be recorded to settings.json
        self.setValuesWithJson()  # Set the values on the screen to match the values in settings.json

        x = 200
        self.y = 100
        self.settings = [PercentageSetting("convergenceFraction", "Convergence Fraction", x, self.nextY(), drawConvergenceFraction, self),
                         IntegerSetting("simDuration", "Simulation Duration", x, self.nextY(), showSimDuration, self),
                         IntegerSetting("fontSize", "Font Size", x, self.nextY(), showFontSize, self),
                         IntegerSetting("largeFontSize", "Large Font Size", x, self.nextY(), showLargeFontSize, self),
                         IntegerSetting("numHubs", "Number of Hubs", x, self.nextY(), drawNumHubs, self),
                         PositionSetting("hubLocations", "Hub Locations", x, self.nextY(), drawHubsPositions, self),
                         ListSetting("hubRadii", "Hub Radii", x, self.nextY(), drawHubsRadii, self),
                         ListSetting("hubAgentCounts", "Hub Agent Counts", x, self.nextY(), drawHubsCounts, self),
                         IntegerSetting("numSites", "Number of Sites", x, self.nextY(), drawNumSites, self),
                         PositionSetting("sitePositions", "Site Positions", x, self.nextY(), drawSitesPositions, self),
                         ListSetting("siteRadii", "Site Radii", x, self.nextY(), drawSitesRadii, self),
                         ListSetting("siteQualities", "Site Qualities", x, self.nextY(), drawSitesQualities, self),
                         BooleanSetting("shouldRecord", "Should Record", x, self.nextY(), drawShouldRecord, self),
                         BooleanSetting("recordAll", "Record All", x, self.nextY(), drawShouldRecord, self),
                         IntegerSetting("siteRadius", "Default Site Radius", x, self.nextY(), drawSiteRadius, self),
                         IntegerSetting("siteNoCloserThan", "Site No Closer Than", x, self.nextY(), drawNoCloserThan, self),
                         IntegerSetting("siteNoFartherThan", "Site No Farther Than", x, self.nextY(), drawNoFartherThan, self),
                         IntegerSetting("maxSearchDist", "Max Search Distance", x, self.nextY(), drawSearchArea, self),
                         StringSetting("agentImage", "Agent Image", x, self.nextY(), drawAgents, self, getOtherFile),
                         IntegerSetting("numPredators", "Number of Predators", x, self.nextY(), drawPredators, self),
                         PositionSetting("predPositions", "Predator Positions", x, self.nextY(), drawPredPositions, self),
                         IntegerSetting("numLadybugs", "Number of Ladybugs", x, self.nextY(), drawLadybugs, self),
                         PositionSetting("ladybugPositions", "Ladybug Positions", x, self.nextY(), drawLadybugPositions, self)]

    def nextY(self):
        y = self.y
        self.y += 25
        return y

    def setValuesWithJson(self):
        """ Set the values on the screen to match the values in settings.json """
        try:
            with open(SETTINGS_FILE_NAME, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print(f"File '{SETTINGS_FILE_NAME}' was not found")
        except json.decoder.JSONDecodeError:
            print(f"File '{SETTINGS_FILE_NAME}' is empty")

    def run(self):
        reading = True
        while reading:  # While the user is reading the settings (or hasn't tried to exit)
            Display.screen.fill(SCREEN_COLOR)  # Fill in the background
            Display.writeCenterPlus(Display.screen, "Settings", self.data["largeFontSize"], -6 * self.data["largeFontSize"])
            self.showSettings()  # Draw the setting the user can select and change
            self.drawBackButton()  # Draw the button used to return to the main menu
            pygame.display.flip()  # Display drawn things on the screen
            reading = self.handleEvents()  # Handle user input and stop reading if they chose the back button or exit

    def showSettings(self):
        """ Write each value on the screen """
        for setting in self.settings:
            collides = setting.rect.collidepoint(pygame.mouse.get_pos())
            Display.write(Display.screen, f"{setting.name}: {setting.savedValue}", int(self.data['fontSize'] * 1.5),
                          setting.rect.left, setting.rect.top, SEARCH_COLOR if collides else WORDS_COLOR)

    def drawBackButton(self):
        """ Draw the button that allows the user to return to the main menu """
        color = SEARCH_COLOR if self.backButton.collidepoint(pygame.mouse.get_pos()) else WORDS_COLOR
        backImg = pygame.font.SysFont('Comic Sans MS', self.data["fontSize"] * 2).render("<- BACK", True, color).convert_alpha()
        self.backButton = pygame.Rect(50, 50, backImg.get_width(), backImg.get_height())
        Display.screen.blit(backImg, self.backButton.topleft)

    def handleEvents(self):
        """ Handle user input """
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                return self.mouseButtonPressed(pygame.mouse.get_pos())
            elif event.type == MOUSEMOTION:
                self.updateCursor()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return False
            if event.type == QUIT:
                pygame.quit()
                raise GameOver("Game Over")
        return True

    def mouseButtonPressed(self, pos):
        """ What to do when the mouse button has been clicked """
        if self.backButton.collidepoint(pos):
            return False
        for setting in self.settings:
            if setting.rect.collidepoint(pos):
                value = setting.getUserInput()
                self.write(setting.key, value)
                self.setValuesWithJson()
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
        for setting in self.settings:
            if setting.rect.collidepoint(pos):
                return True
        return False

    def write(self, key, value):
        self.data[key] = value
        with open(SETTINGS_FILE_NAME, 'w') as file:
            json.dump(self.data, file)
