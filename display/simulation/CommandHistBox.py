from Constants import TRANSPARENT, SIMPLIFY_STATES
from config import Config
from display import Display
from display.buttons.AdjustableBox import AdjustableBox


class CommandHistBox(AdjustableBox):
    """ A box that displays the commands that the user has executed and when they were executed. """

    def __init__(self):
        left = 20  # TODO: Don't hardcode these values
        top = int(Display.origHeight * 4 / 5)
        right = 410
        bottom = int(Display.origHeight * 19 / 20)
        width = right - left
        height = bottom - top
        super().__init__("Command History Box", left, top, width, height, 4, Config.FONT_SIZE, spacing=1, bgColor=TRANSPARENT)
        self.executedCommands = []
        self.shouldDraw = not SIMPLIFY_STATES

    def addExecutedCommand(self, command, time):
        command = '{:003d}'.format(int(time)) + ": " + command
        self.addMessage(command)
        self.executedCommands.append(command)
