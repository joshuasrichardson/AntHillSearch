import pygame
from pygame import MOUSEBUTTONDOWN, KEYUP, KMOD_CTRL

from ColonyExceptions import GameOver
from Constants import GRAPHS_TOP_LEFT, SCREEN_COLOR, ORANGE, STATES_LIST, STATE_COLORS, PHASES_LIST, PHASE_COLORS, BLUE, \
    CONTROL_OPTIONS, RECORDING_CONTROL_OPTIONS, SIMPLIFY_STATES
from config import Config
from display import Display
from display.buttons.Button import Button
from display.buttons.EnableButton import EnableButton
from display.mainmenu.MenuScreen import MenuScreen
from display.buttons.InputButton import InputButton
from display.simulation.AgentGraph import AgentGraph
from display.simulation.ChatBox import ChatBox
from display.simulation.CommandHistBox import CommandHistBox
from display.simulation.Options import Options
from display.simulation.StateNumDisplay import StateNumDisplay
from display.simulation.TimerDisplay import TimerDisplay
from display.simulation.WorldDisplay import drawWorldObjects, drawPotentialQuality
from user.SelectRect import SelectRect


class SimulationDisplay(MenuScreen):
    """ The screen used to draw the world, objects in the world, and buttons and boxes the user interacts with. This
     screen also handles some events related to the buttons and boxes. """

    def __init__(self, world, timer):
        """ world - the world to be displayed
        timer - the timer to be displayed
        selectRect - the rectangle to be displayed that selects agents and sites """
        self.world = world
        self.timer = timer
        self.selectRect = SelectRect()
        self.timerDisplay = TimerDisplay(timer)
        self.screenBorder = []
        self.potentialQuality = 0
        self.shouldDrawQuality = False
        self.numSelectedAgents = 0
        self.numSelectedSites = 0
        self.selectedSites = []
        self.collidesWithWorldObject = False

        self.chatBox = ChatBox()
        self.inputBox = InputButton(self.chatBox.rect.x + 6, self.chatBox.rect.y + self.chatBox.rect.h
                                    - Config.FONT_SIZE * 3.5, self.chatBox.rect.w - 12, Config.FONT_SIZE * 3, self.chatBox)
        self.chatBox.setInput(self.inputBox)

        self.commandHistBox = CommandHistBox()

        self.pauseButton = None
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

        self.commandSiteAgentsButton = Button("", lambda: None, 0, 0) if SIMPLIFY_STATES else EnableButton(
            " Command Sites Agents ", lambda: None, True, True,
            Display.origWidth - (15 * Config.FONT_SIZE),
            Display.origHeight - (5 * Config.FONT_SIZE),
            13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)

        border = Button("", lambda: None, 0, 0)
        border.draw = self.drawScreenBorder

        self.adjustables = [self.inputBox, self.chatBox, self.commandHistBox]
        # First button is handled first but drawn last
        super().__init__([border, self.optionsScreen, self.inputBox, self.chatBox, self.commandHistBox,
                          self.selectAgentsButton, self.selectSitesButton, self.commandSiteAgentsButton])

        if Config.INTERFACE_NAME == "Engineering":
            self.buttons += [self.selectAgentsSitesButton, self.selectSitesAgentsButton,
                             AgentGraph("STATES", STATES_LIST, world.states, STATE_COLORS, GRAPHS_TOP_LEFT[0], GRAPHS_TOP_LEFT[1]),
                             AgentGraph("PHASES", PHASES_LIST, world.phases, PHASE_COLORS, GRAPHS_TOP_LEFT[0], GRAPHS_TOP_LEFT[1] + 175),
                             StateNumDisplay()]
            self.optionsScreen.controlOptions = CONTROL_OPTIONS
        elif Config.INTERFACE_NAME == "Recording":
            self.buttons += [self.selectAgentsSitesButton, self.selectSitesAgentsButton,
                             AgentGraph("STATES", STATES_LIST, world.states, STATE_COLORS, GRAPHS_TOP_LEFT[0], GRAPHS_TOP_LEFT[1]),
                             AgentGraph("PHASES", PHASES_LIST, world.phases, PHASE_COLORS, GRAPHS_TOP_LEFT[0], GRAPHS_TOP_LEFT[1] + 175)]
            self.optionsScreen.controlOptions = RECORDING_CONTROL_OPTIONS
        else:
            self.selectAgentsButton.rect.y = Display.origHeight - (5 * Config.FONT_SIZE)
            self.selectSitesButton.rect.y = Display.origHeight - (5 * Config.FONT_SIZE)

    def setPauseButton(self, button):
        self.pauseButton = button
        self.buttons.append(button)

    def handleEvent(self, event):
        super().handleEvent(event)
        pos = pygame.mouse.get_pos()
        buttonIsSelected = False
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.mouseButtonDown(pos):
                    buttonIsSelected = True
                    break  # Skip the rest if one of the buttons handles it. We only want to press one at a time.
        elif event.type == KEYUP:
            self.inputBox.input(event)
        return not self.inputBox.typing and not buttonIsSelected

    def mouseButtonPressed(self, pos):
        if not self.selectRect.isSelecting(pos):
            super().mouseButtonPressed(pos)

    def scrollUp(self, times=1):
        if not pygame.key.get_mods() & KMOD_CTRL:
            pos = pygame.mouse.get_pos()
            for button in self.adjustables:
                if button.rect.collidepoint(pos):
                    for _ in range(times):
                        button.scrollUp()
                    break  # Only scroll up on one

    def scrollDown(self, times=1):
        if not pygame.key.get_mods() & KMOD_CTRL:
            pos = pygame.mouse.get_pos()
            for button in self.adjustables:
                if button.rect.collidepoint(pos):
                    for _ in range(times):
                        button.scrollDown()
                    break  # Only scroll up on one

    def displayScreen(self):
        Display.screen.fill(SCREEN_COLOR)
        drawWorldObjects(self.world)

        pos = pygame.mouse.get_pos()
        if self.numSelectedAgents > 0:  # Display the number of agents that are selected by the mouse
            Display.write(Display.screen, f"{self.numSelectedAgents}", Config.FONT_SIZE,
                          pos[0] + Config.FONT_SIZE, pos[1] + Config.FONT_SIZE, BLUE)
            if self.numSelectedAgents > 1:
                Display.write(Display.screen, "Cut the number of selected ants in half by pressing 'H'",
                              Config.FONT_SIZE, Display.origWidth - 420, 4 * Config.FONT_SIZE, BLUE)
        if self.numSelectedSites > 0 and self.shouldDrawQuality:
            drawPotentialQuality(self.world, self.potentialQuality)
        if self.selectRect.isSelecting(pos):
            self.selectRect.draw(pos)  # The displayed rect and selectRect need to be different when the screen moves

        for button in reversed(self.buttons):
            button.draw()
        self.timerDisplay.drawRemainingTime()
        Display.drawBorder()
        pygame.display.flip()

    def escape(self):
        pass

    def updateCursor(self):
        if not self.selectRect.isSelecting():
            isResizing = False
            for resizable in self.adjustables:
                if resizable.resizing():
                    isResizing = True
                    break
            if not isResizing:
                super().updateCursor()

    def collidesWithSelectable(self, pos):
        return self.collidesWithWorldObject or super().collidesWithSelectable(pos)

    def drawScreenBorder(self):
        if len(self.screenBorder) > 0:
            Display.drawRect(Display.screen, ORANGE, pygame.Rect(*self.screenBorder), 1, True)

    def quit(self):
        self.pauseButton.isPaused = False
        self.timer.cancel()
        raise GameOver("Game Over")
