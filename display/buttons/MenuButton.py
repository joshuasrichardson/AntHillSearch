from config import Config
from display import Display
from display.buttons.Button import Button


class MenuButton(Button):
    """ A button representing a main menu option such as test, practice, or tutorial, that is drawn in the
    horizontal center of the screen """

    def __init__(self, option, action, y):
        """ option - the name of the button; the name of the action that will happen when the button is pressed
        action - the action that will execute when the button is pressed
        y - the vertical position of the top of the button on the screen """
        super().__init__(option, action, 0, y)

    def draw(self):
        self.rect = Display.writeCenterPlus(Display.screen, self.name, Config.FONT_SIZE * 2, self.y, self.color)
