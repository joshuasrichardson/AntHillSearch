from abc import abstractmethod

import numpy as np
from pygame import Rect

from config import Config
from Constants import COMMIT
from model.states.State import State


class RecruitState(State):
    """ Abstract state where agents recruit other agents to come to their assigned site """

    def __init__(self, agent):
        """ agent - the agent that is in this state """
        super().__init__(agent)

    def changeState(self, neighborList) -> None:
        # Choose a site to recruit from
        if self.agent.goingToRecruit:  # if they are on the way to go recruit someone, they keep going until they get there.
            self.setState(self, self.agent.getRecruitSitePosition())
            if not Config.FIND_SITES_EASILY and self.arrivedAtOrPassedSite(self.agent.getRecruitSitePosition())\
                    and not self.arrivedAtOrPassedSite(self.agent.recruitSite.getPosition()):
                self.agent.goingToRecruit = False
                self.agent.removeKnownSite(self.agent.recruitSite)
                from model.states.AtNestState import AtNestState
                self.setState(AtNestState(self.agent), self.agent.getAssignedSitePosition())
            if self.arrivedAtOrPassedSite(self.agent.recruitSite.getPosition()):  # If agent finds the old site, (or maybe this works with accidentally running into a site on the way)
                self.agent.goingToRecruit = False  # The agent is now going to head back to the new site
                self.agent.comingWithFollowers = True
                self.agent.recruitSiteLastKnownPos = self.agent.recruitSite.getPosition()
                self.setState(self, self.agent.getAssignedSitePosition())  # Go back to the new site with the new follower(s).
            return

        if self.agent.comingWithFollowers:
            self.setState(self, self.agent.getAssignedSitePosition())
            if not Config.FIND_SITES_EASILY and self.arrivedAtOrPassedSite(self.agent.getAssignedSitePosition())\
                    and not self.arrivedAtOrPassedSite(self.agent.assignedSite.getPosition()):  # If they get to where they thought the site was
                self.agent.numFollowers = 0
                self.agent.comingWithFollowers = False
                self.agent.removeKnownSite(self.agent.assignedSite)
                from model.states.SearchState import SearchState
                self.setState(SearchState(self.agent), None)
            if self.arrivedAtOrPassedSite(self.agent.assignedSite.getPosition()):  # If they get to the assigned site
                self.agent.numFollowers = 0
                self.agent.comingWithFollowers = False
                if self.agent.getPhaseNumber() == COMMIT and self.agent.tryConverging():
                    return
                self.arriveAtSite(neighborList)
            return

        if len(self.agent.knownSites) > 1:
            self.chooseSiteToRecruitFrom()
        else:
            from model.states.SearchState import SearchState
            self.setState(SearchState(self.agent), None)
            return

    @abstractmethod
    def arriveAtSite(self, numNeighbors):
        pass

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

    def chooseSiteToRecruitFrom(self):
        indexOfSiteToRecruitFrom = np.random.randint(0, len(self.agent.knownSites))
        self.agent.recruitSite = self.agent.knownSites[indexOfSiteToRecruitFrom]
        while self.agent.recruitSite == self.agent.assignedSite:
            indexOfSiteToRecruitFrom = np.random.randint(0, len(self.agent.knownSites))
            self.agent.recruitSite = self.agent.knownSites[indexOfSiteToRecruitFrom]
        if Config.FIND_SITES_EASILY:
            self.agent.recruitSiteLastKnownPos = self.agent.recruitSite.getPosition()
        else:
            self.agent.recruitSiteLastKnownPos = self.agent.knownSitesPositions[indexOfSiteToRecruitFrom]
        self.agent.goingToRecruit = True
        self.setState(self, self.agent.getRecruitSitePosition())  # Go to their randomly chosen site to recruit.
