from Constants import BORDER_COLOR
from display import Display
from display.buttons.Button import Button


class PlayButton(Button):

    def __init__(self, caller, x=-1, y=-1):
        if x == -1:
            x = Display.origWidth * 1 / 2 - 8
        if y == -1:
            y = Display.origHeight * 5 / 6 - 8
        super().__init__("Play", self.play, x, y)
        self.rect.width = 32
        self.rect.height = 32
        self.caller = caller

    def play(self):
        self.caller.play()

    def draw(self):
        if self.caller.pageNumber == len(self.caller.pages) - 1:
            Display.drawRect(Display.screen, BORDER_COLOR, self.rect, 1, False)
            Display.drawPolygon(Display.screen, self.color, [[self.rect.left + 4, self.rect.top + 4],
                                                             [self.rect.right - 4, self.rect.centery],
                                                             [self.rect.left + 4, self.rect.bottom - 4]], False)
