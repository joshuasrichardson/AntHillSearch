import numpy as np
from abc import ABC, abstractmethod

import Utils
from config import Config


class State(ABC):
    """ An abstract base class for the states the agents can be in """

    def __init__(self, agent):
        """ agent - the agent that is in this state """
        self.agent = agent

    def setState(self, state, target):
        self.agent.setTarget(target)
        self.updateAngle()
        self.agent.setState(state)
        self.forgetMovedSites()

    def updateAngle(self) -> None:
        # Move toward target
        if self.agent.target is not None:
            self.agent.setAngle(np.arctan2(self.agent.target[1] - self.agent.pos[1], self.agent.target[0] - self.agent.pos[0]))

    def forgetMovedSites(self):
        knownSiteRects = []
        for site in self.agent.knownSites:
            knownSiteRects.append(site.getSiteRect())
        for i, pos in enumerate(self.agent.knownSitesPositions):
            rect = self.agent.getRect()
            atOldSitePos = rect.collidepoint(pos[0], pos[1])
            siteIndex = rect.collidelist(knownSiteRects)
            if atOldSitePos and siteIndex != i:
                try:
                    self.agent.removeKnownSite(self.agent.knownSites[siteIndex])
                except IndexError:
                    self.agent.removeKnownSite2(siteIndex)
                break

    def executeCommands(self):
        self.agent.siteInRangeIndex = self.agent.getRect().collidelist(self.agent.world.siteRectList)
        if Config.DRAW_FAR_AGENTS:  # If we are using an interface that lets us access things that are far from the hub
            if self.agent.siteInRangeIndex != -1:  # And the agent comes in contact with a site that has a command
                return self.agent.world.siteList[self.agent.siteInRangeIndex].executeCommands(self.agent)  # Just do the command and be done with this round.
        else:
            if -1 < self.agent.siteInRangeIndex < len(self.agent.world.hubs):  # If we can't access far things, we should have the agents that are assigned to far sites do the command for that site when they get to the hub (where they can receive that instruction).
                return self.agent.assignedSite.executeCommands(self.agent)
            return False

    def doStateActions(self, neighborList) -> None:
        avoidPlaces = self.agent.getNearbyPlaceToAvoid()
        if len(avoidPlaces) == 0:
            self.changeState(neighborList)
        else:  # If the agent is too close to a place they are supposed to avoid
            self.agent.escape(avoidPlaces)  # Turn away from it.

    @abstractmethod
    def changeState(self, neighborList):
        pass

    @abstractmethod
    def toString(self):
        pass

    @abstractmethod
    def getColor(self):
        pass
