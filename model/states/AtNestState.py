import numpy as np

from Constants import *
from model.phases.CanvasPhase import CanvasPhase
from model.phases.CommitPhase import CommitPhase
from model.phases.ExplorePhase import ExplorePhase
from model.states.FollowState import FollowState
from model.states.LeadForwardState import LeadForwardState
from model.states.SearchState import SearchState
from model.states.State import State


class AtNestState(State):
    """ State where an agent is just at a nest, whether it is the original home, a nest they are assessing, or
    a nest they are recruiting to """

    def __init__(self, agent):
        super().__init__(agent)
        self.state = AT_NEST

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.getAssignedSitePosition())

        siteWithinRange = self.agent.getAgentRect().collidelist(self.agent.world.siteRectList)

        if siteWithinRange != -1 and self.agent.world.siteList[siteWithinRange].executeCommand(self.agent):
            return

        # checking the siteWithinRange makes sure they actually get to the site before they search again unless they get lost on the way.
        if self.agent.shouldSearch(siteWithinRange):
            self.setState(SearchState(self.agent), None)
            return

        if self.agent.getPhaseNumber() == ASSESS:
            if self.agent.isDoneAssessing():
                self.acceptOrReject()
                return

        if self.agent.getPhaseNumber() == CANVAS:
            if self.agent.shouldRecruit():
                self.setState(LeadForwardState(self.agent), self.agent.getAssignedSitePosition())
                return

        if self.agent.getPhaseNumber() == COMMIT:
            # Recruit, search, or follow
            if self.agent.shouldRecruit():
                self.agent.transportOrReverseTandem(self)
                return

        for i in range(0, len(neighborList)):
            if (neighborList[i].getState() == LEAD_FORWARD and neighborList[i].estimatedQuality > self.agent.estimatedQuality)\
                    or (neighborList[i].getState() == REVERSE_TANDEM and neighborList[i].estimatedQuality >= self.agent.estimatedQuality)\
                    and self.agent.shouldFollow():
                self.tryFollowing(neighborList[i])
                return

        # If an agent nearby is transporting, get carried by that agent.
        for i in range(0, len(neighborList)):
            if neighborList[i].getState() == TRANSPORT:
                self.getCarried(neighborList[i])
                return

        # Let the agent's estimated quality of the site get closer to the actual quality as they spend time at the site.
        if self.agent.estimatedQuality > self.agent.assignedSite.getQuality():
            self.agent.estimatedQuality = np.round(self.agent.estimatedQuality - 0.1, 1)
        else:
            self.agent.estimatedQuality = np.round(self.agent.estimatedQuality + 0.1, 1)

        # If the site moves, they might not know where it is
        if siteWithinRange != -1 and self.agent.world.siteList[siteWithinRange] is self.agent.assignedSite:
            self.agent.assignedSiteLastKnownPos = self.agent.assignedSite.getPosition()

    def tryFollowing(self, leader):
        if leader.numFollowers < MAX_FOLLOWERS:
            self.agent.leadAgent = leader
            self.agent.leadAgent.incrementFollowers()
            self.setState(FollowState(self.agent), self.agent.leadAgent.pos)

    def acceptOrReject(self):
        # If they determine the site is good enough after they've been there long enough,
        if self.agent.estimatedQuality > MIN_ACCEPT_VALUE:
            if self.agent.quorumMet():
                # enough agents are already at the site, so they skip canvasing and go straight to the committed phase
                self.agent.setPhase(CommitPhase())
                self.agent.transportOrReverseTandem(self)
            else:
                # they enter the canvasing phase and start recruiting others.
                self.agent.setPhase(CanvasPhase())
                from model.states.LeadForwardState import LeadForwardState
                self.setState(LeadForwardState(self.agent), self.agent.getAssignedSitePosition())
        else:
            self.agent.setPhase(ExplorePhase())
            from model.states.SearchState import SearchState
            self.setState(SearchState(self.agent), None)

    # TODO: If I keep this, I need to remove the repetition with SearchState
    def getCarried(self, transporter):
        if transporter.numFollowers < MAX_FOLLOWERS:
            self.agent.leadAgent = transporter
            self.agent.leadAgent.incrementFollowers()
            from model.states.CarriedState import CarriedState
            self.setState(CarriedState(self.agent), self.agent.leadAgent.pos)

    def toString(self):
        return "AT_NEST"

    def getColor(self):
        return AT_NEST_COLOR