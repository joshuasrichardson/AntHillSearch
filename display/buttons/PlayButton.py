from pygame import Rect

from Constants import BORDER_COLOR
from display import Display
from display.buttons.Button import Button


class PlayButton(Button):

    def __init__(self, caller, x=-1, y=-1, canPause=True):
        if x == -1:
            x = Display.origWidth * 1 / 2 - 8
        if y == -1:
            y = Display.origHeight * 5 / 6 - 8
        super().__init__("Play", self.playOrPause, x, y)
        self.rect.width = 32
        self.rect.height = 32
        self.caller = caller
        self.canPause = canPause
        self.isPaused = False

    def playOrPause(self):
        if self.isPaused or not self.canPause:
            self.isPaused = False
            self.caller.play()
        else:
            self.isPaused = True
            self.caller.pause()

    def draw(self):
        if self.caller.shouldDrawPlayButton():
            Display.drawRect(Display.screen, BORDER_COLOR, self.rect, 1, False)
            if self.isPaused or not self.canPause:  # Draw play button
                Display.drawPolygon(Display.screen, self.color, [[self.rect.left + 4, self.rect.top + 4],
                                    [self.rect.right - 4, self.rect.centery],
                                    [self.rect.left + 4, self.rect.bottom - 4]], False)
            else:  # Draw pause button
                Display.drawRect(Display.screen, self.color,
                                 Rect(self.rect.left + self.rect.width / 6, self.rect.top + 3,
                                      self.rect.width / 4, self.rect.height - 6),
                                 adjust=False)
                Display.drawRect(Display.screen, self.color,
                                 Rect(self.rect.left + self.rect.width * 5 / 6 - self.rect.width / 4,  self.rect.top + 3,
                                      self.rect.width / 4, self.rect.height - 6),
                                 adjust=False)
