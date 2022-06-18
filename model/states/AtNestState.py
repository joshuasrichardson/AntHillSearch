from config import Config
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
        """ agent - the agent that is in this state """
        super().__init__(agent)
        self.stateNumber = AT_NEST

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.getAssignedSitePosition())
        phaseNumber = self.agent.getPhaseNumber()

        if phaseNumber == CONVERGED:
            return

        # Checking the siteWithinRange makes sure they actually get to the site before they search again unless they get lost on the way.
        if self.agent.shouldSearch(self.agent.siteInRangeIndex):
            self.setState(SearchState(self.agent), None)
            return

        if phaseNumber == ASSESS:
            if self.agent.isDoneAssessing():
                self.acceptOrReject(neighborList)
                return

        elif phaseNumber == CANVAS:
            if self.agent.shouldRecruit():
                self.recruit(neighborList)
                return

        elif phaseNumber == COMMIT:
            if self.agent.tryConverging():
                return
            # Recruit, search, or follow
            if self.agent.shouldRecruit():
                self.agent.transportOrReverseTandem(self)
                return

        for i in range(0, len(neighborList)):
            neighborState = neighborList[i].getStateNumber()
            if neighborState == DEAD:
                self.agent.avoid(neighborList[i].getPosition())
            if (neighborState == LEAD_FORWARD and neighborList[i].estimatedQuality > self.agent.estimatedQuality)\
                    or (neighborState == REVERSE_TANDEM and neighborList[i].estimatedQuality >= self.agent.estimatedQuality)\
                    and self.agent.shouldFollow():
                self.tryFollowing(neighborList[i])
                return
            if neighborState == TRANSPORT:  # If an agent nearby is transporting, get carried by that agent.
                self.getCarried(neighborList[i])
                return
            if neighborList[i].getPhaseNumber() == CONVERGED:
                self.agent.tryConverging()

        # Let the agent's estimated quality of the site get closer to the actual quality as they spend time at the site.
        if self.agent.estimatedQuality > self.agent.assignedSite.getQuality():
            self.agent.estimatedQuality = round(self.agent.estimatedQuality - 0.1, 1)
        else:
            self.agent.estimatedQuality = round(self.agent.estimatedQuality + 0.1, 1)

        # If the site moves, they might not know where it is
        if self.agent.siteInRangeIndex != -1 and self.agent.world.siteList[self.agent.siteInRangeIndex] is self.agent.assignedSite:
            self.agent.estimateSitePositionMoreAccurately()

    def tryFollowing(self, leader):
        if leader.numFollowers < Config.MAX_FOLLOWERS:
            self.agent.leadAgent = leader
            self.agent.leadAgent.incrementFollowers()
            self.setState(FollowState(self.agent), self.agent.leadAgent.getPosition())

    def acceptOrReject(self, neighborList):
        # If they determine the site is good enough after they've been there long enough,
        if self.agent.estimatedQuality > Config.MIN_ACCEPT_VALUE:
            self.recruit(neighborList)
        else:
            self.agent.setPhase(ExplorePhase())
            from model.states.SearchState import SearchState
            self.setState(SearchState(self.agent), None)

    def getCarried(self, transporter):
        if transporter.numFollowers < Config.MAX_FOLLOWERS:
            self.agent.leadAgent = transporter
            self.agent.leadAgent.incrementFollowers()
            from model.states.CarriedState import CarriedState
            self.setState(CarriedState(self.agent), self.agent.leadAgent.getPosition())

    def recruit(self, neighborList):
        if self.agent.quorumMet(neighborList):
            # enough agents are already at the site, so they skip canvasing and go straight to the committed phase
            self.agent.setPhase(CommitPhase())
            self.agent.transportOrReverseTandem(self)
        else:
            # they enter the canvasing phase and start recruiting others.
            self.agent.setPhase(CanvasPhase())
            self.setState(LeadForwardState(self.agent), self.agent.getAssignedSitePosition())

    def toString(self):
        return "AT_NEST"

    def getColor(self):
        return AT_NEST_COLOR
