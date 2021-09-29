import json

import pygame
from pygame import MOUSEBUTTONUP, QUIT, MOUSEMOTION, KEYDOWN, K_RETURN, K_BACKSPACE, MOUSEBUTTONDOWN, K_ESCAPE

from ColonyExceptions import GameOver
from display import Display
from Constants import *
from display.mainmenu.ArrayStateMachine import ArrayStateMachine


class Settings:

    def __init__(self):
        self.convergenceFraction = CONVERGENCE_FRACTION
        self.simDuration = SIM_DURATION
        self.fontSize = FONT_SIZE
        self.largeFontSize = LARGE_FONT_SIZE
        self.numHubs = NUM_HUBS
        self.hubLocations = HUB_LOCATIONS
        self.hubRadii = HUB_RADII
        self.hubAgentCounts = HUB_AGENT_COUNTS
        self.numSites = NUM_SITES
        self.sitePositions = SITE_POSITIONS
        self.siteQualities = SITE_QUALITIES
        self.siteRadii = SITE_RADII
        self.shouldRecord = SHOULD_RECORD
        self.siteRadius = SITE_RADIUS
        self.siteNoCloserThan = SITE_NO_CLOSER_THAN
        self.siteNoFartherThan = SITE_NO_FARTHER_THAN
        self.agentImage = AGENT_IMAGE
        self.maxSearchDist = MAX_SEARCH_DIST

        self.values = [["Convergence Fraction", self.convergenceFraction],
                       ["Simulation Duration", self.simDuration],
                       ["Font Size", self.fontSize],
                       ["Large Font Size", self.largeFontSize],
                       ["Number of Hubs", self.numHubs],
                       ["Hub Locations", self.hubLocations],
                       ["Hub Radii", self.hubRadii],
                       ["Hub Agent Counts", self.hubAgentCounts],
                       ["Number of Sites", self.numSites],
                       ["Site Positions", self.sitePositions],
                       ["Site Qualities", self.siteQualities],
                       ["Site Radii", self.siteRadii],
                       ["Should Record", self.shouldRecord],
                       ["Default Site Radius", self.siteRadius],
                       ["Site No Closer Than", self.siteNoCloserThan],
                       ["Site No Farther Than", self.siteNoFartherThan],
                       ["Agent Image", self.agentImage],
                       ["Max Search Distance", self.maxSearchDist]]
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

        self.userInputValue = 0
        self.userInput = ''
        self.data = {}
        self.setValuesWithJson()
        self.arrayStates = None

    def setValuesWithJson(self):
        try:
            with open('display/mainmenu/settings.json', 'r') as file:
                self.data = json.load(file)
            if 'convergenceFraction' in self.data:
                self.convergenceFraction = self.data['convergenceFraction']
                self.values[0][1] = self.convergenceFraction
            if 'simDuration' in self.data:
                self.simDuration = self.data['simDuration']
                self.values[1][1] = self.simDuration
            if 'fontSize' in self.data:
                self.fontSize = self.data['fontSize']
                self.values[2][1] = self.fontSize
            if 'largeFontSize' in self.data:
                self.largeFontSize = self.data['largeFontSize']
                self.values[3][1] = self.largeFontSize
            if 'numHubs' in self.data:
                self.numHubs = self.data['numHubs']
                self.values[4][1] = self.numHubs
            if 'hubLocations' in self.data:
                self.hubLocations = self.data['hubLocations']
                self.values[5][1] = self.hubLocations
            if 'hubRadii' in self.data:
                self.hubRadii = self.data['hubRadii']
                self.values[6][1] = self.hubRadii
            if 'hubAgentCounts' in self.data:
                self.hubAgentCounts = self.data['hubAgentCounts']
                self.values[7][1] = self.hubAgentCounts
            if 'numSites' in self.data:
                self.numSites = self.data['numSites']
                self.values[8][1] = self.numSites
            if 'sitePositions' in self.data:
                self.sitePositions = self.data['sitePositions']
                self.values[9][1] = self.sitePositions
            if 'siteQualities' in self.data:
                self.siteQualities = self.data['siteQualities']
                self.values[10][1] = self.siteQualities
            if 'siteRadii' in self.data:
                self.siteRadii = self.data['siteRadii']
                self.values[11][1] = self.siteRadii
            if 'shouldRecord' in self.data:
                self.shouldRecord = self.data['shouldRecord']
                self.values[12][1] = self.shouldRecord
            if 'siteRadius' in self.data:
                self.siteRadius = self.data['siteRadius']
                self.values[13][1] = self.siteRadius
            if 'siteNoCloserThan' in self.data:
                self.siteNoCloserThan = self.data['siteNoCloserThan']
                self.values[14][1] = self.siteNoCloserThan
            if 'siteNoFartherThan' in self.data:
                self.siteNoFartherThan = self.data['siteNoFartherThan']
                self.values[15][1] = self.siteNoFartherThan
            if 'agentImage' in self.data:
                self.agentImage = self.data['agentImage']
                self.values[16][1] = self.agentImage
            if 'maxSearchDist' in self.data:
                self.maxSearchDist = self.data['maxSearchDist']
                self.values[17][1] = self.maxSearchDist
        except FileNotFoundError:
            print("File 'mainmenu/settings.json' Not Found")
        except json.decoder.JSONDecodeError:
            print("File 'mainmenu/settings.json' is empty")

    def run(self):
        try:
            reading = True
            while reading:
                Display.screen.fill(SCREEN_COLOR)
                Display.writeCenterPlus(Display.screen, "Settings", self.largeFontSize, -6 * self.largeFontSize)
                self.showSettings()
                self.drawBackButton()
                pygame.display.flip()
                reading = self.handleEvents()
        except GameOver:
            pass

    def showSettings(self):
        x = 200
        for i, value in enumerate(self.values):
            self.valueRects[i] = Display.write(Display.screen, value[0] + ": " + str(value[1]), int(self.fontSize * 1.5), x, 100 + i * self.fontSize * 2.3)

    def drawBackButton(self):
        backImg = pygame.font.SysFont('Comic Sans MS', self.fontSize * 2).render("<- BACK", True, WORDS_COLOR).convert_alpha()
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
        for i, rect in enumerate(self.valueRects):
            if rect.collidepoint(pos):
                self.changeValue(self.values[i][0])
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

    def changeValue(self, value):
        if value == "Convergence Fraction":
            self.convergenceFraction = self.getUserInputPercent(self.convergenceFraction, self.valueRects[0].topright)
            self.write('convergenceFraction', self.convergenceFraction)
        elif value == "Simulation Duration":
            self.simDuration = self.getUserInputInt(self.simDuration, self.valueRects[1].topright)
            if self.simDuration > MAX_TIME:
                self.simDuration = MAX_TIME
            if self.simDuration < 0:
                self.simDuration = 0
            self.write('simDuration', self.simDuration)
        elif value == "Font Size":
            self.fontSize = self.getUserInputInt(self.fontSize, self.valueRects[2].topright)
            if self.fontSize > 50:
                self.fontSize = 50
            if self.fontSize < 5:
                self.fontSize = 5
            self.write('fontSize', self.fontSize)
        elif value == "Large Font Size":
            self.largeFontSize = self.getUserInputInt(self.largeFontSize, self.valueRects[3].topright)
            if self.largeFontSize > 100:
                self.largeFontSize = 100
            if self.largeFontSize < 10:
                self.largeFontSize = 10
            self.write('largeFontSize', self.largeFontSize)
        elif value == "Number of Hubs":
            self.numHubs = self.getUserInputInt(self.numHubs, self.valueRects[4].topright)
            if self.numHubs > MAX_NUM_SITES / 6:
                self.numHubs = int(MAX_NUM_SITES / 6)
            if self.numHubs < 1:
                self.numHubs = 1
            self.write('numHubs', self.numHubs)
        elif value == "Hub Locations":
            self.hubLocations = self.getUserInputArray(self.hubLocations, self.valueRects[5].topright, 2)
            # TODO: Limited it to be within the screen
            self.write('hubLocations', self.hubLocations)
        elif value == "Hub Radii":
            self.hubRadii = self.getUserInputArray(self.hubRadii, self.valueRects[6].topright, 1)
            for i in range(len(self.hubRadii)):
                if self.hubRadii[i] > 100:
                    self.hubRadii[i] = 100
                if self.hubRadii[i] < 5:
                    self.hubRadii[i] = 5
            self.write('hubRadii', self.hubRadii)
        elif value == "Hub Agent Counts":
            self.hubAgentCounts = self.getUserInputArray(self.hubAgentCounts, self.valueRects[7].topright, 1)
            for i in range(len(self.hubAgentCounts)):
                if self.hubAgentCounts[i] > 200:
                    self.hubAgentCounts[i] = 200
                if self.hubAgentCounts[i] < 0:
                    self.hubAgentCounts[i] = 0
            self.write('hubAgentCounts', self.hubAgentCounts)
        elif value == "Number of Sites":
            self.numSites = self.getUserInputInt(self.numSites, self.valueRects[8].topright)
            if self.numSites > MAX_NUM_SITES:
                self.numSites = MAX_NUM_SITES
            if self.numSites < 0:
                self.numSites= 0
            self.write('numSites', self.numSites)
        elif value == "Site Positions":
            # TODO
            self.sitePositions = self.getUserInputArray(self.sitePositions, self.valueRects[9].topright, 2)
            self.write('sitePositions', self.sitePositions)
        elif value == "Site Qualities":
            self.siteQualities = self.getUserInputArray(self.siteQualities, self.valueRects[10].topright, 1)
            for i in range(len(self.siteQualities)):
                if self.siteQualities[i] > 255:
                    self.siteQualities[i] = 255
                if self.siteQualities[i] < 0:
                    self.siteQualities[i] = 0
            self.write('siteQualities', self.siteQualities)
        elif value == "Site Radii":
            self.siteRadii = self.getUserInputArray(self.siteRadii, self.valueRects[11].topright, 1)
            for i in range(len(self.siteRadii)):
                if self.siteRadii[i] > 100:
                    self.siteRadii[i] = 100
                if self.siteRadii[i] < 5:
                    self.siteRadii[i] = 5
            self.write('siteRadii', self.siteRadii)
        elif value == "Should Record":
            self.shouldRecord = self.getUserInputBool(self.shouldRecord, self.valueRects[12].topright, str(not self.shouldRecord))
            self.write('shouldRecord', self.shouldRecord)
        elif value == "Default Site Radius":
            self.siteRadius = self.getUserInputInt(self.siteRadius, self.valueRects[13].topright)
            if self.siteRadius > 100:
                self.siteRadius = 100
            if self.siteRadius < 5:
                self.siteRadius = 5
            self.write('siteRadius', self.siteRadius)
        elif value == "Site No Closer Than":
            self.siteNoCloserThan = self.getUserInputInt(self.siteNoCloserThan, self.valueRects[14].topright)
            if self.siteNoCloserThan >= self.siteNoFartherThan:
                self.siteNoCloserThan = self.siteNoFartherThan - 10
            if self.siteNoCloserThan < 0:
                self.siteNoCloserThan = 0
            self.write('siteNoCloserThan', self.siteNoCloserThan)
        elif value == "Site No Farther Than":
            self.siteNoFartherThan = self.getUserInputInt(self.siteNoFartherThan, self.valueRects[15].topright)
            if self.siteNoFartherThan > self.maxSearchDist:
                self.siteNoFartherThan = self.maxSearchDist
            if self.siteNoFartherThan <= self.siteNoCloserThan:
                self.siteNoFartherThan = self.siteNoCloserThan + 10
            self.write('siteNoFartherThan', self.siteNoFartherThan)
        elif value == "Agent Image":
            if self.agentImage == "resources/copter.png":
                self.agentImage = self.getUserInputString(self.agentImage, self.valueRects[16].topright, "resources/ant.png")
            else:
                self.agentImage = self.getUserInputString(self.agentImage, self.valueRects[16].topright, "resources/copter.png")
            if self.agentImage != "resources/copter.png" and self.agentImage != "resources/ant.png":
                self.agentImage = "resources/ant.png"
            self.write('agentImage', self.agentImage)
        elif value == "Max Search Distance":
            self.maxSearchDist = self.getUserInputInt(self.maxSearchDist, self.valueRects[17].topright)
            if self.maxSearchDist < 10:
                self.maxSearchDist = 10
            if self.maxSearchDist > 5000:
                self.maxSearchDist = 5000
            self.write('maxSearchDist', self.maxSearchDist)
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
            Display.writeCenterPlus(Display.screen, "Settings", self.largeFontSize, -6 * self.largeFontSize)
            self.showSettings()
            self.showUserInput(pos)
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
        if self.userInputValue == 0 or self.userInputValue > 2000:
            self.userInputValue = number
        else:
            self.userInputValue *= 10
            self.userInputValue += number
        self.userInput = ' -> ' + str(self.userInputValue)

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
        self.userInput = ' -> ' + str(int(self.userInputValue * 100)) + "%"

    def appendLetter(self, letter):
        if len(self.userInputValue) == 0 or len(self.userInputValue) > 100:
            self.userInputValue = letter
        else:
            self.userInputValue += letter
        self.userInput = ' -> ' + self.userInputValue

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
            self.userInput = ' -> ' + self.userInput[4:len(self.userInput) - 1]

    def deleteLastPercentDigit(self):
        if self.userInputValue == 1.00:
            self.userInputValue = 0.00
        else:
            self.userInputValue = self.truncate(self.userInputValue, len(str(self.userInputValue)) - 3)
        self.userInput = ' -> ' + str(int(self.userInputValue * 100)) + "%"

    @staticmethod
    def truncate(n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier

    def deleteLastLetter(self):
        if len(self.userInputValue) > 0:
            self.userInputValue = self.userInputValue[0:len(self.userInputValue) - 1]
            self.userInput = ' -> ' + str(self.userInputValue)

    def deleteLastArrayPart(self):
        self.userInput = self.arrayStates.back()

    def showUserInput(self, pos):
        Display.write(Display.screen, self.userInput, int(self.fontSize * 1.5), pos[0], pos[1], ASSESS_COLOR)
