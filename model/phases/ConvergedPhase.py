from Constants import CONVERGED_COLOR, CONVERGED
from model.phases.Phase import Phase


class ConvergedPhase(Phase):
    """ The phase where agents have met the quorum at their assigned site and are
    completely dedicated to it"""

    def getNumber(self):
        return CONVERGED

    def toString(self):
        return "CONVERGED"

    def getColor(self):
        return CONVERGED_COLOR
