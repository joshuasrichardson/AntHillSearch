import pygame.display
from pygame import MOUSEBUTTONUP, QUIT

from ColonyExceptions import GameOver
from Constants import SCREEN_COLOR, FONT_SIZE, LARGE_FONT_SIZE
from display import Display
from display.mainmenu.Settings import Settings
from display.mainmenu.Tutorial import Tutorial
from interface.RecordingPlayer import RecordingPlayer


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
        options = ["Play",
                   "Tutorial",
                   "Replay",
                   "Settings",
                   "Exit"]
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
        if option == "Play":
            self.play()
        elif option == "Tutorial":
            self.startTutorial()
        elif option == "Replay":
            self.replay()
        elif option == "Settings":
            self.viewSettings()
        elif option == "Exit":
            self.exit()
        self.mousePos = [-1, -1]

    def play(self):
        del self.simInterface
        self.simInterface = self.freshInterface()
        self.simInterface.runSimulation()

    def startTutorial(self):
        self.tutorial.run()

    def replay(self):
        del self.simInterface
        self.simInterface = RecordingPlayer()
        self.simInterface.runSimulation()

    def viewSettings(self):
        self.settings.run()

    @staticmethod
    def exit():
        pygame.quit()
        raise GameOver("Game Over")
