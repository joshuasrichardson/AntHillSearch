from abc import ABC, abstractmethod

from Constants import CONVERGED


def numToPhase(num):
    """ Returns the phase associated with the given number """
    from Constants import EXPLORE
    if num == EXPLORE:
        from model.phases.ExplorePhase import ExplorePhase
        return ExplorePhase()
    from Constants import ASSESS
    if num == ASSESS:
        from model.phases.AssessPhase import AssessPhase
        return AssessPhase()
    from Constants import CANVAS
    if num == CANVAS:
        from model.phases.CanvasPhase import CanvasPhase
        return CanvasPhase()
    from Constants import COMMIT
    if num == COMMIT:
        from model.phases.CommitPhase import CommitPhase
        return CommitPhase()
    if num == CONVERGED:
        from model.phases.ConvergedPhase import ConvergedPhase
        return ConvergedPhase()


class Phase(ABC):
    """ Agent phases or levels of commitment on their way to finding the best new site """

    @abstractmethod
    def getNumber(self):
        pass

    @abstractmethod
    def toString(self):
        pass

    @abstractmethod
    def getColor(self):
        pass

    def getSpeed(self, uncommittedSpeed, committedSpeed, speedCoefficient):
        return uncommittedSpeed * speedCoefficient
