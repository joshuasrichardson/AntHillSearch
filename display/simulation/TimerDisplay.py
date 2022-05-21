from config import Config
from config.Config import FONT_SIZE
from display import Display


class TimerDisplay:
    def __init__(self, timer):
        self.timer = timer

    def drawRemainingTime(self):
        time = round(self.timer.getRemainingTimeOrRounds())
        if Config.USE_ROUNDS_AS_DURATION:
            time = f"{time}/{Config.SIM_DURATION}"
        Display.write(Display.screen, time, FONT_SIZE, Display.origWidth - 175, 30)
