import pygame
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYUP, KMOD_CTRL, KEYDOWN, K_p, K_o

from ColonyExceptions import GameOver
from Constants import GRAPHS_TOP_LEFT, SCREEN_COLOR, ORANGE, STATES_LIST, STATE_COLORS, PHASES_LIST, PHASE_COLORS
from config import Config
from display import Display
from display.buttons.Button import Button
from display.buttons.EnableButton import EnableButton
from display.buttons.PlayButton import PlayButton
from display.mainmenu.MenuScreen import MenuScreen
from display.buttons.InputButton import InputButton
from display.simulation.AgentGraph import AgentGraph
from display.simulation.ChatBox import ChatBox
from display.simulation.CommandHistBox import CommandHistBox
from display.simulation.Options import Options
from display.simulation.StateNumDisplay import StateNumDisplay
from display.simulation.TimerDisplay import TimerDisplay
from display.simulation.WorldDisplay import drawWorldObjects


class SimulationDisplay(MenuScreen):

    def __init__(self, userControls, world, timer):
        self.userControls = userControls
        self.world = world
        self.timer = timer
        self.timerDisplay = TimerDisplay(timer)
        self.screenBorder = []
        self.userControls.initSimDisp(self)  # TODO: Take this out when we don't need it anymore

        self.chatBox = ChatBox()
        self.inputBox = InputButton(self.chatBox.rect.x + 10, self.chatBox.rect.y + self.chatBox.rect.h
                                    - Config.FONT_SIZE * 3.5, self.chatBox.rect.w - 20, Config.FONT_SIZE * 3, self.chatBox)
        self.chatBox.setInput(self.inputBox)

        self.commandHistBox = CommandHistBox()

        self.pauseButton = PlayButton(self, Display.screen.get_width() - 60, GRAPHS_TOP_LEFT[1])
        self.optionsScreen = Options(self.quit)

        self.selectAgentsButton = EnableButton(" Select Agents ", lambda: None, True, True,
                                               Display.origWidth - 3 * (14 * Config.FONT_SIZE),
                                               Display.origHeight - (7 * Config.FONT_SIZE + 2),
                                               13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)

        self.selectSitesButton = EnableButton(" Select Sites ", lambda: None, True, True,
                                              Display.origWidth - 2 * (14.25 * Config.FONT_SIZE),
                                              Display.origHeight - (7 * Config.FONT_SIZE + 2),
                                              13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)

        self.selectAgentsSitesButton = EnableButton(" Select Agents Sites ", lambda: None, False, True,
                                                    Display.origWidth - 3 * (14 * Config.FONT_SIZE),
                                                    Display.origHeight - (5 * Config.FONT_SIZE),
                                                    13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)

        self.selectSitesAgentsButton = EnableButton(" Select Sites Agents ", lambda: None, False, True,
                                                    Display.origWidth - 2 * (14.25 * Config.FONT_SIZE),
                                                    Display.origHeight - (5 * Config.FONT_SIZE),
                                                    13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)

        self.commandSiteAgentsButton = EnableButton(" Command Sites Agents ", lambda: None, True, True,
                                                    Display.origWidth - (15 * Config.FONT_SIZE),
                                                    Display.origHeight - (5 * Config.FONT_SIZE),
                                                    13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)

        border = Button("", lambda: None, 0, 0)
        border.draw = self.drawScreenBorder

        self.adjustables = [self.inputBox, self.chatBox, self.commandHistBox]
        # First button is handled first but drawn last
        super().__init__([border, self.optionsScreen, self.inputBox, self.chatBox, self.commandHistBox,
                          AgentGraph("STATES", STATES_LIST, world.states, STATE_COLORS, GRAPHS_TOP_LEFT[0], GRAPHS_TOP_LEFT[1]),
                          AgentGraph("PHASES", PHASES_LIST, world.phases, PHASE_COLORS, GRAPHS_TOP_LEFT[0], GRAPHS_TOP_LEFT[1] + 175),
                          self.pauseButton, self.selectAgentsButton, self.selectSitesButton, self.commandSiteAgentsButton,
                          StateNumDisplay()])

        if Config.INTERFACE_NAME == "Engineering":
            self.buttons += [self.selectAgentsSitesButton, self.selectSitesAgentsButton]
        else:
            self.selectAgentsButton.rect.y = Display.origHeight - (5 * Config.FONT_SIZE)
            self.selectSitesButton.rect.y = Display.origHeight - (5 * Config.FONT_SIZE)

    def handleEvent(self, event):
        super().handleEvent(event)
        pos = pygame.mouse.get_pos()
        buttonIsSelected = False
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.mouseButtonDown(pos):
                    buttonIsSelected = True
                    break  # Skip the rest if one of the buttons handles it. We only want to press one at a time.
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                for button in self.buttons:
                    button.mouseButtonUp(pos)
            elif not pygame.key.get_mods() & KMOD_CTRL:
                self.scroll(event.button, pos)
        elif event.type == KEYUP:
            self.inputBox.input(event)
        if not self.inputBox.typing and not buttonIsSelected:
            if event.type == KEYDOWN:
                if event.key == K_p:
                    self.pauseButton.playOrPause()
                elif event.key == K_o and self.pauseButton.isPaused:
                    self.optionsScreen.change()
            self.userControls.handleEvent(event)

    def displayScreen(self):
        Display.moveScreen()
        Display.screen.fill(SCREEN_COLOR)
        drawWorldObjects(self.world)
        self.userControls.drawChanges()
        for button in reversed(self.buttons):
            button.draw()
        self.timerDisplay.drawRemainingTime()
        Display.drawBorder()
        pygame.display.flip()

    def escape(self):
        pass

    def scrollUp(self, times=1):
        pass

    def scrollDown(self, times=1):
        pass

    def scroll(self, mouseButton, pos):
        if mouseButton == 4 or mouseButton == 6:
            for button in self.adjustables:
                if button.rect.collidepoint(pos):
                    button.scrollUp()
                    break  # Only scroll up on one
        elif mouseButton == 5 or mouseButton == 7:
            for button in self.adjustables:
                if button.rect.collidepoint(pos):
                    button.scrollDown()
                    break  # Only scroll up on one

    def updateCursor(self):
        isResizing = False
        for resizable in self.adjustables:
            if resizable.resizing():
                isResizing = True
                break
        if not isResizing:
            super().updateCursor()

    @staticmethod
    def shouldDrawPlayButton():
        return True

    def play(self):
        pass

    def pause(self):
        self.optionsScreen.hide()
        self.timer.pause(self.handleEvent, self.pauseButton.collides, self.displayScreen)
        self.optionsScreen.clear()
        self.pauseButton.playOrPause()

    def quit(self):
        self.pauseButton.isPaused = False
        self.timer.cancel()
        raise GameOver("Game Over")

    def drawScreenBorder(self):
        if len(self.screenBorder) > 0:
            Display.drawRect(Display.screen, ORANGE, pygame.Rect(*self.screenBorder), 1, True)
