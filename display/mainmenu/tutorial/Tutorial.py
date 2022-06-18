import pygame
from pygame import KEYDOWN, K_RIGHT, K_LEFT

from config import Config
from display import Display
from display.mainmenu.MenuScreen import MenuScreen
from display.buttons.PlayButton import PlayButton
from display.buttons.PrevButton import PrevButton
from display.buttons.NextButton import NextButton
from display.buttons.BackButton import BackButton
from display.mainmenu.tutorial.Page import Page


class Tutorial(MenuScreen):
    """ A menu screen that displays the pages of the tutorial and allows the user to run a practice round at the end
    of the tutorial """

    def __init__(self, play):
        """ play - the function used to play a practice round of the simulation """
        self.play = play
        self.pageNumber = 0
        self.pages = [Page("", 0, self)]
        self.pages += [Page(f"display/mainmenu/tutorial/instructions/page{page}.png", page, self) for page in range(1, 29)]
        self.pages += [Page("", len(self.pages), self)]
        super().__init__([*self.pages, BackButton(), PrevButton(self), NextButton(self), PlayButton(self, canPause=False)])

    def getNumPages(self):
        return len(self.pages)

    def drawPage(self):
        if self.pageNumber == 0:
            self.drawIntroPage()
        elif self.pageNumber == len(self.pages) - 1:
            self.drawLastPage()
        else:
            self.drawMiddlePage()

    def drawIntroPage(self):
        Display.writeCenterPlus(Display.screen, "Anthill Search", Config.LARGE_FONT_SIZE, -4 * Config.LARGE_FONT_SIZE)
        instructions = ["The ants old home has been broken!",
                        "Your mission is to help them ",
                        "find the best new home in the area ",
                        "in the shortest time possible ",
                        "with as many survivors as possible."]
        for i, instruction in enumerate(instructions):
            Display.writeCenterPlus(Display.screen, instruction, Config.FONT_SIZE * 2, Config.FONT_SIZE * 2 * i)

    def drawMiddlePage(self):
        page = pygame.image.load(self.pages[self.pageNumber].fileName).convert_alpha()
        page = pygame.transform.scale(page, (Display.origWidth, Display.origHeight))
        Display.screen.blit(page, [0, 0])

    def drawLastPage(self):
        Display.writeCenterPlus(Display.screen, "Anthill Search", Config.LARGE_FONT_SIZE, -4 * Config.LARGE_FONT_SIZE)
        instructions = ["Remember:",
                        "",
                        " Good quality home ",
                        " Short time ",
                        " Many survivors ",
                        "",
                        "Good luck!",
                        "",
                        "Press play to do a practice round."]
        for i, instruction in enumerate(instructions):
            Display.writeCenterPlus(Display.screen, instruction, Config.FONT_SIZE * 2, Config.FONT_SIZE * 2 * i)

    def shouldDrawPlayButton(self):
        return self.pageNumber == len(self.pages) - 1

    def handleEvent(self, event):
        super().handleEvent(event)
        if event.type == KEYDOWN:
            if event.key == K_LEFT and self.pageNumber >= 0:
                self.pageNumber -= 1
            elif event.key == K_RIGHT and self.pageNumber < len(self.pages) - 1:
                self.pageNumber += 1
