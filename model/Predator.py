import numpy as np
import pygame

from Constants import KILL_THRESHOLD
from display.PredatorDisplay import getPredatorImage


class Predator:

    def __init__(self, site, world):
        self.site = site  # The site the predator will be terrorizing.
        self.world = world
        pos = site.getPosition()
        self.pos = [pos[0] + np.random.randint(-100, 100), pos[1] + np.random.randint(-100, 100)]  # Where the predator is walking.
        self.predatorHandle = getPredatorImage(self.pos)  # Image on screen representing the predator
        self.predatorRect = self.predatorHandle.get_rect()  # Rectangle around the predator to help track collisions
        self.predatorRect.centerx = self.pos[0]  # Horizontal center of the predator
        self.predatorRect.centery = self.pos[1]  # Vertical center of the predator
        self.angle = np.random.uniform(0, 2 * np.pi)
        self.speed = np.random.randint(3, 5)
        self.numSteps = np.random.randint(0, 20)
        self.discovered = False

    def getRect(self):
        return self.predatorRect

    def updatePosition(self, position=None):
        self.numSteps += 1
        if position is None:  # If the position is not specified, continue moving along the same path as before
            self.predatorRect.centerx = int(np.round(float(self.pos[0]) + self.speed * np.sin(self.angle)))
            self.predatorRect.centery = int(np.round(float(self.pos[1]) + self.speed * -np.cos(self.angle)))
            if self.numSteps > 20:
                self.numSteps = 0
                self.angle += 2 * np.pi / 3
        else:  # Else, update the position to match the parameter
            self.predatorRect.centerx = position[0]
            self.predatorRect.centery = position[1]
        self.pos = list([self.predatorRect.centerx, self.predatorRect.centery])

    def setAngle(self, angle):
        self.angle = angle

    def attack(self, preyList):
        if np.random.exponential() > KILL_THRESHOLD:
            for agent in preyList:
                agent.die()
        else:
            for agent in preyList:
                # if agent.getNearbyPlaceToAvoid() is None:
                agent.avoid(self.pos)
