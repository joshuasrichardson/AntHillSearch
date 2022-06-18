from config import Config
from display import Display
from display.buttons.Button import Button


class Title(Button):
    """ An object used to display a title """

    def __init__(self, name, y):
        """ name - the name of title
        y - the top vertical position of the title """
        super().__init__(name, lambda: None, 0, y)

    def draw(self):
        Display.writeCenterPlus(Display.screen, self.name, Config.LARGE_FONT_SIZE, -Display.origHeight / 2 + self.rect.top)
