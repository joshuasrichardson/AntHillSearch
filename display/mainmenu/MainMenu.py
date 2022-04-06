import json
import time

import pygame.display

from config import Config
from ColonyExceptions import GameOver
from Constants import TRIAL_SETTINGS, CONFIG_FILE_NAME, RESULTS_DIR, COPY_FROM_CONFIG

from display import Display
from display.mainmenu.InterfaceSelector import InterfaceSelector
from display.mainmenu.buttons.MenuButton import MenuButton
from display.mainmenu.MenuScreen import MenuScreen
from display.mainmenu.buttons.Title import Title
from display.mainmenu.settings.Settings import Settings
from display.mainmenu.tutorial.Tutorial import Tutorial
from interface.RecordingPlayer import RecordingPlayer
from display.mainmenu.ReplaySelector import ReplaySelector


class StartUpDisplay(MenuScreen):
    def __init__(self, interface):
        super().__init__(self.getButtons())
        Display.createScreen()  # Initialize the pygame screen
        self.defaultInterface = interface  # The interface to be played when the "Play" option is selected
        self.freshInterface = interface  # The interface to run when "Play" or "Practice" is selected
        self.interfaceSelector = InterfaceSelector()  # An object used to change the interface
        self.replaySelector = ReplaySelector()  # An object used to select a recent replay
        self.simInterface = None  # A constructed version of the interface that we will run
        self.mousePos = [-1, -1]  # Where the mouse is (for when something is selected)
        self.tutorial = Tutorial(self.practice)  # The tutorial about how to play the game
        self.settings = Settings()  # Settings that can be changed

    def getButtons(self):
        spacing = Config.FONT_SIZE * 3
        return [
            Title("Anthill Search", 200),
            MenuButton(self.doUserExperiments, "Test", spacing * 0),
            MenuButton(self.practice, "Practice", spacing * 1),
            MenuButton(self.startTutorial, "Tutorial", spacing * 2),
            MenuButton(self.replay, "Replay", spacing * 3),
            MenuButton(self.viewSettings, "Settings", spacing * 4),
            MenuButton(self.exit, "Exit", spacing * 5)
        ]

    def run(self):
        try:
            super().run()
        except GameOver:  # End when the GameOver exception is raised
            pass

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
            for setting in COPY_FROM_CONFIG:
                trial[setting] = current[setting]
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
        self.replaySelector = ReplaySelector()  # Reconstruct it to make sure that the most recent recordings show up.
        replay = self.replaySelector.chooseReplay()
        file_path = RESULTS_DIR + replay
        if replay != "":
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
