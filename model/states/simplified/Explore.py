from Constants import *
from config.Config import PROB_ER, PROB_EA
from model.states.State import State
from numpy import pi, random


class ExploreState(State):
    """ State where agents look around the world for better sites """

    def __init__(self, agent):
        """ agent - the agent that is in this state """
        super().__init__(agent)
        self.stateNumber = EXPLORE_STATE
        self.collides = False
        self.itersSinceLastCollide = 8
        self.agent.setAngle(random.uniform(0, pi * 2))

    def updateAngle(self) -> None:
        self.itersSinceLastCollide += 1
        if self.collides and self.itersSinceLastCollide > 8:  # Go straight unless they bump into an obstacle
            if random.randint(0, 2) == 1:
                self.agent.setAngle(self.agent.getAngle() - pi / 2)  # Ants are more likely to turn left.
                # See https://www.nature.com/articles/s41598-018-23652-4
            else:
                self.agent.setAngle(random.uniform(0, 2 * pi))
            self.itersSinceLastCollide = 0

    def changeState(self, neighborList) -> None:
        self.setState(self, self.agent.target)
        # Set whether they collided with another agent or not. If they are by a nest, they don't collide because they can go down into the nest, etc.
        self.collides = len(neighborList) > 1 and not self.agent.isCloseToASite()
        self.agent.marker = None

        # If agent finds a site within range then maybe assess it
        if self.agent.siteInRangeIndex != -1:
            # print(f"site: {self.agent.siteInRangeIndex}")
            site = self.agent.world.siteList[self.agent.siteInRangeIndex]
            if not site.isHub():
                site.wasFound = True
                d = len(neighborList)  # number of agents assigned to the site
                qual = site.getQuality() / 255  # quality of site. quality is between 0 and 1
                deg_factor = 1.0
                qual_factor = self.agent.world.getNumAgents() / 5.0
                X = deg_factor * (d + 1.0) / self.agent.world.getNumSites() + qual_factor * qual
                explore_to_assess = PROB_EA * self.agent.world.getNumSites() / 4.0 * X / self.agent.world.getNumAgents()
                explore_to_assess *= 10

                if random.uniform(0, 1) < explore_to_assess:
                    from model.states.simplified.Assess import AssessState
                    self.agent.assignSite(site)
                    self.setState(AssessState(self.agent), site.getPosition())
                    return

        if random.uniform(0, 1) < PROB_ER:
            from model.states.simplified.Rest import RestState
            self.setState(RestState(self.agent), self.agent.getHub().getPosition())
            return

        if self.agent.isTooFarAway(self.agent.getHub()):
            self.goBackTowardSite(self.agent.getHub())

    def goBackTowardSite(self, site):
        if site.getPosition()[0] > self.agent.getPosition()[0]:
            x = self.agent.getPosition()[0] + 1
        else:
            x = self.agent.getPosition()[0] - 1
        if site.getPosition()[1] > self.agent.getPosition()[1]:
            y = self.agent.getPosition()[1] + 1
        else:
            y = self.agent.getPosition()[1] - 1
        self.agent.setPosition(x, y)
        self.agent.setAngle(self.agent.angle - (1.1 * pi))

    def toString(self):
        return "EXPLORE"

    def getColor(self):
        return EXPLORE_STATE_COLOR
