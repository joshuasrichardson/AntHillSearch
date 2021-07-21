import numpy as np

from Constants import *
from phases.CanvasPhase import CanvasPhase
from phases.CommitPhase import CommitPhase
from phases.ExplorePhase import ExplorePhase
from states.FollowState import FollowState
from states.LeadForwardState import LeadForwardState
from states.SearchState import SearchState
from states.State import State


class AtNestState(State):
    """ State where an agent is just at a nest, whether it is the original home, a nest they are assessing, or
    a nest they are recruiting to """

    def __init__(self, agent):
        super().__init__(agent)
        self.state = AT_NEST

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.assignedSite.getPosition())

        siteWithinRange = self.agent.getAgentRect().collidelist(self.agent.world.siteRectList)
        # checking the siteWithinRange makes sure they actually get to the site before they search again unless they get lost on the way.
        if self.agent.shouldSearch() and (siteWithinRange != -1 or self.agent.assignedSite is self.agent.getHub())\
                and self.agent.world.siteList[siteWithinRange] is self.agent.assignedSite\
                and not self.agent.shouldGetLost():
            self.setState(SearchState(self.agent), None)
            return

        if self.agent.getPhaseNumber() == ASSESS:
            if self.agent.isDoneAssessing():
                self.acceptOrReject()
                return

        if self.agent.getPhaseNumber() == CANVAS:
            if self.agent.shouldRecruit():
                self.setState(LeadForwardState(self.agent), self.agent.assignedSite.getPosition())
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

        # If an agent nearby is transporting, get carried by that agent. TODO: If I do end up adding passive agents and brood items, I will get rid of this.
        for i in range(0, len(neighborList)):
            if neighborList[i].getState() == TRANSPORT:
                self.getCarried(neighborList[i])
                return

        # Let the agent's estimated quality of the site get closer to the actual quality as they spend time at the site.
        if self.agent.estimatedQuality > self.agent.assignedSite.getQuality():
            self.agent.estimatedQuality = np.round(self.agent.estimatedQuality - 0.1, 1)
        else:
            self.agent.estimatedQuality = np.round(self.agent.estimatedQuality + 0.1, 1)

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
                from states.LeadForwardState import LeadForwardState
                self.setState(LeadForwardState(self.agent), self.agent.assignedSite.getPosition())
        else:
            self.agent.setPhase(ExplorePhase())
            from states.SearchState import SearchState
            self.setState(SearchState(self.agent), None)

    # TODO: If I keep this, I need to remove the repetition with SearchState
    def getCarried(self, transporter):
        if transporter.numFollowers < MAX_FOLLOWERS:
            self.agent.leadAgent = transporter
            self.agent.leadAgent.incrementFollowers()
            from states.CarriedState import CarriedState
            self.setState(CarriedState(self.agent), self.agent.leadAgent.pos)

    def toString(self):
        return "AT_NEST"

    def getColor(self):
        return AT_NEST_COLOR
