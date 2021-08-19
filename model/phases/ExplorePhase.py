from Constants import EXPLORE_COLOR, EXPLORE
from model.phases.Phase import Phase


class ExplorePhase(Phase):
    """ The phase where agents start looking for a new site and haven't yet come into contact with any """

    def getNumber(self):
        return EXPLORE

    def toString(self):
        return "EXPLORE"

    def getColor(self):
        return EXPLORE_COLOR

    def getSpeed(self, uncommittedSpeed, committedSpeed, speedCoefficient):
        return uncommittedSpeed * speedCoefficient
