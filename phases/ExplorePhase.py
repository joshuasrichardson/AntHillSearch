from Constants import EXPLORE_COLOR, EXPLORE
from phases.Phase import Phase


class ExplorePhase(Phase):

    def getNumber(self):
        return EXPLORE

    def toString(self):
        return "EXPLORE"

    def getColor(self):
        return EXPLORE_COLOR

    def getSpeed(self, uncommittedSpeed, committedSpeed):
        return uncommittedSpeed
