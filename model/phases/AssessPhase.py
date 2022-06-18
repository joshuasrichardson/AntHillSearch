from Constants import ASSESS_COLOR, ASSESS
from model.phases.Phase import Phase


class AssessPhase(Phase):
    """ The phase where the agent has found a site and are trying to determine whether they should
    accept it or not """

    def getNumber(self):
        return ASSESS

    def toString(self):
        return "ASSESS"

    def getColor(self):
        return ASSESS_COLOR
