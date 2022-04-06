from display import Display
from display.mainmenu.buttons.Button import Button


class PrevButton(Button):

    def __init__(self, caller, x=-1, y=-1):
        if x == -1:
            x = Display.origWidth * 1 / 4
        if y == -1:
            y = Display.origHeight * 3 / 4
        super().__init__("< PREV", self.prev, x, y)
        self.caller = caller

    def draw(self):
        if self.caller.pageNumber > 0:
            super().draw()

    def prev(self):
        if self.caller.pageNumber > 0:
            self.caller.pageNumber -= 1
