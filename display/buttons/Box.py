from Constants import BORDER_COLOR, TRANSPARENT, SCREEN_COLOR
from config import Config
from display import Display
from display.buttons.Button import Button


class Box(Button):
    """ A button with a background and border """

    def __init__(self, name, action, x, y, w=0, h=0, fontSize=int(Config.FONT_SIZE * 1.5), bgColor=SCREEN_COLOR):
        """ name - the name of the box doesn't necessarily show up anywhere, but it can be used in debugging
         action - an action that is executed when the box is clicked
         x - the left position of the box
         y - the right position of the box
         w - the width of the box
         h - the height of the box
         fontSize - size of the words to be written in the box
         bgColor - the background color of the box """
        super().__init__(name, action, x, y, w, h, fontSize)
        self.bgColor = bgColor
        self.borderColor = BORDER_COLOR

    def draw(self):
        if self.bgColor != TRANSPARENT:
            Display.drawRect(Display.screen, self.bgColor, self.rect, adjust=False)
        Display.drawRect(Display.screen, self.borderColor, self.rect, width=1, adjust=False)
