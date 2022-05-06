from config import Config
from display import Display
from display.buttons.Button import Button


class MenuButton(Button):

    def __init__(self, action, option, y):
        super().__init__(option, action, 0, y)
        self.option = option

    def draw(self):
        self.rect = Display.writeCenterPlus(Display.screen, self.option, Config.FONT_SIZE * 2, self.y, self.color)
