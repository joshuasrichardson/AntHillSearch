from Constants import COMMIT_COLOR, COMMIT
from phases.Phase import Phase


class CommitPhase(Phase):

    def getNumber(self):
        return COMMIT

    def toString(self):
        return "COMMIT"

    def getColor(self):
        return COMMIT_COLOR

    def getSpeed(self, uncommittedSpeed, committedSpeed):
        return committedSpeed
