from Constants import *
from states.SearchState import SearchState
from states.State import State


class FollowState(State):
    """ State where an agent is following an agent in the lead forward or reverse tandem state either toward
    the other agent's assigned site or toward the site they are going to recruit from """

    def __init__(self, agent):
        super().__init__(agent)
        self.state = FOLLOW
        self.color = FOLLOW_COLOR

    def changeState(self, neighborList) -> None:
        siteWithinRange = self.agent.agentRect.collidelist(self.agent.siteObserveRectList)
        if (self.agent.leadAgent.getState() == LEAD_FORWARD or self.agent.leadAgent.getState() == REVERSE_TANDEM)\
                and self.agent.siteList[siteWithinRange] != self.agent.leadAgent.assignedSite:
            if self.agent.shouldGetLost():
                self.agent.leadAgent = None
                self.setState(SearchState(self.agent), None)
            else:
                self.agent.updateFollowPosition()
                # If they get to the site the lead agent is recruiting from,
                if self.agent.phase == COMMIT and self.agent.leadAgent.getState() == REVERSE_TANDEM\
                        and self.agent.leadAgent.comingWithFollowers and self.agent.assignedSite == self.agent.leadAgent.assignedSite:
                    # they also start recruiting from that site.
                    self.agent.knownSites.add(self.agent.leadAgent.siteToRecruitFrom)
                    self.agent.siteToRecruitFrom = self.agent.leadAgent.siteToRecruitFrom
                    self.agent.leadAgent = None
                    self.agent.transportOrReverseTandem(self)
        else:
            # if they arrived at a nest:
            self.agent.knownSites.add(self.agent.leadAgent.assignedSite)
            self.agent.assignSite(self.agent.leadAgent.assignedSite)
            self.agent.leadAgent = None
            from states.AtNestState import AtNestState
            self.setState(AtNestState(self.agent), self.agent.assignedSite.getPosition())
