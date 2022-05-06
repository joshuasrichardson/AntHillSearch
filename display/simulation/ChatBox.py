from config import Config
from display import Display
from display.buttons.AdjustableBox import MovableBox


class ChatBox(MovableBox):

    def __init__(self):
        left = int(Display.origWidth * 2 / 3)
        top = int(Display.origHeight * 3 / 5)
        right = int(Display.origWidth * 11 / 12)
        bottom = int(Display.origHeight * 17 / 20)
        width = right - left
        height = bottom - top
        super().__init__("Chat Box", left, top, width, height, Config.FONT_SIZE * 4, 1.5)
