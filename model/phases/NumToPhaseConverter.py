from Constants import EXPLORE, ASSESS, CANVAS, COMMIT, CONVERGED


def numToPhase(num):
    """ Returns the phase associated with the given number """
    if num == EXPLORE:
        from model.phases.ExplorePhase import ExplorePhase
        return ExplorePhase()
    if num == ASSESS:
        from model.phases.AssessPhase import AssessPhase
        return AssessPhase()
    if num == CANVAS:
        from model.phases.CanvasPhase import CanvasPhase
        return CanvasPhase()
    if num == COMMIT:
        from model.phases.CommitPhase import CommitPhase
        return CommitPhase()
    if num == CONVERGED:
        from model.phases.ConvergedPhase import ConvergedPhase
        return ConvergedPhase()
