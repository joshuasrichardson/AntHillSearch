from Constants import *
from states.FollowState import FollowState
from states.LeadForwardState import LeadForwardState
from states.SearchState import SearchState
from states.phases.CommitPhase import CommitPhase
from states.State import State


class AtNestState(State):

    def __init__(self, agent):
        super().__init__(agent)
        self.state = AT_NEST
        self.color = AT_NEST_COLOR

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.assignedSite.getPosition())

        siteWithinRange = self.agent.agentRect.collidelist(self.agent.siteObserveRectList)
        # checking the siteWithinRange makes sure they actually get to the site before they search again unless they get lost on the way.
        if self.agent.shouldSearch() and siteWithinRange != -1\
                and self.agent.siteList[siteWithinRange] is self.agent.assignedSite\
                and not self.agent.shouldGetLost():
            self.setState(SearchState(self.agent), None)
            return

        if self.agent.phase == ASSESS:
            if self.agent.isDoneAssessing():
                self.acceptOrReject()
                return

        if self.agent.phase == CANVAS:
            if self.agent.shouldRecruit():
                self.setState(LeadForwardState(self.agent), self.agent.assignedSite.getPosition())
                return

        if self.agent.phase == COMMIT:
            # Recruit, search, or follow
            if self.agent.shouldRecruit():
                CommitPhase.transportOrReverseTandem(self)
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
                self.agent.setPhase(COMMIT)
                CommitPhase.transportOrReverseTandem(self)
            else:
                # they enter the canvasing phase and start recruiting others.
                self.agent.setPhase(CANVAS)
                from states.LeadForwardState import LeadForwardState
                self.setState(LeadForwardState(self.agent), self.agent.assignedSite.getPosition())
        else:
            self.agent.setPhase(EXPLORE)
            self.agent.assignSite(self.agent.hub)  # or None or just don't have this statement?
            from states.SearchState import SearchState
            self.setState(SearchState(self.agent), None)

    # TODO: If I keep this, I need to remove the repetition with SearchState
    def getCarried(self, transporter):
        if transporter.numFollowers < MAX_FOLLOWERS:
            self.agent.leadAgent = transporter
            self.agent.leadAgent.incrementFollowers()
            from states.CarriedState import CarriedState
            self.setState(CarriedState(self.agent), self.agent.leadAgent.pos)
