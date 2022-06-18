from Constants import CANVAS_COLOR, CANVAS
from model.phases.Phase import Phase


class CanvasPhase(Phase):
    """ The phase where the agent has accepted a site but not yet met the quorum there """

    def getNumber(self):
        return CANVAS

    def toString(self):
        return "CANVAS"

    def getColor(self):
        return CANVAS_COLOR
