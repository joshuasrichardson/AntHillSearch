from abc import ABC, abstractmethod


def numToPhase(num):
    from Constants import EXPLORE
    if num == EXPLORE:
        from phases.ExplorePhase import ExplorePhase
        return ExplorePhase()
    from Constants import ASSESS
    if num == ASSESS:
        from phases.AssessPhase import AssessPhase
        return AssessPhase()
    from Constants import CANVAS
    if num == CANVAS:
        from phases.CanvasPhase import CanvasPhase
        return CanvasPhase()
    from Constants import COMMIT
    if num == COMMIT:
        from phases.CommitPhase import CommitPhase
        return CommitPhase()


class Phase(ABC):

    @abstractmethod
    def getNumber(self):
        pass

    @abstractmethod
    def toString(self):
        pass

    @abstractmethod
    def getColor(self):
        pass

    @abstractmethod
    def getSpeed(self, uncommittedSpeed, committedSpeed):
        pass
