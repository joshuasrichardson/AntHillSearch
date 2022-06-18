import pygame

from Constants import UI_CONTROL_OPTIONS, OTHER_OPTIONS, OTHER_CONTROLS
from config import Config
from config.Config import FONT_SIZE
from display import Display
from display.buttons.AdjustableBox import Box
from display.buttons.EnableButton import EnableButton
from display.buttons.NextButton import NextButton
from display.buttons.PrevButton import PrevButton
from display.buttons.Title import Title


class Options(Box):
    """ A box that can be displayed while the simulation is paused, that displays options about how the user can
    interact with the simulation """

    def __init__(self, end, controlOptions=UI_CONTROL_OPTIONS):
        """ end - a function used to end the current simulation and bring the user out to the main menu or somewhere
        controlOptions - the set of options that are available to the user based on their current interface """
        self.controlOptions = controlOptions
        right, bottom = Display.screen.get_size()
        super().__init__("Options", self.onClick, right / 4, bottom / 4, right / 2, bottom / 2)

        self.pageNumber = 0
        self.visible = False

        self.viewOptsButton = EnableButton("Options", self.show, False, False,
                                           Display.origWidth / 2 - (6.5 * Config.FONT_SIZE),
                                           Display.origHeight / 2 - Config.FONT_SIZE,
                                           13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE,
                                           canActivate=False, fontSize=int(1.5 * Config.FONT_SIZE))

        self.closeButton = EnableButton(" X ", self.hide, False, True,
                                        self.rect.right - Config.FONT_SIZE * 3, self.rect.top + 10,
                                        canActivate=False, fontSize=int(1.5 * Config.FONT_SIZE))

        self.exitButton = EnableButton("  Exit Simulation  ", end, False, True, self.rect.centerx, self.rect.bottom + 10,
                                       recenter=True, fontSize=int(1.5 * Config.FONT_SIZE))

        self.buttons = [self.viewOptsButton, self.closeButton, Title("Options", self.rect.top),
                        NextButton(self, self.rect.right - Config.FONT_SIZE * 6, self.rect.bottom - Config.FONT_SIZE * 3),
                        PrevButton(self, self.rect.left + Config.FONT_SIZE, self.rect.bottom - Config.FONT_SIZE * 3),
                        self.exitButton]

    def onClick(self):
        pos = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.collides(pos):
                button.action()

    def show(self):
        self.visible = True
        self.viewOptsButton.visible = False

    def clear(self):
        self.visible = False
        self.viewOptsButton.visible = False

    def hide(self):
        self.visible = False
        self.viewOptsButton.visible = True

    def change(self):
        self.visible = not self.visible
        self.viewOptsButton.visible = not self.viewOptsButton.visible

    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.visible:
            super().draw()
            self.drawOptions()
            for button in self.buttons:
                button.update(pos)
                button.draw()
        else:
            self.viewOptsButton.update(pos)
            self.viewOptsButton.draw()

    def collides(self, pos):
        return not self.visible and self.viewOptsButton.collides(pos) or \
               self.visible and self.innerButtonCollides(pos)

    def innerButtonCollides(self, pos):
        for button in self.buttons:
            if button.collides(pos):
                return True
        return False

    @staticmethod
    def getNumPages():
        return 2

    def next(self):
        if self.pageNumber < self.getNumPages() - 1:
            self.pageNumber += 1

    def prev(self):
        if self.pageNumber > 0:
            self.pageNumber -= 1

    def drawOptions(self):
        if self.pageNumber == 0:
            self.drawOptionsPage0()
        else:
            self.drawOptionsPage1()

    def drawOptionsPage0(self):
        agentOptions = self.controlOptions["agentOptions"]
        agentControls = self.controlOptions["agentControls"]

        longerListSize = len(agentOptions)

        siteOptions = self.controlOptions["siteOptions"]
        siteControls = self.controlOptions["siteControls"]

        if len(siteOptions) > longerListSize:
            longerListSize = len(siteOptions)

        Display.write(Display.screen, "Agent Options:", FONT_SIZE + 4, self.rect.left + 10, self.rect.top + 10)

        h = self.rect.height / longerListSize - 4
        for i, option in enumerate(agentOptions):
            Display.write(Display.screen, option, FONT_SIZE, self.rect.left + 10, self.rect.top + 40 + i * h)

        for i, control in enumerate(agentControls):
            Display.write(Display.screen, control, FONT_SIZE, self.rect.left + 130, self.rect.top + 40 + i * h)

        Display.write(Display.screen, "Site Options:", FONT_SIZE + 4, self.rect.centerx, self.rect.top + 10)

        for i, option in enumerate(siteOptions):
            Display.write(Display.screen, option, FONT_SIZE, self.rect.centerx, self.rect.top + 40 + i * h)

        for i, control in enumerate(siteControls):
            Display.write(Display.screen, control, FONT_SIZE, self.rect.centerx + 120, self.rect.top + 40 + i * h)

    def drawOptionsPage1(self):
        Display.write(Display.screen, "Other Options:", FONT_SIZE + 4, self.rect.left + 10, self.rect.top + 10)

        h = self.rect.height / len(OTHER_OPTIONS) - 7

        for i, option in enumerate(OTHER_OPTIONS):
            Display.write(Display.screen, option, FONT_SIZE, self.rect.left + 10, self.rect.top + 40 + i * h)

        for i, control in enumerate(OTHER_CONTROLS):
            Display.write(Display.screen, control, FONT_SIZE, self.rect.centerx, self.rect.top + 40 + i * h)
