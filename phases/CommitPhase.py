from Constants import COMMIT_COLOR, COMMIT
from phases.Phase import Phase


class CommitPhase(Phase):
    """ The phase where agents have met the quorum at their assigned site and are
    completely dedicated to it"""

    def getNumber(self):
        return COMMIT

    def toString(self):
        return "COMMIT"

    def getColor(self):
        return COMMIT_COLOR

    def getSpeed(self, uncommittedSpeed, committedSpeed, speedCoefficient):
        return committedSpeed * speedCoefficient
