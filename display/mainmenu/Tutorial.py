import pygame
from pygame import MOUSEBUTTONUP, QUIT, MOUSEMOTION

from ColonyExceptions import GameOver
from Constants import FONT_SIZE, LARGE_FONT_SIZE, WORDS_COLOR, BORDER_COLOR, SCREEN_COLOR
from display import Display


class Tutorial:

    def __init__(self, play):
        self.play = play

        self.playButton = pygame.Rect(Display.origWidth / 2 - FONT_SIZE, Display.origHeight * 3 / 4 + FONT_SIZE + (FONT_SIZE / 2), FONT_SIZE * 2, FONT_SIZE * 2)
        self.prevButton = pygame.Rect(0, 0, 0, 0)
        self.nextButton = pygame.Rect(0, 0, 0, 0)
        self.backButton = pygame.Rect(0, 0, 0, 0)

        self.mousePos = [0, 0]

        self.pageNumber = 0
        self.pages = []
        for page in range(2, 11):
            self.pages.append("resources/instructions/page" + str(page) + ".png")
        self.pages.append(None)

    def run(self):
        try:
            reading = True
            while reading:
                Display.screen.fill(SCREEN_COLOR)
                self.showInstructions()
                pygame.display.flip()
                reading = self.handleEvents()
        except GameOver:
            pass

    def showInstructions(self):
        if self.pageNumber == 0:
            self.drawPage1()
        elif self.pageNumber == len(self.pages) - 1:
            self.drawLastPage()
        else:
            self.drawPage()

    def drawPage1(self):
        Display.writeCenterPlus(Display.screen, "Anthill Search", LARGE_FONT_SIZE, -4 * LARGE_FONT_SIZE)
        instructions = ["The ants old home has been broken!",
                        "Your task is to help them find the ",
                        "best new home in the area."]
        for i, instruction in enumerate(instructions):
            Display.writeCenterPlus(Display.screen, instruction, FONT_SIZE * 2, FONT_SIZE * 2 * i)
        self.drawBackButton()
        self.drawNextButton()

    def drawPage(self):
        page2 = pygame.image.load(self.pages[self.pageNumber])
        page2 = page2.convert_alpha()
        page2 = pygame.transform.scale(page2, (Display.origWidth, Display.origHeight))
        Display.screen.blit(page2, [0, 0])
        self.drawBackButton()
        self.drawPreviousButton()
        self.drawNextButton()

    def drawLastPage(self):
        Display.writeCenterPlus(Display.screen, "Anthill Search", LARGE_FONT_SIZE, -4 * LARGE_FONT_SIZE)
        instructions = ["Good luck!"]
        for i, instruction in enumerate(instructions):
            Display.writeCenterPlus(Display.screen, instruction, FONT_SIZE * 2, FONT_SIZE * 2 * i)
        self.drawBackButton()
        self.drawPreviousButton()
        self.drawPlayButton()

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
                return self.mouseButtonPressed(pygame.mouse.get_pos())
            elif event.type == MOUSEMOTION:
                self.setMouse()
            elif event.type == QUIT:
                pygame.quit()
                raise GameOver("Game Over")
        return True

    def mouseButtonPressed(self, pos):
        self.mousePos = pos
        if self.playButton.collidepoint(pos):
            self.play()
            return False
        elif self.nextButton.collidepoint(pos) and self.pageNumber < len(self.pages) - 1:
            self.pageNumber += 1
        elif self.prevButton.collidepoint(pos) and self.pageNumber > 0:
            self.pageNumber -= 1
        elif self.backButton.collidepoint(pos):
            return False
        return True

    def setMouse(self):
        if self.collidesWithSelectable(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def collidesWithSelectable(self, pos):
        return self.playButton.collidepoint(pos) or \
                self.prevButton.collidepoint(pos) or \
                self.nextButton.collidepoint(pos) or \
                self.backButton.collidepoint(pos)
