import pygame
from pygame import KEYDOWN, K_RETURN, MOUSEBUTTONDOWN, MOUSEMOTION, K_ESCAPE, QUIT, K_BACKSPACE

from ColonyExceptions import GameOver
from Constants import SCREEN_COLOR, RED, FONT_SIZE_NAME
from display import Display


class Setting:
    """ An option that can be changed in the settings tab """

    def __init__(self, key, name, x, y, showUserInputVisuals, settingMenu):
        self.settingMenu = settingMenu  # The settings menu that this setting belongs to
        self.key = key  # A key to help read and write the data from json
        self.name = name  # A name for the setting that may include spaces
        self.value = self.settingMenu.data[key]  # The potential value of the setting to be used in the simulation if saved
        self.savedValue = self.value  # The value that will be used in the simulation
        self.rect = Display.write(Display.screen, f"{self.name}: {self.value}",
                                  int(self.settingMenu.data[FONT_SIZE_NAME] * 1.5), x, y)  # The rect that lets users select the setting
        self.showUserInputVisuals = showUserInputVisuals  # The method to draw the user input on the screen
        self.userInputString = f" -> {self.value}"  # The string representation of the value provided by the user

    def getUserInput(self):
        self.initUserInput()
        while 1:
            Display.screen.fill(SCREEN_COLOR)
            self.settingMenu.showSettings()
            self.showUserInput()
            self.showUserInputVisuals(self)
            self.settingMenu.drawBackButton()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_RETURN:
                    self.savedValue = self.value
                    return self.value
                elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.value = self.savedValue
                    return self.savedValue
                elif event.type == MOUSEMOTION:
                    self.settingMenu.updateCursor()
                elif event.type == KEYDOWN and event.key == K_BACKSPACE:
                    self.backspace()
                elif event.type == KEYDOWN:
                    self.appendUserInput(event.unicode)
                elif event.type == QUIT:
                    pygame.quit()
                    raise GameOver("Exiting")

    def showUserInput(self):
        pos = self.rect.topright
        Display.write(Display.screen, self.userInputString, int(self.settingMenu.data[FONT_SIZE_NAME] * 1.5),
                      pos[0], pos[1], RED)

    def updateRect(self):
        self.rect = Display.write(Display.screen, f"{self.name}: {self.value}",
                                  int(self.settingMenu.data[FONT_SIZE_NAME] * 1.5), self.rect.left, self.rect.top)

    def initUserInput(self):
        pass

    def backspace(self):
        pass

    def appendUserInput(self, userInput):
        pass
