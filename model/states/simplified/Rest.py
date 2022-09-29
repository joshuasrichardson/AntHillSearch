from Constants import *
from model.states.State import State
from model.states.simplified.Explore import ExploreState


class RestState(State):
    """ State where an agent is just at the hub resting """

    def __init__(self, agent):
        """ agent - the agent that is in this state """
        super().__init__(agent)
        self.stateNumber = REST_STATE

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.getHub().getPosition())

        # Checking the siteWithinRange makes sure they actually get to the site before they search again unless they get lost on the way.
        if self.agent.shouldSearch(self.agent.siteInRangeIndex):
            self.setState(ExploreState(self.agent), None)
            return

        for i in range(0, len(neighborList)):
            neighborState = neighborList[i].getStateNumber()
            if neighborState == DANCE_STATE and self.agent.shouldFollowDance():
                self.agent.assignSite(neighborList[i].assignedSite)
                from model.states.simplified.Assess import AssessState
                self.setState(AssessState(self.agent), self.agent.getAssignedSitePosition())
                return

    def toString(self):
        return "REST"

    def getColor(self):
        return REST_STATE_COLOR
