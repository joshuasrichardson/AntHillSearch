from config import Config
from config.Config import FONT_SIZE
from display import Display


class TimerDisplay:
    """ A display used to show how much time is left in the simulation """

    def __init__(self, timer):
        """ timer - the time with the time to be displayed """
        self.timer = timer

    def drawRemainingTime(self):
        time = round(self.timer.getRemainingTimeOrRounds())
        if Config.USE_ROUNDS_AS_DURATION:
            time = f"{time}/{Config.SIM_DURATION}"
        Display.write(Display.screen, time, FONT_SIZE, Display.origWidth - 175, 30)
