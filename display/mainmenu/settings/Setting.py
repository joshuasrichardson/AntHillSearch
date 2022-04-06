from pygame import KEYDOWN, K_RETURN, K_BACKSPACE

from Constants import RED
from config import Config
from display import Display
from display.mainmenu.MenuScreen import MenuScreen
from display.mainmenu.buttons.BackButton import BackButton
from display.mainmenu.buttons.SelectorButton import SelectorButton


class Setting(SelectorButton, MenuScreen):
    """ An option that can be changed in the settings tab """

    def __init__(self, key, name, x, y, showUserInputVisuals, settingMenu):
        self.settingMenu = settingMenu  # The settings menu that this setting belongs to
        self.key = key  # A key to help read and write the data from json
        self.name = name  # A name for the setting that may include spaces
        self.value = self.settingMenu.data[key]  # The potential value of the setting to be used in the simulation if saved
        self.savedValue = self.value  # The value that will be used in the simulation
        self.showUserInputVisuals = showUserInputVisuals  # The method to draw the user input on the screen
        self.userInputString = f" -> {self.value}"  # The string representation of the value provided by the user
        self.shouldDraw = True
        super().__init__(name, self.value, x, y, self, self.getUserInput)
        self.buttons = [BackButton()]

    def draw(self):
        if self.shouldDraw:
            self.rect = Display.write(Display.screen, f"{self.name}: {self.savedValue}", int(Config.FONT_SIZE * 1.5),
                                      self.rect.left, self.rect.top, self.color)

    def collides(self, pos):
        return self.shouldDraw and super().collides(pos)

    def handleEvent(self, event):
        super().handleEvent(event)
        if event.type == KEYDOWN and event.key == K_RETURN:
            self.saveValue()
        elif event.type == KEYDOWN and event.key == K_BACKSPACE:
            self.backspace()
        elif event.type == KEYDOWN:
            self.appendUserInput(event.unicode)

    def saveValue(self):
        self.savedValue = self.value
        self.settingMenu.save(self.key, self.savedValue)
        self.escape()

    def displayScreen(self):
        super().displayScreen()
        self.draw()
        self.showUserInput()
        self.showUserInputVisuals(self)

    def escape(self):
        self.value = self.savedValue
        super().escape()

    def getUserInput(self):
        self.initUserInput()
        super().run()

    def showUserInput(self):
        pos = self.rect.topright
        Display.write(Display.screen, self.userInputString, int(Config.FONT_SIZE * 1.5),
                      pos[0], pos[1], RED)

    def mouseButtonPressed(self, pos):
        super().mouseButtonPressed(pos)
        self.escape()

    def initUserInput(self):
        pass

    def backspace(self):
        pass

    def appendUserInput(self, userInput):
        pass
