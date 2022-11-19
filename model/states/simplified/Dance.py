import random

import numpy as np
from pygame import Rect

from Constants import *
from config.Config import PROB_DA
from model.states.State import State


class DanceState(State):
    """ Abstract state where agents recruit other agents to come to their assigned site """

    def __init__(self, agent):
        """ agent - the agent that is in this state """
        super().__init__(agent)
        self.stateNumber = DANCE_STATE
        self.agent.goingToRecruit = True

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.getHub().getPosition())

        base = 5.0
        pwr = -1.0
        qual = self.agent.assignedSite.getQuality() / 255
        dance_to_rest = np.power(base, pwr * qual)
        dance_to_rest /= 4
        if random.uniform(0, 1) < dance_to_rest:
            from model.states.simplified.Rest import RestState
            self.setState(RestState(self.agent), self.agent.getHub().getPosition())
            return

        if random.uniform(0, 1) < PROB_DA:
            from model.states.simplified.Rest import AssessState
            self.setState(AssessState(self.agent), self.agent.getAssignedSitePosition())
            return

        if self.agent.goingToRecruit:  # if they are on the way to go recruit someone, they keep going until they get there.
            if self.arrivedAtOrPassedSite(self.agent.getHub().getPosition()):  # If agent finds the old site
                self.agent.goingToRecruit = False  # The agent is now going to head back to the new site

    def arrivedAtOrPassedSite(self, sitePos):
        if self.agent.getRect().collidepoint(sitePos):
            return True
        if self.agent.prevPos[0] < self.agent.pos[0]:
            left = self.agent.prevPos[0]
        else:
            left = self.agent.pos[0]
        if self.agent.prevPos[1] < self.agent.pos[1]:
            top = self.agent.prevPos[1]
        else:
            top = self.agent.pos[1]
        rect = Rect(left, top, self.agent.speed, self.agent.speed)
        return rect.collidepoint(sitePos)

    def toString(self):
        return "DANCE"

    def getColor(self):
        return DANCE_STATE_COLOR
