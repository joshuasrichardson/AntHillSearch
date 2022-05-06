from config import Config
from display import Display
from display.buttons.Button import Button


class Title(Button):

    def __init__(self, words, y):
        super().__init__(words, lambda: None, 0, y)
        self.words = words

    def draw(self):
        Display.writeCenterPlus(Display.screen, self.words, Config.LARGE_FONT_SIZE, -Display.origHeight / 2 + self.rect.top)
