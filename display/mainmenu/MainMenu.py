import time

import pygame.display

import Utils
from config import Config
from ColonyExceptions import GameOver
from Constants import TRIAL_SETTINGS, RESULTS_DIR

from display import Display
from display.mainmenu.InterfaceSelector import InterfaceSelector
from display.buttons.MenuButton import MenuButton
from display.mainmenu.MenuScreen import MenuScreen
from display.buttons.Title import Title
from display.mainmenu.settings.Settings import Settings
from display.mainmenu.tutorial.Tutorial import Tutorial
from interface.RecordingPlayer import RecordingPlayer
from display.mainmenu.ReplaySelector import ReplaySelector


class MainMenu(MenuScreen):
    """ The menu the appears when the program starts up, allowing the user to choose among doing the test trials,
     practicing, running through a tutorial, viewing replays, changing settings, and exiting. """

    def __init__(self, interface):
        """ interface - the default interface used to run the test trials """
        Display.createScreen()  # Initialize the pygame screen
        super().__init__(self.getButtons())
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
            MenuButton("Test", self.doUserExperiments, spacing * 0),
            MenuButton("Practice", self.practice, spacing * 1),
            MenuButton("Tutorial", self.startTutorial, spacing * 2),
            MenuButton("Replay", self.replay, spacing * 3),
            MenuButton("Settings", self.viewSettings, spacing * 4),
            MenuButton("Exit", self.exit, spacing * 5)
        ]

    def run(self):
        try:
            super().run()
        except GameOver:  # End when the GameOver exception is raised
            pass

    def doUserExperiments(self):
        """ Run a simulation for each set of settings """
        for trial, trialSetting in enumerate(TRIAL_SETTINGS):
            Utils.setConfig(trialSetting)
            self.play()

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
                self.simInterface = RecordingPlayer(file_path)
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
