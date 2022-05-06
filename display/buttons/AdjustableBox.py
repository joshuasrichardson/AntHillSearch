from math import isclose

import pygame

from Constants import SCREEN_COLOR, BORDER_COLOR, TRANSPARENT
from config import Config
from display import Display
from display.buttons.Button import Button


MIN_LEN = 20


class MovableBox(Button):

    def __init__(self, name, x, y, w, h, bottomPadding, spacing=0.4, bgColor=SCREEN_COLOR, action=lambda: None):
        super().__init__(name, action, x, y, w, h)
        self.dragging = False
        self.resizingTop = False
        self.resizingRight = False
        self.resizingBottom = False
        self.resizingLeft = False
        self.paragraphs = []
        self.lines = []
        self.messagePositions = []
        self.bottomMargins = []
        self.dy = 0
        self.bottomPadding = bottomPadding
        self.spacing = spacing
        self.bgColor = bgColor

    def mouseButtonDown(self, pos):
        if self.collidesTop(pos):
            self.resizingTop = True
        if self.collidesRight(pos):
            self.resizingRight = True
        if self.collidesBottom(pos):
            self.resizingBottom = True
        if self.collidesLeft(pos):
            self.resizingLeft = True
        if self.collides(pos) and not self.resizing():
            self.dragging = True

    def resizing(self):
        return self.resizingTop or self.resizingRight or self.resizingBottom or self.resizingLeft

    def mouseButtonUp(self, pos):
        self.dragging = False
        self.resizingTop = False
        self.resizingRight = False
        self.resizingBottom = False
        self.resizingLeft = False

    def update(self, pos):
        super().update(pos)
        if self.resizingTop:
            self.setBoxTop(pos[1])
        if self.resizingRight:
            self.setBoxRight(pos[0])
        if self.resizingBottom:
            self.setBoxBottom(pos[1])
        if self.resizingLeft:
            self.setBoxLeft(pos[0])
        if self.dragging:
            self.rect.center = pos
            for i in range(len(self.messagePositions)):
                if i == 0:
                    self.messagePositions[i] = [self.rect.x + 10, self.rect.y + 10 + self.dy]
                else:
                    prevPos = self.messagePositions[i - 1]
                    self.messagePositions[i] = [prevPos[0], prevPos[1] + self.bottomMargins[i - 1]]

    def draw(self):
        if self.bgColor != TRANSPARENT:
            Display.drawRect(Display.screen, self.bgColor, self.rect, adjust=False)
        Display.drawRect(Display.screen, BORDER_COLOR, self.rect, width=1, adjust=False)
        for i, message in enumerate(self.lines):
            if self.rect.top < self.messagePositions[i][1] < self.rect.bottom - self.bottomPadding:
                Display.write(Display.screen, message, Config.FONT_SIZE,
                              self.messagePositions[i][0], self.messagePositions[i][1])
        if len(self.messagePositions) > 0:
            if self.rect.top > self.messagePositions[0][1]:
                self.drawScrollUpArrow()
            if self.messagePositions[len(self.messagePositions) - 1][1] > self.rect.bottom - self.bottomPadding:
                self.drawScrollDownArrow()

    def isOnHorizEdge(self, pos):
        return self.collidesTop(pos) or self.collidesBottom(pos)

    def collidesTop(self, pos):
        return isclose(pos[1], self.rect.y, abs_tol=4) \
               and self.rect.x < pos[0] < self.rect.x + self.rect.w

    def collidesBottom(self, pos):
        return isclose(pos[1], self.rect.y + self.rect.h, abs_tol=4) \
               and self.rect.x < pos[0] < self.rect.x + self.rect.w

    def isOnVertEdge(self, pos):
        return self.collidesLeft(pos) or self.collidesRight(pos)

    def collidesLeft(self, pos):
        return isclose(pos[0], self.rect.x, abs_tol=4) \
               and self.rect.y < pos[1] < self.rect.y + self.rect.h

    def collidesRight(self, pos):
        return isclose(pos[0], self.rect.x + self.rect.w, abs_tol=4) \
               and self.rect.y < pos[1] < self.rect.y + self.rect.h

    def addMessage(self, words):
        self.paragraphs.append(words)
        lines = self.separateIntoLines(words)
        self.spaceLines(lines)
        self.repositionLines()

    def separateIntoLines(self, words):
        lines = [words]
        allLinesFit = False
        while not allLinesFit:
            img = self.font.render(lines[len(lines) - 1], True, self.color)
            nextLine = ""
            while img.get_width() > self.rect.w:
                nextLine = lines[len(lines) - 1][len(lines[len(lines) - 1]) - 1] + nextLine
                lines[len(lines) - 1] = lines[len(lines) - 1][:len(lines[len(lines) - 1]) - 1]
                img = self.font.render(lines[len(lines) - 1], True, self.color).convert_alpha()
            lines.append(nextLine)
            img = self.font.render(lines[len(lines) - 1], True, self.color)
            if img.get_width() <= self.rect.w:
                allLinesFit = True

        return lines

    def spaceLines(self, lines):
        for i, line in enumerate(lines):
            self.lines.append(line)
            if i == len(lines) - 1:
                self.bottomMargins.append(Config.FONT_SIZE * self.spacing)
            else:
                self.bottomMargins.append(Config.FONT_SIZE)
            if len(self.messagePositions) > 0:
                prevPos = self.messagePositions[len(self.messagePositions) - 1]
                self.messagePositions.append([prevPos[0], prevPos[1] + self.bottomMargins[len(self.bottomMargins) - 2]])
            else:
                self.messagePositions.append([self.rect.x + 10, self.rect.y + 10])

    def repositionLines(self):
        while self.messagePositions[len(self.messagePositions) - 1][1] >= self.rect.bottom - self.bottomPadding:
            self.scrollDown()

    def repositionParagraphs(self):
        self.lines = []
        self.messagePositions = []
        self.bottomMargins = []
        for paragraph in self.paragraphs:
            lines = self.separateIntoLines(paragraph)
            self.spaceLines(lines)
            self.repositionLines()

    def scrollDown(self):
        self.messagePositions = [[pos[0], pos[1] - Config.FONT_SIZE] for pos in self.messagePositions]
        self.dy -= Config.FONT_SIZE

    def scrollUp(self):
        self.messagePositions = [[pos[0], pos[1] + Config.FONT_SIZE] for pos in self.messagePositions]
        self.dy += Config.FONT_SIZE

    def drawScrollUpArrow(self):
        Display.drawLine(Display.screen, BORDER_COLOR, [self.rect.right - 16, self.rect.top + 10],
                         [self.rect.right - 12, self.rect.top + 6], width=2, adjust=False)
        Display.drawLine(Display.screen, BORDER_COLOR, [self.rect.right - 12, self.rect.top + 6],
                         [self.rect.right - 8, self.rect.top + 10], width=2, adjust=False)

    def drawScrollDownArrow(self):
        Display.drawLine(Display.screen, BORDER_COLOR, [self.rect.right - 16, self.rect.bottom - 10],
                         [self.rect.right - 12, self.rect.bottom - 6], width=2, adjust=False)
        Display.drawLine(Display.screen, BORDER_COLOR, [self.rect.right - 12, self.rect.bottom - 6],
                         [self.rect.right - 8, self.rect.bottom - 10], width=2, adjust=False)

    def setBoxTop(self, top):
        if self.rect.bottom - top > MIN_LEN:
            self.rect = pygame.Rect(self.rect.left, top, self.rect.width, self.rect.bottom - top)
            self.repositionParagraphs()

    def setBoxRight(self, right):
        if right - self.rect.left > MIN_LEN:
            self.rect = pygame.Rect(self.rect.left, self.rect.top, right - self.rect.left, self.rect.height)
            self.repositionParagraphs()

    def setBoxBottom(self, bottom):
        if bottom - self.rect.top > MIN_LEN:
            self.rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, bottom - self.rect.top)
            self.repositionParagraphs()

    def setBoxLeft(self, left):
        if self.rect.right - left > MIN_LEN:
            self.rect = pygame.Rect(left, self.rect.top, self.rect.right - left, self.rect.height)
            self.repositionParagraphs()
