import random

from Constants import *
from config.Config import PROB_AD
from model.states.State import State
from model.states.simplified.Dance import DanceState


class AssessState(State):
    """ State where an agent is at a nest assessing """

    def __init__(self, agent):
        """ agent - the agent that is in this state """
        super().__init__(agent)
        self.stateNumber = ASSESS_STATE

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.getAssignedSitePosition())

        if random.uniform(0, 1) < PROB_AD:
            self.recruit()
            return

        # Let the agent's estimated quality of the site get closer to the actual quality as they spend time at the site.
        if self.agent.estimatedQuality > self.agent.assignedSite.getQuality():
            self.agent.estimatedQuality = round(self.agent.estimatedQuality - 0.1, 1)
        else:
            self.agent.estimatedQuality = round(self.agent.estimatedQuality + 0.1, 1)

    def recruit(self):
        self.setState(DanceState(self.agent), self.agent.getHub().getPosition())

    def toString(self):
        return "ASSESS"

    def getColor(self):
        return ASSESS_COLOR
