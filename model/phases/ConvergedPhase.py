from Constants import CONVERGED_COLOR, CONVERGED
from model.phases.Phase import Phase


class ConvergedPhase(Phase):
    """ The phase where the agent simply stays at the new site because their colony's simulation is over.
    This can only be achieved for more than a split second when there are at least 2 colonies in the simulation. """

    def getNumber(self):
        return CONVERGED

    def toString(self):
        return "CONVERGED"

    def getColor(self):
        return CONVERGED_COLOR
