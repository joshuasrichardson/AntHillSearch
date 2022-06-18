import numpy as np

from config import Config
from display.simulation.LadybugDisplay import getLadybugImage


class Ladybug:
    """ Ladybugs are friendly to the agents. When an agent comes in contact with them, they tell it where it can
    find a great-quality site. """

    def __init__(self, site, world, pos=None):
        """ site - the site the ladybug knows about
        world - the world the ladybug lives in
        pos - the initial position of the ladybug on the screen """
        self.world = world
        if pos is None:
            pos = site.getPosition()
            self.pos = [pos[0] + np.random.randint(-100, 100),
                        pos[1] + np.random.randint(-100, 100)]  # Where the ladybug is walking
        else:
            self.pos = pos
        self.ladybugHandle = getLadybugImage(self.pos)  # Image on screen representing ladybug
        self.ladybugRect = self.ladybugHandle.get_rect()  # Rectangle around the ladybug to help track collisions
        self.ladybugRect.centerx = self.pos[0]  # Horizontal center of the ladybug
        self.ladybugRect.centery = self.pos[1]  # Vertical center of the ladybug
        self.angle = np.random.uniform(0, 2 * np.pi)  # The direction the ladybug is facing in radians
        self.speed = np.random.randint(3, 5)  # The speed the ladybug is moving
        self.numSteps = np.random.randint(0, 20)  # The number of steps the ladybug has taken since turning
        self.bestSite = self.determineBestSite()

    def getRect(self):
        return self.ladybugRect

    def setPosition(self, x, y):
        self.ladybugRect.centerx = x
        self.ladybugRect.centery = y
        self.pos = list([x, y])

    def moveForward(self):
        self.numSteps += 1
        self.setPosition(int(np.round(float(self.pos[0]) + self.speed * np.sin(self.angle))),
                         int(np.round(float(self.pos[1]) + self.speed * -np.cos(self.angle))))
        if self.numSteps > 20:
            self.turn()

    def turn(self):
        self.numSteps = 0
        self.angle += 2 * np.pi / 4

    def setAngle(self, angle):
        self.angle = angle

    def help(self, helpeeList):
        if np.random.exponential() > Config.HELP_THRESHOLD:
            for agent in helpeeList:
                agent.assignSite(self.bestSite)
        else:
            for agent in helpeeList:
                agent.addToKnownSites(self.bestSite)

    def determineBestSite(self):
        bestSite = self.world.siteList[0]
        for i in range(len(self.world.siteList)):
            if self.world.siteList[i].getQuality() > bestSite.getQuality():
                bestSite = self.world.siteList[i]
        return bestSite
