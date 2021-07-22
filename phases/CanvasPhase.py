from Constants import CANVAS_COLOR, CANVAS
from phases.Phase import Phase


class CanvasPhase(Phase):

    def getNumber(self):
        return CANVAS

    def toString(self):
        return "CANVAS"

    def getColor(self):
        return CANVAS_COLOR

    def getSpeed(self, uncommittedSpeed, committedSpeed, speedCoefficient):
        return uncommittedSpeed * speedCoefficient
