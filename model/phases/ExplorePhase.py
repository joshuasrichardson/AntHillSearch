from Constants import EXPLORE_COLOR, EXPLORE
from model.phases.Phase import Phase


class ExplorePhase(Phase):
    """ The phase where the agent starts looking for a new site and hasn't yet come into contact with any """

    def getNumber(self):
        return EXPLORE

    def toString(self):
        return "EXPLORE"

    def getColor(self):
        return EXPLORE_COLOR
