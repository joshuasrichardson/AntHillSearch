import numpy as np

from display.PredatorDisplay import getPredatorImage


class Predator:

    def __init__(self, site):
        self.site = site  # The site the predator will be terrorizing.
        pos = site.getPosition()
        self.pos = [pos[0] + np.random.randint(-100, 100), pos[1] + np.random.randint(-100, 100)]  # Where the predator is walking.
        self.predatorHandle = getPredatorImage(self.pos)  # Image on screen representing the agent
        self.predatorRect = self.predatorHandle.get_rect()  # Rectangle around the agent to help track collisions
        self.predatorRect.centerx = self.pos[0]  # Horizontal center of the agent
        self.predatorRect.centery = self.pos[1]  # Vertical center of the agent
        self.angle = 0
