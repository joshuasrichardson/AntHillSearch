from Constants import BORDER_COLOR
from config import Config
from display import Display
from display.buttons.AdjustableBox import AdjustableBox


class ChatBox(AdjustableBox):

    def __init__(self):
        left = int(Display.origWidth * 3 / 4)
        top = int(Display.origHeight * 3 / 5)
        right = int(Display.origWidth * 29 / 30)
        bottom = int(Display.origHeight * 17 / 20)
        width = right - left
        height = bottom - top
        super().__init__("Chat Box", left, top, width, height, 8, Config.FONT_SIZE * 4, 1.5, minW=60, minH=60)
        self.inputBox = None

    def setInput(self, inputBox):
        self.inputBox = inputBox
        self.setInputBounds()

    def setInputBounds(self):
        self.inputBox.setBounds(self.rect.left + 6, self.rect.bottom - self.rect.height / 2,
                                self.rect.right - 6, self.rect.bottom - 6)

    def setBoxTop(self, top):
        super().setBoxTop(top)
        self.inputBox.setTBound(self.rect.top + self.rect.height / 2)
        diff = self.rect.bottom - 6 - self.inputBox.rect.bottom
        if diff < 0 and self.inputBox.rect.height > self.inputBox.minH:
            self.inputBox.rect.height += diff
        if self.inputBox.rect.height < 2 * Config.FONT_SIZE:
            self.inputBox.rect.top = self.rect.bottom - 6 - 2 * Config.FONT_SIZE
            self.inputBox.rect.height = 2 * Config.FONT_SIZE

    def setBoxRight(self, right):
        super().setBoxRight(right)
        self.inputBox.setRBound(self.rect.right)
        self.inputBox.rect.left = self.rect.left + 6
        self.inputBox.rect.w = self.rect.w - 12

    def setBoxBottom(self, bottom):
        super().setBoxBottom(bottom)
        self.inputBox.setBBound(self.rect.bottom)
        self.inputBox.rect.bottom = self.rect.bottom - 6
        self.bottomPad = self.inputBox.rect.h + 1.5 * Config.FONT_SIZE

    def setBoxLeft(self, left):
        super().setBoxLeft(left)
        self.inputBox.setLBound(self.rect.left)
        self.inputBox.rect.left = self.rect.left + 6
        self.inputBox.rect.w = self.rect.w - 12

    def move(self, pos):
        relPos = [self.inputBox.rect.left - self.rect.left, self.inputBox.rect.top - self.rect.top]
        width = self.inputBox.rect.w
        super().move(pos)
        self.setInputBounds()
        self.inputBox.rect.left = self.rect.left + relPos[0]
        self.inputBox.rect.top = self.rect.top + relPos[1]
        self.inputBox.rect.w = width

    def drawScrollDownArrow(self):
        Display.drawLine(Display.screen, BORDER_COLOR, [self.rect.right - 16, self.rect.bottom - self.bottomPad - 10],
                         [self.rect.right - 12, self.rect.bottom - self.bottomPad - 6], width=2, adjust=False)
        Display.drawLine(Display.screen, BORDER_COLOR, [self.rect.right - 12, self.rect.bottom - self.bottomPad - 6],
                         [self.rect.right - 8, self.rect.bottom - self.bottomPad - 10], width=2, adjust=False)
