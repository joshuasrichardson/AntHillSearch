import numpy as np
from abc import ABC, abstractmethod

from Constants import SEARCH, AT_NEST, LEAD_FORWARD, FOLLOW, REVERSE_TANDEM, TRANSPORT, GO, CARRIED
from display import Display


def numToState(num, agent):
    if num == AT_NEST:
        from model.states.AtNestState import AtNestState
        return AtNestState(agent)
    if num == SEARCH:
        from model.states.SearchState import SearchState
        return SearchState(agent)
    if num == CARRIED:
        from model.states.CarriedState import CarriedState
        return CarriedState(agent)
    if num == FOLLOW:
        from model.states.FollowState import FollowState
        return FollowState(agent)
    if num == LEAD_FORWARD:
        from model.states.LeadForwardState import LeadForwardState
        return LeadForwardState(agent)
    if num == REVERSE_TANDEM:
        from model.states.ReverseTandemState import ReverseTandemState
        return ReverseTandemState(agent)
    if num == TRANSPORT:
        from model.states.TransportState import TransportState
        return TransportState(agent)
    if num == GO:
        from model.states.GoState import GoState
        return GoState(agent)


class State(ABC):
    """ An abstract base class for the states the agents can be in """

    def __init__(self, agent):
        self.agent = agent

    def setState(self, state, target):
        self.agent.target = target
        self.updateAngle(state.state)
        self.agent.state = state

    def updateAngle(self, stateNum) -> None:
        if stateNum == SEARCH:  # If changing state to search from something else, set angle randomly
            self.agent.setAngle(np.random.uniform(0, np.pi * 2, 1))
        else:  # Move toward target
            self.agent.setAngle(np.arctan2(self.agent.target[1] - self.agent.pos[1], self.agent.target[0] - self.agent.pos[0]))
        self.forgetMovedSites()

    def forgetMovedSites(self):
        knownSiteRects = []
        for site in self.agent.knownSites:
            knownSiteRects.append(site.getSiteRect())
        for i, pos in enumerate(self.agent.knownSitesPositions):
            rect = self.agent.getAgentRect()
            atOldSitePos = rect.collidepoint(pos[0], pos[1])
            siteIndex = rect.collidelist(knownSiteRects)
            if atOldSitePos and siteIndex != i:
                try:
                    self.agent.removeKnownSite(self.agent.knownSites[siteIndex])
                except IndexError:
                    self.agent.removeKnownSite2(siteIndex)
                break

    def executeCommand(self):
        self.agent.siteInRangeIndex = self.agent.getAgentRect().collidelist(self.agent.world.siteRectList)
        if Display.drawFarAgents:  # If we are using an interface that lets us access things that are far from the hub
            if self.agent.siteInRangeIndex != -1:  # And the agent comes in contact with a site that has a command
                return self.agent.world.siteList[self.agent.siteInRangeIndex].executeCommand(self.agent)  # Just do the command and be done with this round.
        else:
            if -1 < self.agent.siteInRangeIndex < len(self.agent.world.hubs):  # If we can't access far things, we should have the agents that are assigned to far sites do the command for that site when they get to the hub (where they can receive that instruction).
                return self.agent.assignedSite.executeCommand(self.agent)
            return False

    @abstractmethod
    def changeState(self, neighborList) -> None:
        pass

    @abstractmethod
    def toString(self):
        pass

    @abstractmethod
    def getColor(self):
        pass
