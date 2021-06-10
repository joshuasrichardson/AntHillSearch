""" Site class. Stores 2D positions of hub and sites """
import numpy as np
import pygame as pyg
from Constants import *


class Site:
    def __init__(self, surface):
        """randomly places site at a 2D location and assigns it a random state"""
        self.myfont = pyg.font.SysFont('Comic Sans MS', 12)
        self.screen = surface
        self.quality = np.random.uniform(0, 255)  # 255 is maximum color, so maximum quality
        self.color = 255 - self.quality, self.quality, 0
        angle = np.random.uniform(0, np.pi*2)
        radius = np.random.uniform(SITE_NO_CLOSER_THAN, SITE_NO_FARTHER_THAN)
        x = int(HUB_LOCATION[0] + np.round(radius * np.cos(angle)))
        y = int(HUB_LOCATION[1] + np.round(radius * np.sin(angle)))
        self.pos = [x, y]
        self.radius = SITE_SIZE
        self.siteRect = pyg.draw.circle(self.screen, self.color, self.pos, self.radius, 0)
        self.agentCount = 0
        self.observeRadius = SITE_OBSERVED_RANGE
        self.siteObserveRect = pyg.draw.circle(self.screen, self.color, self.pos, self.observeRadius, 0)

        self.siteRect.centerx = self.pos[0]
        self.siteRect.centery = self.pos[1]
        self.siteObserveRect.centerx = self.pos[0]
        self.siteObserveRect.centery = self.pos[1]

    def drawSite(self):
        self.siteRect = pyg.draw.circle(self.screen, self.color, self.pos, self.radius, 0)
        img = self.myfont.render(str(self.agentCount), True, self.color)
        self.screen.blit(img, (self.pos[0] - 5, self.pos[1] - 40, 15, 10))     # """JOSHUA"""

    def getQuality(self):
        return self.quality

    def normalizeQuality(self, span, zero):
        self.quality = int(round((self.quality - zero)/span*255)) 
        # 255 is the maximum color range
        self.color = 255 - self.quality, self.quality, 0

    def getPosition(self):
        # return self.x,self.y
        return [self.siteRect.centerx, self.siteRect.centery]

    def getColor(self):
        return self.color

    def getAgentRect(self):
        return self.siteRect

    def incrementCount(self):
        self.agentCount += 1

    def decrementCount(self):
        self.agentCount -= 1
