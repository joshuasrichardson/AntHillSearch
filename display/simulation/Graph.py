from pygame import Rect

from Constants import WORDS_COLOR
from config import Config
from display import Display
from display.buttons.AdjustableBox import AdjustableBox


class Graph(AdjustableBox):
    def __init__(self, title, categories, counts, maxCount, colors, left, top):
        self.title = title
        self.categories = categories
        self.counts = counts
        self.colors = colors
        super().__init__(title, left, top, maxCount + 110, (len(counts) + 2) * Config.FONT_SIZE, 0, 0)

    def draw(self):
        super().draw()
        Display.write(Display.screen, self.title, Config.FONT_SIZE, self.rect.left + 3, self.rect.top)

        left = self.rect.left + 100
        height = Config.FONT_SIZE

        for i, category in enumerate(self.categories):
            Display.write(Display.screen, category, Config.FONT_SIZE, self.rect.left + 3,
                          self.rect.top + (i + 1) * Config.FONT_SIZE + 2)

            top = self.rect.top + (i + 1) * Config.FONT_SIZE + 7
            width = self.counts[i] + 2
            Display.drawRect(Display.screen, WORDS_COLOR, Rect(left, top, width, height), adjust=False)
            Display.drawRect(Display.screen, self.colors[i], Rect(left + 1, top + 1, width - 2, height - 2),
                             adjust=False)
