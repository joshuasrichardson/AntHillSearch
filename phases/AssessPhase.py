from Constants import ASSESS_COLOR, ASSESS
from phases.Phase import Phase


class AssessPhase(Phase):

    def getNumber(self):
        return ASSESS

    def toString(self):
        return "ASSESS"

    def getColor(self):
        return ASSESS_COLOR

    def getSpeed(self, uncommittedSpeed, committedSpeed):
        return uncommittedSpeed
