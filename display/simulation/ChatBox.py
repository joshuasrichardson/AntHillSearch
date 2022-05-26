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
        super().__init__("Chat Box", left, top, width, height, 8, Config.FONT_SIZE * 4, 1.5)
        self.inputBox = None

    def setInput(self, inputBox):
        self.inputBox = inputBox
        self.setInputBounds()

    def setInputBounds(self):
        self.inputBox.setBounds(self.rect.left, self.rect.bottom - self.bottomPad + Config.FONT_SIZE / 2,
                                self.rect.right, self.rect.bottom)

    def setBoxTop(self, top):
        super().setBoxTop(top)
        self.inputBox.setTBound(self.rect.top + self.rect.height - self.bottomPad)

    def setBoxRight(self, right):
        super().setBoxRight(right)
        self.inputBox.setRBound(self.rect.right)

    def setBoxBottom(self, bottom):
        super().setBoxBottom(bottom)
        self.inputBox.setBBound(self.rect.bottom)

    def setBoxLeft(self, left):
        super().setBoxLeft(left)
        self.inputBox.setLBound(self.rect.left)

    def move(self, pos):
        relPos = [self.inputBox.rect.left - self.rect.left, self.inputBox.rect.top - self.rect.top]
        width = self.inputBox.rect.w
        super().move(pos)
        self.setInputBounds()
        self.inputBox.rect.left = self.rect.left + relPos[0]
        self.inputBox.rect.top = self.rect.top + relPos[1]
        self.inputBox.rect.w = width
