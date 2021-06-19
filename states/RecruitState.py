from abc import abstractmethod

import numpy as np

from states.State import State


class RecruitState(State):

    def __init__(self, agent):
        super().__init__(agent)

    def changeState(self, neighborList) -> None:
        # Choose a site to recruit from
        if self.agent.goingToRecruit:  # if they are on the way to go recruit someone, they keep going until they get there. TODO: Can they get lost here? for now, no.
            self.setState(self, self.agent.siteToRecruitFrom.getPosition())
            if self.agent.agentRect.collidepoint(self.agent.siteToRecruitFrom.pos):  # If agent finds the old site, (or maybe this works with accidentally running into a site on the way)
                self.agent.goingToRecruit = False  # The agent is now going to head back to the new site
                self.agent.comingWithFollowers = True
                self.setState(self, self.agent.assignedSite.getPosition())  # Go back to the new site with the new follower(s).
            return

        if self.agent.comingWithFollowers:
            self.setState(self, self.agent.assignedSite.getPosition())
            if self.agent.agentRect.collidepoint(self.agent.assignedSite.pos):  # If they get to the assigned site
                self.agent.numFollowers = 0
                self.agent.comingWithFollowers = False
                self.arriveAtSite()
            return

        self.agent.siteToRecruitFrom = self.agent.assignedSite
        while self.agent.siteToRecruitFrom == self.agent.assignedSite:
            indexOfSiteToRecruitFrom = np.random.randint(0, len(self.agent.knownSites))
            index = 0
            for site in self.agent.knownSites:
                if index == indexOfSiteToRecruitFrom:
                    self.agent.siteToRecruitFrom = site
                index += 1
        self.agent.goingToRecruit = True
        self.setState(self, self.agent.siteToRecruitFrom.getPosition())  # Go to their randomly chosen site to recruit.

    @abstractmethod
    def arriveAtSite(self):
        self.arriveAtSite()
