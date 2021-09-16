import pygame.display
from pygame import MOUSEBUTTONUP, QUIT

from ColonyExceptions import GameOver
from Constants import SCREEN_COLOR, FONT_SIZE, WORDS_COLOR, LARGE_FONT_SIZE, BORDER_COLOR
from display import Display
from interface.RecordingPlayer import RecordingPlayer


class StartUpDisplay:
    def __init__(self, interface):
        Display.createScreen()
        Display.screen.fill(SCREEN_COLOR)
        Display.writeBigCenter(Display.screen, "Anthill Search")
        pygame.display.flip()

        self.freshInterface = interface
        self.simInterface = None
        self.mousePos = [0, 0]
        self.playPressed = False
        self.playButton = pygame.Rect(Display.origWidth / 2 - FONT_SIZE, Display.origHeight * 3 / 4 + FONT_SIZE + (FONT_SIZE / 2), FONT_SIZE * 2, FONT_SIZE * 2)
        self.tutorialButton = pygame.Rect(Display.origWidth / 2 - FONT_SIZE, Display.origHeight * 3 / 4 + 2 * FONT_SIZE, FONT_SIZE * 2, FONT_SIZE * 10)
        self.pageNumber = -1
        self.prevButton = pygame.Rect(0, 0, 0, 0)
        self.nextButton = pygame.Rect(0, 0, 0, 0)
        self.backButton = pygame.Rect(0, 0, 0, 0)
        self.pages = [None]
        for page in range(2, 11):
            self.pages.append("resources/instructions/page" + str(page) + ".png")
        self.pages.append(None)

    def run(self):
        try:
            Display.createScreen()
            while not self.playPressed:
                Display.screen.fill(SCREEN_COLOR)
                self.showInstructions()
                pygame.display.flip()
                self.handleEvents()
            self.simInterface.runSimulation()
            self.playAgain()
        except GameOver:
            pass

    def playAgain(self):
        self.playPressed = False
        self.pageNumber = -1
        self.mousePos = [-1, -1]
        self.run()

    def showInstructions(self):
        if self.pageNumber == -1:
            self.drawStartPage()
        elif self.pageNumber == 0:
            self.drawPage1()
        elif self.pageNumber == len(self.pages) - 1:
            self.drawLastPage()
        else:
            self.drawPage()

    def drawStartPage(self):
        Display.writeCenterPlus(Display.screen, "Anthill Search", LARGE_FONT_SIZE, -4 * LARGE_FONT_SIZE)
        options = ["Play",
                   "Tutorial",
                   "Replay",
                   "Settings",
                   "Exit"]
        for i, option in enumerate(options):
            rect = Display.writeCenterPlus(Display.screen, option, FONT_SIZE * 2, FONT_SIZE * 3 * i)
            if rect.collidepoint(self.mousePos):
                self.start(option)
                break

    def start(self, option):
        if option == "Play":
            self.play()
        elif option == "Tutorial":
            self.pageNumber += 1
        elif option == "Replay":
            self.replay()
        elif option == "Settings":
            pass
        elif option == "Exit":
            pygame.quit()
            raise GameOver("Game Over")

    def drawPage1(self):
        Display.writeCenterPlus(Display.screen, "Anthill Search", LARGE_FONT_SIZE, -4 * LARGE_FONT_SIZE)
        instructions = ["The ants old home has been broken!",
                        "Your task is to help them find the ",
                        "best new home in the area."]
        for i, instruction in enumerate(instructions):
            Display.writeCenterPlus(Display.screen, instruction, FONT_SIZE * 2, FONT_SIZE * 2 * i)
        self.drawBackButton()
        self.drawNextButton()

    def drawLastPage(self):
        Display.writeCenterPlus(Display.screen, "Anthill Search", LARGE_FONT_SIZE, -4 * LARGE_FONT_SIZE)
        instructions = ["Good luck!"]
        for i, instruction in enumerate(instructions):
            Display.writeCenterPlus(Display.screen, instruction, FONT_SIZE * 2, FONT_SIZE * 2 * i)
        self.drawBackButton()
        self.drawPreviousButton()
        self.drawPlayButton()

    def drawPage(self):
        page2 = pygame.image.load(self.pages[self.pageNumber])
        page2 = page2.convert_alpha()
        page2 = pygame.transform.scale(page2, (Display.origWidth, Display.origHeight))
        Display.screen.blit(page2, [0, 0])
        self.drawBackButton()
        self.drawPreviousButton()
        self.drawNextButton()

    def drawNextButton(self):
        nextImg = pygame.font.SysFont('Comic Sans MS', FONT_SIZE * 2).render("NEXT >", True, WORDS_COLOR).convert_alpha()
        self.nextButton = pygame.Rect(Display.origWidth * 3 / 4 - 2 * nextImg.get_width(), Display.origHeight * 3 / 4 + FONT_SIZE,
                                      nextImg.get_width(), nextImg.get_height())
        Display.screen.blit(nextImg, self.nextButton.topleft)

    def drawPreviousButton(self):
        prevImg = pygame.font.SysFont('Comic Sans MS', FONT_SIZE * 2).render("< PREV", True, WORDS_COLOR).convert_alpha()
        self.prevButton = pygame.Rect(Display.origWidth / 4 + prevImg.get_width(), Display.origHeight * 3 / 4 + FONT_SIZE,
                                      prevImg.get_width(), prevImg.get_height())
        Display.screen.blit(prevImg, self.prevButton.topleft)

    def drawBackButton(self):
        backImg = pygame.font.SysFont('Comic Sans MS', FONT_SIZE * 2).render("<- BACK", True, WORDS_COLOR).convert_alpha()
        self.backButton = pygame.Rect(100, 100, backImg.get_width(), backImg.get_height())
        Display.screen.blit(backImg, self.backButton.topleft)

    def drawPlayButton(self):
        Display.drawRect(Display.screen, BORDER_COLOR, self.playButton, 1, False)
        pygame.draw.polygon(Display.screen, WORDS_COLOR, [[self.playButton.left + 4, self.playButton.top + 4],
                                                          [self.playButton.right - 4, self.playButton.centery],
                                                          [self.playButton.left + 4, self.playButton.bottom - 4]])

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                self.mouseButtonPressed(pygame.mouse.get_pos())
            elif event.type == QUIT:
                pygame.quit()
                raise GameOver("Game Over")

    def mouseButtonPressed(self, pos):
        self.mousePos = pos
        if self.playButton.collidepoint(pos):
            self.play()
        elif self.nextButton.collidepoint(pos) and self.pageNumber < len(self.pages) - 1:
            self.pageNumber += 1
        elif self.prevButton.collidepoint(pos) and self.pageNumber > 0:
            self.pageNumber -= 1
        elif self.backButton.collidepoint(pos):
            self.pageNumber = -1

    def play(self):
        self.playPressed = True
        del self.simInterface
        self.simInterface = self.freshInterface()

    def replay(self):
        del self.simInterface
        self.simInterface = RecordingPlayer()
        self.playPressed = True
