from Constants import COMMIT_COLOR, COMMIT
from model.phases.Phase import Phase


class CommitPhase(Phase):
    """ The phase where the agent has met the quorum at their assigned site and is
    completely dedicated to it. """

    def getNumber(self):
        return COMMIT

    def toString(self):
        return "COMMIT"

    def getColor(self):
        return COMMIT_COLOR

    def getSpeed(self, uncommittedSpeed, committedSpeed, speedCoefficient):
        return committedSpeed * speedCoefficient
