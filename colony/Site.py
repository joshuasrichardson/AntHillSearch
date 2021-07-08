""" Site class. Stores 2D positions of hub and sites """
import numpy as np
import pygame as pyg
from Constants import *


class Site:
    """ Represents possible sites for agents to move to, including their old home """
    def __init__(self, surface, x, y, quality):
        """ randomly places site at a 2D location and assigns it a random state """
        self.myfont = pyg.font.SysFont('Comic Sans MS', 12)
        self.screen = surface
        self.quality = self.setQuality(quality)
        self.color = self.setColor(self.quality)

        self.pos = self.initializePosition(x, y)
        self.radius = SITE_SIZE
        self.siteRect = pyg.draw.circle(self.screen, self.color, self.pos, self.radius, 0)
        self.agentCount = 0
        self.observeRadius = SITE_OBSERVED_RANGE
        self.siteObserveRect = pyg.draw.circle(self.screen, self.color, self.pos, self.observeRadius, 0)

        self.siteRect.centerx = self.pos[0]
        self.siteRect.centery = self.pos[1]
        self.siteObserveRect.centerx = self.pos[0]
        self.siteObserveRect.centery = self.pos[1]

        self.isSelected = False

    def setQuality(self, quality):
        if quality is None:
            self.quality = np.random.uniform(0, 255)  # 255 is maximum color, so maximum quality
        elif quality > 255:
            self.quality = 255
        elif quality < -1:
            self.quality = 0
        else:
            self.quality = quality
        return self.quality

    def setColor(self, quality):
        if quality < 0:
            self.color = (0, 0, 0)
        else:
            self.color = 255 - quality, quality, 0
        return self.color

    @staticmethod
    def initializePosition(x, y):
        angle = np.random.uniform(0, np.pi * 2)
        radius = np.random.uniform(SITE_NO_CLOSER_THAN, SITE_NO_FARTHER_THAN)
        if x is None:
            x = int(HUB_LOCATION[0] + np.round(radius * np.cos(angle)))
        if y is None:
            y = int(HUB_LOCATION[1] + np.round(radius * np.sin(angle)))
        return [x, y]

    def drawSite(self):
        if self.isSelected:
            pyg.draw.circle(self.screen, SELECTED_COLOR, self.pos, self.radius + 2, 0)
        self.siteRect = pyg.draw.circle(self.screen, self.color, self.pos, self.radius, 0)
        img = self.myfont.render(str(self.agentCount), True, self.color)
        self.screen.blit(img, (self.pos[0] - (img.get_width() / 2), self.pos[1] - (self.radius + 20), 15, 10))

    def getQuality(self):
        return self.quality

    def normalizeQuality(self, span, zero):
        if SITE_QUALITIES.count(self.quality) == 0:  # Only normalize if the quality was not manually set
            self.quality = int(round((self.quality - zero) / span * 255))
            # 255 is the maximum color range
            self.color = 255 - self.quality, self.quality, 0

    def getPosition(self):
        # return self.x,self.y
        return [self.siteRect.centerx, self.siteRect.centery]

    def setPosition(self, pos):
        self.pos = pos
        self.siteRect.centerx = self.pos[0]
        self.siteRect.centery = self.pos[1]
        self.siteObserveRect.centerx = self.pos[0]
        self.siteObserveRect.centery = self.pos[1]

    def getColor(self):
        return self.color

    def getAgentRect(self):
        return self.siteRect

    def incrementCount(self):
        self.agentCount += 1

    def decrementCount(self):
        self.agentCount -= 1

    def select(self):
        self.isSelected = True

    def unselect(self):
        self.isSelected = False
