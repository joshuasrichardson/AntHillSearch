from config import Config
from Constants import BORDER_COLOR, ACTIVE_COLOR
from display import Display
from display.mainmenu.buttons.SelectorButton import SelectorButton


class InputButton(SelectorButton):
    def __init__(self, x, y, w, h, selector):
        self.typing = False
        super().__init__("", "", x, y, selector, action=self.receiveInput)
        self.rect.w = w
        self.rect.h = h
        self.borderColor = BORDER_COLOR

    def draw(self):
        super().draw()
        Display.drawRect(Display.screen, self.borderColor, self.rect, width=1, adjust=False)
        Display.write(Display.screen, self.optionValue, Config.FONT_SIZE, self.rect.x + 10, self.rect.y)

    def changeColor(self, color):
        self.borderColor = ACTIVE_COLOR if self.typing else color

    def receiveInput(self):
        self.typing = True
        self.changeColor(ACTIVE_COLOR)

    def type(self, character):
        self.optionValue += character

    def backspace(self):
        self.optionValue = self.optionValue[:len(self.optionValue) - 1]

    def escape(self):
        self.typing = False

    def enter(self):
        self.selector.send(self.optionValue)
        self.optionValue = ""
        self.typing = False
        self.changeColor(BORDER_COLOR)
