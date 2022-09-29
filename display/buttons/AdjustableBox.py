from math import isclose

from numpy import inf

from Constants import SCREEN_COLOR, BORDER_COLOR
from config import Config
from display import Display
from display.buttons.Box import Box

MIN_LEN = 20


class AdjustableBox(Box):
    """ A box that can be moved around, resized, and written on. """

    def __init__(self, name, x, y, w, h, topPad, bottomPad, spacing=0.4, bgColor=SCREEN_COLOR, action=None,
                 minW=MIN_LEN, minH=MIN_LEN):
        """ name - the name of the box doesn't necessarily show up anywhere, but it can be used in debugging
         x - the left position of the box
         y - the right position of the box
         w - the width of the box
         h - the height of the box
         topPad - how much space to leave between the top of the box and the first words
         bottomPad - how much space to leave between the bottom of the box and the last words
         spacing - how much space to put between each line of words in the box
         bgColor - the background color of the box
         action - an action that is executed when the box is clicked
         minW - the smallest the width can be adjusted to
         minH - the smallest the height of the box can be adjusted to """
        if action is None:
            def action(): self.mouseButtonUp(0)
        super().__init__(name, action, x, y, w, h, bgColor=bgColor)
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
        self.topPad = topPad
        self.bottomPad = bottomPad
        self.spacing = spacing
        self.minL = -inf
        self.minT = -inf
        self.maxR = inf
        self.maxB = inf
        self.minW = minW
        self.minH = minH
        self.shouldDraw = True

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
        return self.dragging or self.resizing()

    def resizing(self):
        return self.resizingTop or self.resizingRight or self.resizingBottom or self.resizingLeft

    def mouseButtonUp(self, _):
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
            self.move(pos)

    def move(self, pos):
        self.rect.center = pos
        for i in range(len(self.messagePositions)):
            if i == 0:
                self.messagePositions[i] = [self.rect.x + 10, self.rect.y + self.topPad + self.dy]
            else:
                prevPos = self.messagePositions[i - 1]
                self.messagePositions[i] = [prevPos[0], prevPos[1] + self.bottomMargins[i - 1]]
        self.enforceBounds()

    def draw(self):
        if not self.shouldDraw:
            return
        super().draw()
        for i, message in enumerate(self.lines):
            if self.rect.top < self.messagePositions[i][1] < self.rect.bottom - self.bottomPad:
                Display.write(Display.screen, message, Config.FONT_SIZE,
                              self.messagePositions[i][0], self.messagePositions[i][1])
        if len(self.messagePositions) > 0:
            if self.rect.top > self.messagePositions[0][1]:
                self.drawScrollUpArrow()
            if self.messagePositions[len(self.messagePositions) - 1][1] > self.rect.bottom - self.bottomPad:
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
            while img.get_width() > self.rect.w * 1.4:
                nextLine = lines[len(lines) - 1][len(lines[len(lines) - 1]) - 1] + nextLine
                lines[len(lines) - 1] = lines[len(lines) - 1][:len(lines[len(lines) - 1]) - 1]
                img = self.font.render(lines[len(lines) - 1], True, self.color).convert_alpha()
            lines.append(nextLine)
            img = self.font.render(lines[len(lines) - 1], True, self.color)
            if img.get_width() <= self.rect.w * 1.4:
                allLinesFit = True

        return lines

    def spaceLines(self, lines):
        self.lines += lines
        for i in range(len(lines)):
            self.spaceLine(i)

    def spaceLine(self, i):
        if i == len(self.lines) - 1:
            self.bottomMargins.append(Config.FONT_SIZE * self.spacing)
        else:
            self.bottomMargins.append(Config.FONT_SIZE)
        if len(self.messagePositions) > 0:
            prevPos = self.messagePositions[len(self.messagePositions) - 1]
            self.messagePositions.append([prevPos[0], prevPos[1] + self.bottomMargins[len(self.bottomMargins) - 2]])
        else:
            self.messagePositions.append([self.rect.x + 10, self.rect.y + self.topPad])

    def repositionLines(self):
        while self.messagePositions[len(self.messagePositions) - 1][1] >= self.rect.bottom - self.bottomPad:
            self.scrollDown()

    def repositionParagraphs(self):
        self.clearFormat()
        for paragraph in self.paragraphs:
            lines = self.separateIntoLines(paragraph)
            self.spaceLines(lines)
            self.repositionLines()

    def clearFormat(self):
        self.lines = []
        self.messagePositions = []
        self.bottomMargins = []

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
        if self.rect.bottom - top > self.minH:
            if top < self.minT:
                top = self.minT
            self.rect.height = self.rect.bottom - top
            self.rect.top = top
            self.repositionParagraphs()

    def setBoxRight(self, right):
        if right - self.rect.left > self.minW:
            if right > self.maxR:
                right = self.maxR
            self.rect.width = right - self.rect.left
            self.repositionParagraphs()

    def setBoxBottom(self, bottom):
        if bottom - self.rect.top > self.minH:
            if bottom > self.maxB:
                bottom = self.maxB
            self.rect.height = bottom - self.rect.top
            self.repositionParagraphs()

    def setBoxLeft(self, left):
        if self.rect.right - left > self.minW:
            if left < self.minL:
                left = self.minL
            self.rect.width = self.rect.right - left
            self.rect.left = left
            self.repositionParagraphs()

    def setBounds(self, left, top, right, bottom):
        self.setLBound(left)
        self.setTBound(top)
        self.setRBound(right)
        self.setBBound(bottom)

    def setLBound(self, left):
        if self.maxR - left < self.minW:
            left = self.maxR - self.minW
        self.minL = int(left)
        self.enforceLeftBound()

    def setTBound(self, top):
        if self.maxB - top < self.minH:
            top = self.maxB - self.minH
        self.minT = int(top)
        self.enforceTopBound()

    def setRBound(self, right):
        if right - self.minL < self.minW:
            right = self.minL + self.minW
        self.maxR = int(right)
        self.enforceRightBound()

    def setBBound(self, bottom):
        if bottom - self.minT < self.minH:
            bottom = self.minT + self.minH
        self.maxB = int(bottom)
        self.enforceBottomBound()

    def enforceBounds(self):
        self.enforceLeftBound()
        self.enforceTopBound()
        self.enforceRightBound()
        self.enforceBottomBound()
        self.enforceWidthBound()
        self.enforceHeightBound()

    def enforceLeftBound(self):
        if self.rect.left < self.minL:
            self.rect.left = self.minL
            if self.rect.right > self.maxR:
                self.rect.width = self.maxR - self.minL

    def enforceTopBound(self):
        if self.rect.top < self.minT:
            self.rect.top = self.minT

    def enforceRightBound(self):
        if self.rect.right > self.maxR:
            self.rect.right = self.maxR
            self.enforceLeftBound()

    def enforceBottomBound(self):
        if self.rect.bottom > self.maxB:
            self.rect.bottom = self.maxB

    def enforceWidthBound(self):
        if self.rect.width < self.minW:
            self.rect.width = self.minW

    def enforceHeightBound(self):
        if self.rect.height < self.minH:
            self.rect.height = self.minH
