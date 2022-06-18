from display import Display
from display.buttons.Button import Button


class PrevButton(Button):
    """ A button used to navigate to the previous screen of a paged menu """

    def __init__(self, caller, x=-1, y=-1):
        """ caller - the screen that owns this button, that will be moved to the previous screen when PREV is clicked
        x - the horizontal position of the left side of the button; 1/4 of the way across the screen if left at -1
        y - the vertical position of the top side of the button; 3/4 of the way down the screen if left at -1 """
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

    def collides(self, pos):
        return self.caller.pageNumber > 0 and super().collides(pos)
