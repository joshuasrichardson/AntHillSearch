from Constants import ASSESS_COLOR, ASSESS
from phases.Phase import Phase


class AssessPhase(Phase):
    """ The phase where agents have found a site and are trying to determine whether they should
    accept it or not """

    def getNumber(self):
        return ASSESS

    def toString(self):
        return "ASSESS"

    def getColor(self):
        return ASSESS_COLOR

    def getSpeed(self, uncommittedSpeed, committedSpeed, speedCoefficient):
        return uncommittedSpeed * speedCoefficient
