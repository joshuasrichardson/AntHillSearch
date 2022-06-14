from pygame import K_RETURN, K_BACKSPACE, K_ESCAPE

from Constants import BORDER_COLOR, ACTIVE_COLOR, TRANSPARENT
from display.buttons.AdjustableBox import AdjustableBox


class InputButton(AdjustableBox):
    def __init__(self, x, y, w, h, receiver):
        super().__init__("Input", x, y, w, h, 2, 11, 0.4, TRANSPARENT, action=self.receiveInput)
        self.typing = False
        self.paragraphs = []
        self.receiver = receiver

    def changeColor(self, color):
        self.borderColor = ACTIVE_COLOR if self.typing else color

    def receiveInput(self):
        self.typing = True
        self.changeColor(ACTIVE_COLOR)
        if len(self.paragraphs) == 0:
            self.paragraphs.append("")
        self.dragging = False

    def input(self, event):
        if self.typing:
            if event.key == K_RETURN:
                self.enter()
            elif event.key == K_BACKSPACE:
                self.backspace()
            elif event.key == K_ESCAPE:
                self.escape()
            else:
                self.type(event.unicode)

    def type(self, character):
        self.paragraphs[0] += character
        self.repositionParagraphs()

    def backspace(self):
        self.paragraphs[0] = self.paragraphs[0][:-1]
        if len(self.lines[-1]) == 0 and len(self.lines) > 1:
            self.lines.pop(-1)
        self.lines[-1] = self.lines[-1][:-1]

    def escape(self):
        self.typing = False

    def enter(self):
        self.receiver.addMessage(f"User: {self.paragraphs[0]}")
        self.paragraphs = []
        self.clearFormat()
        self.typing = False
        self.changeColor(BORDER_COLOR)

    def move(self, _):
        pass
