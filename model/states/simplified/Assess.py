from config import Config
from Constants import *
from model.states.State import State
from model.states.simplified.Dance import DanceState
from model.states.simplified.Explore import ExploreState


class AssessState(State):
    """ State where an agent is at a nest assessing """

    def __init__(self, agent):
        """ agent - the agent that is in this state """
        super().__init__(agent)
        self.stateNumber = ASSESS_STATE

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.getAssignedSitePosition())

        if self.agent.isDoneAssessing():
            self.acceptOrReject()
            return

        # Let the agent's estimated quality of the site get closer to the actual quality as they spend time at the site.
        if self.agent.estimatedQuality > self.agent.assignedSite.getQuality():
            self.agent.estimatedQuality = round(self.agent.estimatedQuality - 0.1, 1)
        else:
            self.agent.estimatedQuality = round(self.agent.estimatedQuality + 0.1, 1)

        # If the site moves, they might not know where it is
        if self.agent.siteInRangeIndex != -1 and self.agent.world.siteList[self.agent.siteInRangeIndex] is self.agent.assignedSite:
            self.agent.estimateSitePositionMoreAccurately()

    def acceptOrReject(self):
        # If they determine the site is good enough after they've been there long enough,
        if self.agent.estimatedQuality > Config.MIN_ACCEPT_VALUE:
            self.recruit()
        else:
            self.setState(ExploreState(self.agent), None)

    def recruit(self):
        self.setState(DanceState(self.agent), self.agent.getHub().getPosition())

    def toString(self):
        return "ASSESS"

    def getColor(self):
        return ASSESS_COLOR
