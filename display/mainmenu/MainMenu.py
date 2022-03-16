import json
import time

import pygame.display
from pygame import MOUSEBUTTONUP, QUIT

from config import Config
from ColonyExceptions import GameOver
from Constants import SCREEN_COLOR, TRIAL_SETTINGS, BLUE, CONFIG_FILE_NAME, RESULTS_DIR, FULL_CONTROL_NAME, DISTRACTED_NAME

from display import Display
from display.mainmenu.InterfaceSelector import InterfaceSelector
from display.mainmenu.settings.Settings import Settings
from display.mainmenu.tutorial.Tutorial import Tutorial
from interface.RecordingPlayer import RecordingPlayer
from display.mainmenu.ReplaySelector import ReplaySelector

DO_USER_EXPERIMENTS = "Test"
PRACTICE = "Practice"
REPLAY = "Replay"
TUTORIAL = "Tutorial"
SETTINGS = "Settings"
EXIT = "Exit"


class StartUpDisplay:
    def __init__(self, interface):
        Display.createScreen()  # Initialize the pygame screen
        self.defaultInterface = interface  # The interface to be played when the "Play" option is selected
        self.freshInterface = interface  # The interface to run when "Play" or "Practice" is selected
        self.interfaceSelector = InterfaceSelector()  # An object used to change the interface
        self.replaySelector = ReplaySelector()  # An object used to select a recent replay
        self.simInterface = None  # A constructed version of the interface that we will run
        self.mousePos = [-1, -1]  # Where the mouse is (for when something is selected)
        self.tutorial = Tutorial(self.practice)  # The tutorial about how to play the game
        self.settings = Settings()  # Settings that can be changed

    def run(self):
        try:
            while 1:  # Keep going till the game is over
                Display.screen.fill(SCREEN_COLOR)  # Fill in the background
                self.drawStartPage()  # Draw game title and options the user can select
                pygame.display.flip()  # Have the things that have been drawn show up
                self.handleEvents()  # Handle any user input
        except GameOver:  # End when the GameOver exception is raised
            pass

    def drawStartPage(self):
        # Write the simulation title
        Display.writeCenterPlus(Display.screen, "Anthill Search", Config.LARGE_FONT_SIZE, -4 * Config.LARGE_FONT_SIZE)
        # The options the user can select
        options = [DO_USER_EXPERIMENTS,
                   PRACTICE,
                   TUTORIAL,
                   REPLAY,
                   SETTINGS,
                   EXIT]
        # Whether the mouse collides with a word
        mouseIsOverAnOption = False
        # Check each option to see if the mouse is over it
        for i, option in enumerate(options):
            rect = Display.writeCenterPlus(Display.screen, option, Config.FONT_SIZE * 2, Config.FONT_SIZE * 3 * i)
            if rect.collidepoint(self.mousePos):
                self.start(option)
                break
            mouseIsOverCurrentOption = rect.collidepoint(pygame.mouse.get_pos())
            mouseIsOverAnOption = mouseIsOverAnOption or mouseIsOverCurrentOption
            if mouseIsOverCurrentOption:
                Display.writeCenterPlus(Display.screen, option, Config.FONT_SIZE * 2, Config.FONT_SIZE * 3 * i, BLUE)
        if mouseIsOverAnOption:
            # Change the cursor to be a hand
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            # Change the cursor to be an arrow (same as default)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:  # If the user clicked, update the mouse position
                self.mousePos = pygame.mouse.get_pos()
            elif event.type == QUIT:  # If the user pressed the x to close the game, stop the game
                self.exit()

    def start(self, option):
        """ Start another page from the main menu """
        if option == DO_USER_EXPERIMENTS:
            self.doUserExperiments()
        elif option == PRACTICE:
            self.practice()
        elif option == TUTORIAL:
            self.startTutorial()
        elif option == REPLAY:
            self.replay()
        elif option == SETTINGS:
            self.viewSettings()
        elif option == EXIT:
            self.exit()
        self.mousePos = [-1, -1]

    def doUserExperiments(self):
        """ Run a simulation for each set of settings """
        for trial, trialSetting in enumerate(TRIAL_SETTINGS):
            self.setSettings(trialSetting)
            self.play()

    @staticmethod
    def setSettings(trialSetting):
        """ Copy the current trial's settings to the settings file that will be used in the simulation """
        currentSettings = open(CONFIG_FILE_NAME, 'r')
        current = json.load(currentSettings)
        currentSettings.close()
        with open(trialSetting, 'r') as trialFile, open(CONFIG_FILE_NAME, 'w') as currentSetting:
            trial = json.load(trialFile)
            trial[FULL_CONTROL_NAME] = current[FULL_CONTROL_NAME]
            trial[DISTRACTED_NAME] = current[DISTRACTED_NAME]
            json.dump(trial, currentSetting)

    def practice(self):
        interface = self.interfaceSelector.chooseInterface()
        if interface is not None:
            self.freshInterface = interface
            self.play()
        self.freshInterface = self.defaultInterface

    def play(self):
        """ Construct and start the simulation """
        try:
            del self.simInterface
        except AttributeError:
            print("Nothing to delete")
        self.simInterface = self.freshInterface()
        self.simInterface.runSimulation()
        Display.resetScreen()

    def startTutorial(self):
        """ Start the tutorial to teach about how to play """
        self.tutorial.run()

    def replay(self):
        """ Watch one of the most recent simulation's replays """
        replay = self.replaySelector.chooseReplay()
        file_path = RESULTS_DIR + replay
        try:  # If the recording exists, play it, else tell the user there is no recording
            del self.simInterface
            self.simInterface = RecordingPlayer(replay)
            self.simInterface.runSimulation()
            Display.resetScreen()
        except FileNotFoundError:
            self.complainAboutMissingRecording(file_path)

    @staticmethod
    def complainAboutMissingRecording(file_path):
        """ Tell the user there is no recording so they can't play the recording """
        Display.writeCenterPlus(Display.screen, "No Recording Available", Config.LARGE_FONT_SIZE, 130)
        Display.writeCenterPlus(Display.screen, "Please play the simulation with the recording",
                                Config.FONT_SIZE, 130 + Config.LARGE_FONT_SIZE)
        Display.writeCenterPlus(Display.screen, "option on before trying to watch a recording.",
                                Config.FONT_SIZE, 130 + Config.LARGE_FONT_SIZE + Config.FONT_SIZE)
        pygame.display.flip()
        time.sleep(2.5)
        print(f"'{file_path} is empty.")

    def viewSettings(self):
        """ Enter the settings tab """
        self.settings.run()

    @staticmethod
    def exit():
        """ Close the pygame window and exit the program """
        pygame.quit()
        raise GameOver("Exiting")
