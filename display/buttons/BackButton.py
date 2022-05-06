from ColonyExceptions import BackException
from display.buttons.Button import Button


class BackButton(Button):

    def __init__(self, x=50, y=50):
        super().__init__("<- BACK", self.back, x, y)

    def back(self):
        raise BackException()
