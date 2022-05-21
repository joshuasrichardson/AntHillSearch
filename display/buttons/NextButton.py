from display import Display
from display.buttons.Button import Button


class NextButton(Button):

    def __init__(self, caller, x=-1, y=-1):
        if x == -1:
            x = Display.origWidth * 3 / 4
        if y == -1:
            y = Display.origHeight * 3 / 4
        super().__init__("NEXT >", self.next, x, y)
        self.caller = caller

    def draw(self):
        if self.caller.pageNumber < self.caller.getNumPages() - 1:
            super().draw()

    def next(self):
        if self.caller.pageNumber < self.caller.getNumPages() - 1:
            self.caller.pageNumber += 1

    def collides(self, pos):
        return self.caller.pageNumber < self.caller.getNumPages() - 1 and super().collides(pos)
