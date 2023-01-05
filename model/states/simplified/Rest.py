import random

import numpy as np

from Constants import *
from config.Config import PROB_RE
from model.states.State import State
from model.states.simplified.Assess import AssessState
from model.states.simplified.Explore import ExploreState


class RestState(State):
    """ State where an agent is just at the hub resting """

    def __init__(self, agent):
        """ agent - the agent that is in this state """
        super().__init__(agent)
        self.stateNumber = REST_STATE

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.getHub().getPosition())

        dancers = []
        nonHubSites = list(filter(lambda s: not s.isHub(), self.agent.world.getSiteList()))
        degrees = [0 for _ in nonHubSites]  # The number of recruiting agents at each site
        for neighbor in neighborList:
            if neighbor.getStateNumber() == DANCE_STATE and not neighbor.assignedSite.isHub():
                dancers.append(neighbor)
                degrees[self.agent.world.getSiteIndex(neighbor.assignedSite) - len(self.agent.world.hubs)] += 1

        max_deg = max(degrees)
        siteList = []
        for i, degree in enumerate(degrees):
            if degree > 0:
                siteList.append(nonHubSites[i])
        for i, degree in enumerate(reversed(degrees)):
            if degree == 0:
                degrees.remove(degree)

        # d should be the number of dancers for the given site
        if len(siteList) > 0:
            deg_factor = 1.0
            Y = [deg_factor * d + 1.0 / self.agent.world.getNumSites() for d in degrees]
            pdf = Y
            pdf = [value / sum(pdf) for value in pdf]
            choice = np.random.choice(siteList, p=pdf)
            PROB_RA = 2 / self.agent.world.getNumAgents()
            rest_to_assess = (0.5 + PROB_RA) * (max_deg / sum(Y))
            rest_to_assess /= 38
            if random.uniform(0, 1) < rest_to_assess:
                self.agent.assignSite(choice)
                self.setState(AssessState(self.agent), choice.getPosition())
                return

        if random.uniform(0, 1) < PROB_RE / 10:
            self.setState(ExploreState(self.agent), self.agent.getHub().getPosition())
            return

    def toString(self):
        return "REST"

    def getColor(self):
        return REST_STATE_COLOR
