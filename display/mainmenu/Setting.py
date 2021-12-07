import pygame
from pygame import KEYDOWN, K_RETURN, MOUSEBUTTONDOWN, MOUSEMOTION, K_ESCAPE, QUIT, K_BACKSPACE

from ColonyExceptions import GameOver
from Constants import SCREEN_COLOR, ASSESS_COLOR
from display import Display


class Setting:

    def __init__(self, key, name, value, rect, showUserInputVisuals, settingMenu):
        self.key = key  # A key to help read and write the data from json
        self.name = name  # A name for the setting that may include spaces
        self.value = value  # The value of the setting to be used in the simulation
        self.rect = rect  # The pygame rect that lets users select the setting
        self.showUserInputVisuals = showUserInputVisuals  # The method to draw the user input on the screen
        self.userInputValue = 0.00  # A value provided by the user
        self.userInputString = ''  # The string representation of the value provided by the user
        self.settingMenu = settingMenu

    def getUserInput(self, originalValue, pos):
        self.initUserInput()
        while 1:
            Display.screen.fill(SCREEN_COLOR)
            Display.writeCenterPlus(Display.screen, "Settings", self.settingMenu.data['largeFontSize'],
                                    -6 * self.settingMenu.data['largeFontSize'])
            self.settingMenu.showSettings()
            self.showUserInput(pos)
            self.showUserInputVisuals(self.userInputValue)  # todo: Might not work for all. We also might be able to remove the parameter
            self.settingMenu.drawBackButton()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_RETURN:
                    self.value = self.userInputValue
                    return self.userInputValue
                elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN and event.key == K_ESCAPE:
                    return originalValue
                elif event.type == MOUSEMOTION:
                    self.settingMenu.setMouse()
                elif event.type == KEYDOWN and event.key == K_BACKSPACE:
                    self.backspace()
                elif event.type == KEYDOWN:
                    self.appendUserInput(event.unicode)
                elif event.type == QUIT:
                    pygame.quit()
                    raise GameOver("Game Over")

    def showUserInput(self, pos):
        Display.write(Display.screen, self.userInputString, int(self.settingMenu.data['fontSize'] * 1.5),
                      pos[0], pos[1], ASSESS_COLOR)

    def initUserInput(self):
        pass

    def backspace(self):
        pass

    def appendUserInput(self, userInput):
        pass
