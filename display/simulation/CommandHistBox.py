from Constants import TRANSPARENT
from config import Config
from display import Display
from display.buttons.AdjustableBox import MovableBox


class CommandHistBox(MovableBox):

    def __init__(self):
        left = 20  # TODO: Don't hardcode these values
        top = int(Display.origHeight * 4 / 5)
        right = 400
        bottom = int(Display.origHeight * 19 / 20)
        width = right - left
        height = bottom - top
        super().__init__("Command History Box", left, top, width, height, Config.FONT_SIZE, bgColor=TRANSPARENT)
        self.executedCommands = []

    def addExecutedCommand(self, command, time):
        self.addMessage('{:003d}'.format(int(time)) + ": " + command)
