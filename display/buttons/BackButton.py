from ColonyExceptions import BackException
from display.buttons.Button import Button


class BackButton(Button):
    """ A button used to return to a previous MenuScreen """

    def __init__(self, x=50, y=50):
        """ x - the left position of the back button on the screen
        y - the top position of the back button on the screen """
        super().__init__("<- BACK", self.back, x, y)

    def back(self):
        raise BackException()
