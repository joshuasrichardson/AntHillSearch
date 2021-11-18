import time

import pygame.display
from pygame import MOUSEBUTTONUP, QUIT

from ColonyExceptions import GameOver
from Constants import SCREEN_COLOR, FONT_SIZE, LARGE_FONT_SIZE, TRIAL_SETTINGS
from display import Display
from display.mainmenu.Settings import Settings
from display.mainmenu.Tutorial import Tutorial
from interface.RecordingPlayer import RecordingPlayer
from recording.Recorder import getMostRecentRecording

DO_USER_EXPERIMENTS = "Play"
PRACTICE = "Practice"
REPLAY = "Replay"
TUTORIAL = "Tutorial"
SETTINGS = "Settings"
EXIT = "Exit"


class StartUpDisplay:
    def __init__(self, interface):
        Display.createScreen()
        self.freshInterface = interface
        self.simInterface = None
        self.mousePos = [-1, -1]
        self.tutorial = Tutorial(self.play)
        self.settings = Settings()

    def run(self):
        try:
            while 1:
                Display.screen.fill(SCREEN_COLOR)
                self.drawStartPage()
                pygame.display.flip()
                self.handleEvents()
        except GameOver:
            pass

    def drawStartPage(self):
        Display.writeCenterPlus(Display.screen, "Anthill Search", LARGE_FONT_SIZE, -4 * LARGE_FONT_SIZE)
        options = [DO_USER_EXPERIMENTS,
                   PRACTICE,
                   TUTORIAL,
                   REPLAY,
                   SETTINGS,
                   EXIT]
        collides = False
        for i, option in enumerate(options):
            rect = Display.writeCenterPlus(Display.screen, option, FONT_SIZE * 2, FONT_SIZE * 3 * i)
            if rect.collidepoint(self.mousePos):
                self.start(option)
                break
            collides = collides or rect.collidepoint(pygame.mouse.get_pos())
        if collides:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                self.mousePos = pygame.mouse.get_pos()
            elif event.type == QUIT:
                pygame.quit()
                raise GameOver("Game Over")

    def start(self, option):
        if option == DO_USER_EXPERIMENTS:
            self.doUserExperiments()
        elif option == PRACTICE:
            self.play()
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
        for trial, trialSetting in enumerate(TRIAL_SETTINGS):
            self.setSettings(trialSetting)
            self.play()

    @staticmethod
    def setSettings(trialSetting):
        with open(trialSetting, 'r') as trialFile, open('display/mainmenu/settings.json', 'w') as currentSettings:
            currentSettings.write(trialFile.read())

    def play(self):
        del self.simInterface
        self.simInterface = self.freshInterface()
        self.simInterface.runSimulation()

    def startTutorial(self):
        self.tutorial.run()

    def replay(self):
        try:
            from os.path import getsize
            file_path = f'{getMostRecentRecording()}_RECORDING.json'
            if getsize(file_path) > 0:
                del self.simInterface
                self.simInterface = RecordingPlayer()
                self.simInterface.runSimulation()
            else:
                self.complainAboutMissingRecording()
        except FileNotFoundError:
            self.complainAboutMissingRecording()

    @staticmethod
    def complainAboutMissingRecording():
        Display.writeCenterPlus(Display.screen, "No Recording Available", LARGE_FONT_SIZE, 130)
        Display.writeCenterPlus(Display.screen, "Please play the simulation with the recording", FONT_SIZE, 130 + LARGE_FONT_SIZE)
        Display.writeCenterPlus(Display.screen, "option on before trying to watch a recording.", FONT_SIZE, 130 + LARGE_FONT_SIZE + FONT_SIZE)
        pygame.display.flip()
        time.sleep(2.5)
        print(f"'{getMostRecentRecording()}_RECORDING.json' is empty.")

    def viewSettings(self):
        self.settings.run()

    @staticmethod
    def exit():
        pygame.quit()
        raise GameOver("Game Over")
