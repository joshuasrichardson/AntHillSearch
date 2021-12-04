import json
import math

import pygame
from pygame import MOUSEBUTTONUP, QUIT, MOUSEMOTION, KEYDOWN, K_RETURN, K_BACKSPACE, MOUSEBUTTONDOWN, K_ESCAPE

from ColonyExceptions import GameOver
from display import Display, SiteDisplay, AgentDisplay, PredatorDisplay
from Constants import *
from display.mainmenu.ArrayStateMachine import ArrayStateMachine
from model.builder.SiteBuilder import getNewSite


class Settings:
    """ A tab accessible from the main menu that allows the user to change certain settings for the simulation.
    Not all settings are able to be changed here. See Constants.py for more settings. """

    def __init__(self):
        # A list of values that can be updated by the user
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
                       ["Record All", RECORD_ALL],
                       ["Default Site Radius", SITE_RADIUS],
                       ["Site No Closer Than", SITE_NO_CLOSER_THAN],
                       ["Site No Farther Than", SITE_NO_FARTHER_THAN],
                       ["Agent Image", AGENT_IMAGE],
                       ["Max Search Distance", MAX_SEARCH_DIST],
                       ["Number of Predators", NUM_PREDATORS],
                       ["Predators' Positions", PRED_POSITIONS]]
        # The rectangles that make values selectable
        self.valueRects = [pygame.Rect(0, 0, 0, 0) for _ in range(len(self.values))]
        self.backButton = pygame.Rect(0, 0, 0, 0)  # Button to go back to the main menu

        self.userInputValue = 0  # The value of the user's input
        self.userInput = ''  # A string representation of the user's input
        self.data = {}  # The data about the settings to be recorded to settings.json
        self.setValuesWithJson()  # Set the values on the screen to match the values in settings.json
        self.arrayStates = None  # Used for handling input that should be arrays
        self.selectedRect = None  # The rectangle that has most recently been selected

    def setValuesWithJson(self):
        """ Set the values on the screen to match the values in settings.json """
        try:
            with open('display/mainmenu/settings.json', 'r') as file:
                self.data = json.load(file)
            for i, key in enumerate(SETTING_KEYS):
                if key in self.data:
                    self.values[i][1] = self.data[key]
        except FileNotFoundError:
            print("File 'mainmenu/settings.json' Not Found")
        except json.decoder.JSONDecodeError:
            print("File 'mainmenu/settings.json' is empty")

    def run(self):
        reading = True
        while reading:  # While the user is reading the settings (or hasn't tried to exit)
            Display.screen.fill(SCREEN_COLOR)  # Fill in the background
            Display.writeCenterPlus(Display.screen, "Settings", self.values[3][1], -6 * self.values[3][1])
            self.showSettings()  # Draw the setting the user can select and change
            self.drawBackButton()  # Draw the button used to return to the main menu
            pygame.display.flip()  # Display drawn things on the screen
            reading = self.handleEvents()  # Handle user input and stop reading if they chose the back button or exit

    def showSettings(self):
        """ Write each value on the screen """
        x = 200
        for i, value in enumerate(self.values):
            self.valueRects[i] = Display.write(Display.screen, value[0] + ": " + str(value[1]),
                                               int(self.values[2][1] * 1.5), x, 100 + i * self.values[2][1] * 2.3)
            if self.valueRects[i].collidepoint(pygame.mouse.get_pos()):
                Display.write(Display.screen, value[0] + ": " + str(value[1]),
                              int(self.values[2][1] * 1.5), x, 100 + i * self.values[2][1] * 2.3, SEARCH_COLOR)

    def drawBackButton(self):
        """ Draw the button that allows the user to return to the main menu """
        backImg = pygame.font.SysFont('Comic Sans MS', self.values[2][1] * 2).render("<- BACK", True, WORDS_COLOR).convert_alpha()
        self.backButton = pygame.Rect(50, 50, backImg.get_width(), backImg.get_height())
        if self.backButton.collidepoint(pygame.mouse.get_pos()):
            backImg = pygame.font.SysFont('Comic Sans MS', self.values[2][1] * 2).render("<- BACK", True, SEARCH_COLOR).convert_alpha()
        Display.screen.blit(backImg, self.backButton.topleft)

    def handleEvents(self):
        """ Handle user input """
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
        """ What to do when the mouse button has been clicked """
        if self.backButton.collidepoint(pos):
            return False
        for i, rect in enumerate(self.valueRects):
            if rect.collidepoint(pos):
                self.selectedRect = rect
                self.changeValue(self.values[i][0])
                break
        return True

    def setMouse(self):
        """ Change the style of the mouse """
        if self.collidesWithSelectable(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def collidesWithSelectable(self, pos):
        """ Returns whether the position is overlapping with something that can be selected """
        if self.backButton.collidepoint(pos):
            return True
        for rect in self.valueRects:
            if rect.collidepoint(pos):
                return True
        return False

    def changeValue(self, value):
        if value == "Convergence Fraction":
            self.values[0][1] = self.getUserInputPercent(self.values[0][1], self.valueRects[0].topright)
            self.write('convergenceFraction', self.values[0][1])
        elif value == "Simulation Duration":
            self.values[1][1] = self.getUserInputInt(self.values[1][1], self.valueRects[1].topright)
            if self.values[1][1] > MAX_TIME:
                self.values[1][1] = MAX_TIME
            if self.values[1][1] < 0:
                self.values[1][1] = 0
            self.write('simDuration', self.values[1][1])
        elif value == "Font Size":
            self.values[2][1] = self.getUserInputInt(self.values[2][1], self.valueRects[2].topright)
            if self.values[2][1] > 50:
                self.values[2][1] = 50
            if self.values[2][1] < 5:
                self.values[2][1] = 5
            self.write('fontSize', self.values[2][1])
        elif value == "Large Font Size":
            self.values[3][1] = self.getUserInputInt(self.values[3][1], self.valueRects[3].topright)
            if self.values[3][1] > 100:
                self.values[3][1] = 100
            if self.values[3][1] < 10:
                self.values[3][1] = 10
            self.write('largeFontSize', self.values[3][1])
        elif value == "Number of Hubs":
            self.values[4][1] = self.getUserInputInt(self.values[4][1], self.valueRects[4].topright)
            if self.values[4][1] > MAX_NUM_SITES / 6:
                self.values[4][1] = int(MAX_NUM_SITES / 6)
            if self.values[4][1] < 1:
                self.values[4][1] = 1
            self.write('numHubs', self.values[4][1])
        elif value == "Hub Locations":
            self.values[5][1] = self.getUserInputArray(self.values[5][1], self.valueRects[5].topright, 2)
            for hubLoc in self.values[5][1]:
                if hubLoc[0] > Display.origWidth + self.values[18][1]:
                    hubLoc[0] = Display.origWidth + self.values[18][1]
                if hubLoc[1] > Display.origHeight + self.values[18][1]:
                    hubLoc[1] = Display.origHeight + self.values[18][1]
            self.write('hubLocations', self.values[5][1])
        elif value == "Hub Radii":
            self.values[6][1] = self.getUserInputArray(self.values[6][1], self.valueRects[6].topright, 1)
            for i in range(len(self.values[6][1])):
                if self.values[6][1][i] > 100:
                    self.values[6][1][i] = 100
                if self.values[6][1][i] < 5:
                    self.values[6][1][i] = 5
            self.write('hubRadii', self.values[6][1])
        elif value == "Hub Agent Counts":
            self.values[7][1] = self.getUserInputArray(self.values[7][1], self.valueRects[7].topright, 1)
            for i in range(len(self.values[7][1])):
                if self.values[7][1][i] > 200:
                    self.values[7][1][i] = 200
                if self.values[7][1][i] < 0:
                    self.values[7][1][i] = 0
            self.write('hubAgentCounts', self.values[7][1])
        elif value == "Number of Sites":
            self.values[8][1] = self.getUserInputInt(self.values[8][1], self.valueRects[8].topright)
            if self.values[8][1] > MAX_NUM_SITES:
                self.values[8][1] = MAX_NUM_SITES
            if self.values[8][1] < 0:
                self.values[8][1] = 0
            self.write('numSites', self.values[8][1])
        elif value == "Site Positions":
            self.values[9][1] = self.getUserInputArray(self.values[9][1], self.valueRects[9].topright, 2)
            for pos in self.values[9][1]:
                if pos[0] > Display.origWidth + self.values[18][1]:
                    pos[0] = Display.origWidth + self.values[18][1]
                if pos[1] > Display.origHeight + self.values[18][1]:
                    pos[1] = Display.origHeight + self.values[18][1]
            self.write('sitePositions', self.values[9][1])
        elif value == "Site Qualities":
            self.values[10][1] = self.getUserInputArray(self.values[10][1], self.valueRects[10].topright, 1)
            for i in range(len(self.values[10][1])):
                if self.values[10][1][i] > 255:
                    self.values[10][1][i] = 255
                if self.values[10][1][i] < 0:
                    self.values[10][1][i] = 0
            self.write('siteQualities', self.values[10][1])
        elif value == "Site Radii":
            self.values[11][1] = self.getUserInputArray(self.values[11][1], self.valueRects[11].topright, 1)
            for i in range(len(self.values[11][1])):
                if self.values[11][1][i] > 100:
                    self.values[11][1][i] = 100
                if self.values[11][1][i] < 5:
                    self.values[11][1][i] = 5
            self.write('siteRadii', self.values[11][1])
        elif value == "Should Record":
            self.values[12][1] = self.getUserInputBool(self.values[12][1], self.valueRects[12].topright, str(not self.values[12][1]))
            self.write('shouldRecord', self.values[12][1])
        elif value == "Record All":
            self.values[13][1] = self.getUserInputBool(self.values[13][1], self.valueRects[13].topright, str(not self.values[13][1]))
            self.write("recordAll", self.values[13][1])
        elif value == "Default Site Radius":
            self.values[14][1] = self.getUserInputInt(self.values[14][1], self.valueRects[14].topright)
            if self.values[14][1] > 100:
                self.values[14][1] = 100
            if self.values[14][1] < 5:
                self.values[14][1] = 5
            self.write('siteRadius', self.values[14][1])
        elif value == "Site No Closer Than":
            self.values[15][1] = self.getUserInputInt(self.values[15][1], self.valueRects[15].topright)
            if self.values[15][1] >= self.values[16][1]:
                self.values[15][1] = self.values[16][1] - 10
            if self.values[15][1] < 0:
                self.values[15][1] = 0
            self.write('siteNoCloserThan', self.values[15][1])
        elif value == "Site No Farther Than":
            self.values[16][1] = self.getUserInputInt(self.values[16][1], self.valueRects[16].topright)
            if self.values[16][1] > self.values[18][1]:
                self.values[16][1] = self.values[18][1]
            if self.values[16][1] <= self.values[15][1]:
                self.values[16][1] = self.values[15][1] + 10
            self.write('siteNoFartherThan', self.values[16][1])
        elif value == "Agent Image":
            print(f"AgentImage: {self.values[17][1]}")
            if self.values[17][1] == "resources/copter.png":
                self.values[17][1] = self.getUserInputString(self.values[17][1], self.valueRects[17].topright, "resources/ant.png")
            else:
                self.values[17][1] = self.getUserInputString(self.values[17][1], self.valueRects[17].topright, "resources/copter.png")
            if self.values[17][1] != "resources/copter.png" and self.values[17][1] != "resources/ant.png":
                self.values[17][1] = "resources/ant.png"
            self.write('agentImage', self.values[17][1])
        elif value == "Max Search Distance":
            self.values[18][1] = self.getUserInputInt(self.values[18][1], self.valueRects[18].topright)
            if self.values[18][1] < 10:
                self.values[18][1] = 10
            if self.values[18][1] > 5000:
                self.values[18][1] = 5000
            self.write('maxSearchDist', self.values[18][1])
        elif value == "Number of Predators":
            self.values[19][1] = self.getUserInputInt(self.values[19][1], self.valueRects[19].topright)
            if self.values[19][1] > 15:
                self.values[19][1] = 15
            self.write("numPredators", self.values[19][1])
        elif value == "Predators' Positions":
            self.values[20][1] = self.getUserInputArray(self.values[20][1], self.valueRects[20].topright, 2)
            self.write("predPositions", self.values[20][1])
        self.setValuesWithJson()

    def write(self, key, value):
        self.data[key] = value
        with open('display/mainmenu/settings.json', 'w') as file:
            json.dump(self.data, file)

    def getUserInputInt(self, originalValue, pos):
        self.userInputValue = 0
        self.userInput = ' -> 0'
        return self.getUserInput(originalValue, pos, "int")

    def getUserInputPercent(self, originalValue, pos):
        self.userInputValue = 0.00
        self.userInput = ' -> 0%'
        return self.getUserInput(originalValue, pos, "percent")

    def getUserInputString(self, originalValue, pos, autofill):
        self.userInputValue = autofill
        self.userInput = ' -> ' + autofill
        return self.getUserInput(originalValue, pos, "string")

    def getUserInputArray(self, originalValue, pos, depth):
        self.userInputValue = []
        self.userInput = " -> "
        self.arrayStates = ArrayStateMachine(depth)
        return self.getUserInput(originalValue, pos, "array")

    def getUserInputBool(self, originalValue, pos, autofill):
        boolString = self.getUserInputString(originalValue, pos, autofill)
        return boolString == "True" or boolString == "T" or boolString == "true" or boolString == "t" or boolString == "1"

    def getUserInput(self, originalValue, pos, inputType):
        while 1:
            Display.screen.fill(SCREEN_COLOR)
            Display.writeCenterPlus(Display.screen, "Settings", self.values[3][1], -6 * self.values[3][1])
            self.showSettings()
            self.showUserInput(pos)
            self.showUserInputVisuals()
            self.drawBackButton()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_RETURN:
                    return self.userInputValue
                elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN and event.key == K_ESCAPE:
                    return originalValue
                elif event.type == MOUSEMOTION:
                    self.setMouse()
                elif inputType == "int":
                    if event.type == KEYDOWN and event.unicode.isnumeric():
                        self.appendNumber(int(event.unicode))
                    elif event.type == KEYDOWN and event.key == K_BACKSPACE:
                        self.deleteLastIntDigit()
                elif inputType == "string":
                    if event.type == KEYDOWN and event.key == K_BACKSPACE:
                        self.deleteLastLetter()
                    elif event.type == KEYDOWN:
                        self.appendLetter(event.unicode)
                elif inputType == "percent":
                    if event.type == KEYDOWN and event.key == K_BACKSPACE:
                        self.deleteLastPercentDigit()
                    elif event.type == KEYDOWN:
                        self.appendPercentageNumber(event.unicode)
                elif inputType == "array":
                    if event.type == KEYDOWN and event.key == K_BACKSPACE:
                        self.deleteLastArrayPart()
                    elif event.type == KEYDOWN:
                        self.appendArray(event.unicode)
                elif event.type == QUIT:
                    pygame.quit()
                    raise GameOver("Game Over")

    def appendNumber(self, number):
        if self.userInputValue == 0 or self.userInputValue > 250:
            self.userInputValue = number
        else:
            self.userInputValue *= 10
            self.userInputValue += number
        self.userInput = f' -> {self.userInputValue}'

    def appendPercentageNumber(self, number):
        try:
            if self.userInputValue == 0.00 or (self.userInputValue > 0.10 and number != 0):
                self.userInputValue = float(number) / 100.00
            else:
                self.userInputValue *= 10
                self.userInputValue = round(self.userInputValue + (float(number) / 100.00), 2)
            if self.userInputValue > 1.0:
                self.userInputValue = 1.00
        except ValueError:
            self.userInputValue = 0.00
        self.userInput = f' -> {int(self.userInputValue * 100)}%'

    def appendLetter(self, letter):
        if len(self.userInputValue) == 0 or len(self.userInputValue) > 100:
            self.userInputValue = letter
        else:
            self.userInputValue += letter
        self.userInput = f' -> {self.userInputValue}'

    def appendArray(self, value):
        self.userInput = self.arrayStates.state(value)
        if self.arrayStates.isComplete1:
            self.userInputValue = self.arrayStates.array
        elif self.arrayStates.isComplete2:
            self.userInputValue = self.arrayStates.array2D

    def arrayIsAtMaxDepth(self):
        numLayers = 0
        for i, c in enumerate(self.userInput):
            if c == '[':
                numLayers += 1
            elif c == ']':
                numLayers -= 1
            if numLayers >= 2:
                return True
        return False

    def deleteLastIntDigit(self):
        self.userInputValue = int(self.userInputValue / 10)
        if len(self.userInput) > 4:
            self.userInput = f' -> {self.userInput[4:len(self.userInput) - 1]}'

    def deleteLastPercentDigit(self):
        if self.userInputValue == 1.00:
            self.userInputValue = 0.00
        else:
            self.userInputValue = self.truncate(self.userInputValue, len(str(self.userInputValue)) - 3)
        self.userInput = f' -> {int(self.userInputValue * 100)}%'

    @staticmethod
    def truncate(n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier

    def deleteLastLetter(self):
        if len(self.userInputValue) > 0:
            self.userInputValue = self.userInputValue[0:len(self.userInputValue) - 1]
            self.userInput = f' -> {self.userInputValue}'

    def deleteLastArrayPart(self):
        self.userInput = self.arrayStates.back()

    def showUserInput(self, pos):
        Display.write(Display.screen, self.userInput, int(self.values[2][1] * 1.5), pos[0], pos[1], ASSESS_COLOR)

    def showUserInputVisuals(self):
        if self.selectedRect == self.valueRects[0]:  # Convergence Fraction
            self.drawConvergenceFraction(self.userInputValue)
        elif self.selectedRect == self.valueRects[1]:  # Simulation duration
            Display.write(Display.screen, self.userInputValue, int(self.values[2][1] * 1.5), Display.origWidth - 100, 50)
        elif self.selectedRect == self.valueRects[2]:  # Font size
            Display.writeCenter(Display.screen, "Simulation size", self.userInputValue)
            Display.writeCenterPlus(Display.screen, "Settings size", int(self.userInputValue * 1.5), int(self.userInputValue * 1.5))
        elif self.selectedRect == self.valueRects[3]:  # Large font size
            Display.writeCenter(Display.screen, "This size", self.userInputValue)
        elif self.selectedRect == self.valueRects[4]:  # Num hubs
            self.drawNumSites(-1)
        elif self.selectedRect == self.valueRects[5]:  # Hub Positions
            if self.arrayStates.isComplete2:
                # TODO: If the hubs are too close together, force them to be farther apart
                for pos in self.userInputValue:
                    self.drawSite(pos, self.values[14][1], -1)
            else:
                self.drawSites(self.values[5][1], -1)
        elif self.selectedRect == self.valueRects[6]:  # Hub Radii
            self.drawSitesRadii(-1)
        elif self.selectedRect == self.valueRects[7]:  # Hub Agent Counts
            self.drawSitesCounts(-1)
        elif self.selectedRect == self.valueRects[8]:  # Num sites
            self.drawNumSites(200)
        elif self.selectedRect == self.valueRects[9]:  # Site Positions
            if self.arrayStates.isComplete2:
                for pos in self.userInputValue:
                    self.drawSite(pos, self.values[14][1], 200)
            else:
                self.drawSites(self.values[9][1], 200)
        elif self.selectedRect == self.valueRects[10]:  # Site Qualities
            self.drawSitesQualities()
        elif self.selectedRect == self.valueRects[11]:  # Site Radii
            self.drawSitesRadii(200)
        elif self.selectedRect == self.valueRects[12]:  # Should Record
            if self.values[12][1]:
                Display.drawCircle(Display.screen, (220, 0, 0), [15, 15], 10, width=1, adjust=False)
                Display.drawLine(Display.screen, (220, 0, 0), [4, 24], [25, 5], adjust=False)
            else:
                Display.drawCircle(Display.screen, (220, 0, 0), [15, 15], 10, adjust=False)
        elif self.selectedRect == self.valueRects[14]:  # Default Site Radius
            self.drawSite([Display.origWidth / 2, Display.origHeight / 2], self.userInputValue, 200)
        elif self.selectedRect == self.valueRects[15]:  # Site No Farther Than
            self.drawArea(COMMIT_COLOR, self.values[16][1])
            self.drawArea(ASSESS_COLOR, self.userInputValue)
        elif self.selectedRect == self.valueRects[16]:  # Site No Closer Than
            self.drawArea(COMMIT_COLOR, self.userInputValue)
            self.drawArea(ASSESS_COLOR, self.values[15][1])
        elif self.selectedRect == self.valueRects[17]:  # Agent Image
            self.drawAgents()
        elif self.selectedRect == self.valueRects[18]:  # Max Search Distance
            self.drawArea(SEARCH_COLOR, self.userInputValue)
        elif self.selectedRect == self.valueRects[19]:  # Number of Predators
            self.drawPredators(self.userInputValue)
        # TODO: Predator's positions

    def drawConvergenceFraction(self, fraction):
        AgentDisplay.agentImage = self.values[17][1]
        image = AgentDisplay.getAgentImage([Display.origWidth / 2, Display.origHeight / 2])
        w = image.get_width() * 5
        h = image.get_height() * 20
        x = Display.origWidth / 2 - w / 2
        y = Display.origHeight / 2 - h / 2
        rect = (x, y, w, h)
        Display.drawRect(Display.screen, BORDER_COLOR, rect, 2, False)

        fraction = int(math.ceil(fraction * 100))
        j = 0
        d = h
        dif = h / 20
        for i in range(fraction):
            if j % 5 == 0:
                d -= dif
            Display.blitImage(Display.screen, image, [x + (dif * (i % 5)), y + d], False)
            j += 1
        for i in range(100 - fraction):
            if j % 5 == 0:
                d -= dif
            Display.blitImage(Display.screen, image, [2 * w + 10 + x - (dif * (i % 5)), y + d], False)
            j += 1

    @staticmethod
    def drawSite(pos, radius, quality, numAgents=0):
        potentialSite = getNewSite(1, pos[0], pos[1], radius, quality)
        potentialSite.wasFound = True
        potentialSite.agentCount = numAgents
        SiteDisplay.drawSite(potentialSite)
        del potentialSite

    def drawSites(self, positions, quality):
        for pos in positions:
            self.drawSite(pos, self.values[14][1], quality)

    def drawNumSites(self, quality):
        x = Display.origWidth / 2
        h = int((Display.origHeight - self.values[3][1] * 3) / (2 * (self.values[14][1] + 10)))  # The number of sites that can fit in a column
        for i in range(self.userInputValue):
            y = 2 * (i % h) * (self.values[14][1] + 10) + (self.values[3][1] * 3)
            if i % h == 0 and i > 0:
                x += 2 * (self.values[14][1] + 10)
            self.drawSite([x, y], self.values[14][1], quality)

    def drawSitesRadii(self, quality):
        x = Display.origWidth / 2
        h = int((Display.origHeight - self.values[3][1] * 3) / (2 * (self.values[14][1] + 10)))  # The number of sites that can fit in a column
        for i in range(len(self.userInputValue)):
            y = 2 * (i % h) * (self.values[14][1] + 10) + (self.values[3][1] * 3)
            if i % h == 0 and i > 0:
                x += 2 * (self.values[14][1] + 10)
            self.drawSite([x, y], self.userInputValue[i], quality)

    def drawSitesCounts(self, quality):
        x = Display.origWidth / 2
        h = int((Display.origHeight - self.values[3][1] * 3) / (2 * (self.values[14][1] + 10)))  # The number of sites that can fit in a column
        for i in range(len(self.userInputValue)):
            y = 2 * (i % h) * (self.values[14][1] + 10) + (self.values[3][1] * 3)
            if i % h == 0 and i > 0:
                x += 2 * (self.values[14][1] + 10)
            self.drawSite([x, y], self.values[14][1], quality, self.userInputValue[i])

    def drawSitesQualities(self):
        x = Display.origWidth / 2
        h = int((Display.origHeight - self.values[3][1] * 3) / (2 * (self.values[14][1] + 10)))  # The number of sites that can fit in a column
        for i in range(len(self.userInputValue)):
            y = 2 * (i % h) * (self.values[14][1] + 10) + (self.values[3][1] * 3)
            if i % h == 0 and i > 0:
                x += 2 * (self.values[14][1] + 10)
            self.drawSite([x, y], self.values[14][1], self.userInputValue[i])

    def drawAgents(self):  # TODO: Make images selectable
        for i, imgFile in enumerate(AGENT_IMAGES):
            pos = [Display.origWidth / 2 + i * 30, Display.origHeight / 2]
            AgentDisplay.agentImage = imgFile
            image = AgentDisplay.getAgentImage([Display.origWidth / 2, Display.origHeight / 2])
            if imgFile != self.values[17][1]:
                Display.drawDownArrow([pos[0] + image.get_width() / 2, pos[1]], BORDER_COLOR, False)
            Display.blitImage(Display.screen, image, pos, False)

    def drawArea(self, color, radius):
        fadedColor = (color[0], color[1], color[2], 80)
        surf = pygame.Surface((Display.origWidth, Display.origHeight), pygame.SRCALPHA)
        Display.drawCircle(surf, fadedColor, [Display.origWidth / 2, Display.origHeight / 2], radius)
        Display.blitImage(Display.screen, surf, (0, 0), False)
        self.drawSite([Display.origWidth / 2, Display.origHeight / 2], self.values[15][1], -1)

    @staticmethod
    def drawPredators(numPredators):
        for i in range(numPredators):
            pos = [Display.origWidth / 2 + i * 50, Display.origHeight / 2]
            image = PredatorDisplay.getPredatorImage([Display.origWidth / 2, Display.origHeight / 2])
            Display.blitImage(Display.screen, image, pos, False)
