import pygame.display
from pygame import MOUSEBUTTONUP, QUIT

from Constants import SCREEN_COLOR, FONT_SIZE, WORDS_COLOR, LARGE_FONT_SIZE, BORDER_COLOR
from display import Display


class StartUpDisplay:
    def __init__(self, interface):
        Display.createScreen()
        Display.screen.fill(SCREEN_COLOR)
        Display.writeBigCenter(Display.screen, "Anthill Search")
        pygame.display.flip()

        self.simInterface = interface()
        self.playPressed = False
        self.playButton = pygame.Rect(Display.origWidth / 2 - FONT_SIZE, Display.origHeight * 3 / 4 + FONT_SIZE + (FONT_SIZE / 2), FONT_SIZE * 2, FONT_SIZE * 2)
        self.pageNumber = 0
        self.prevButton = pygame.Rect(0, 0, 0, 0)
        self.nextButton = pygame.Rect(0, 0, 0, 0)
        self.pages = [None]
        for page in range(2, 11):
            self.pages.append("resources/instructions/page" + str(page) + ".png")
        self.pages.append(None)

    def run(self):
        while not self.playPressed:
            Display.screen.fill(SCREEN_COLOR)
            self.showInstructions()
            self.drawPlayButton()
            pygame.display.flip()
            self.handleEvents()
        self.simInterface.runSimulation()

    def showInstructions(self):
        if self.pageNumber == 0:
            self.drawPage1()
        elif self.pageNumber == len(self.pages) - 1:
            self.drawLastPage()
        else:
            self.drawPage()
        if self.pageNumber < len(self.pages) - 1:
            self.drawNextButton()
        if self.pageNumber > 0:
            self.drawPreviousButton()

    @staticmethod
    def drawPage1():
        Display.writeCenterPlus(Display.screen, "Anthill Search", LARGE_FONT_SIZE, -4 * LARGE_FONT_SIZE)
        instructions = ["The ants old home has been broken!",
                        "Your task is to help them find the ",
                        "best new home in the area."]
        for i, instruction in enumerate(instructions):
            Display.writeCenterPlus(Display.screen, instruction, FONT_SIZE * 2, FONT_SIZE * 2 * i)

    @staticmethod
    def drawLastPage():
        Display.writeCenterPlus(Display.screen, "Anthill Search", LARGE_FONT_SIZE, -4 * LARGE_FONT_SIZE)
        instructions = ["Good luck!"]
        for i, instruction in enumerate(instructions):
            Display.writeCenterPlus(Display.screen, instruction, FONT_SIZE * 2, FONT_SIZE * 2 * i)

    def drawPage(self):
        page2 = pygame.image.load(self.pages[self.pageNumber])
        page2 = page2.convert_alpha()
        page2 = pygame.transform.scale(page2, (Display.origWidth, Display.origHeight))
        Display.screen.blit(page2, [0, 0])

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

    def drawPlayButton(self):
        Display.drawRect(Display.screen, BORDER_COLOR, self.playButton, 1, False)
        pygame.draw.polygon(Display.screen, WORDS_COLOR, [[self.playButton.left + 4, self.playButton.top + 4],
                                                          [self.playButton.right - 4, self.playButton.centery],
                                                          [self.playButton.left + 4, self.playButton.bottom - 4]])

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if self.playButton.collidepoint(pygame.mouse.get_pos()):
                    self.playPressed = True
                elif self.nextButton.collidepoint(pygame.mouse.get_pos()) and self.pageNumber < len(self.pages) - 1:
                    self.pageNumber += 1
                elif self.prevButton.collidepoint(pygame.mouse.get_pos()) and self.pageNumber > 0:
                    self.pageNumber -= 1
            elif event.type == QUIT:
                pygame.quit()
