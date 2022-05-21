from Constants import BORDER_COLOR, TRANSPARENT, SCREEN_COLOR
from config import Config
from display import Display
from display.buttons.Button import Button


class Box(Button):

    def __init__(self, name, action, x, y, w=0, h=0, fontSize=int(Config.FONT_SIZE * 1.5), screen=None, bgColor=SCREEN_COLOR):
        super().__init__(name, action, x, y, w, h, fontSize, screen)
        self.bgColor = bgColor
        self.borderColor = BORDER_COLOR

    def draw(self):
        if self.bgColor != TRANSPARENT:
            Display.drawRect(Display.screen, self.bgColor, self.rect, adjust=False)
        Display.drawRect(Display.screen, self.borderColor, self.rect, width=1, adjust=False)
