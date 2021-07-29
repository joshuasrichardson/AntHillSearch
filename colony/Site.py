""" Site class. Stores 2D positions of hub and sites """
import numpy as np
import pygame as pyg
from pygame.rect import Rect

from Constants import *
from colony.myPygameUtils import drawCircleLines


class Site:
    """ Represents possible sites for agents to move to, including their old home """
    def __init__(self, surface, hubLocation, x, y, radius, quality, allSiteQualities, siteNoCloserThan, siteNoFartherThan,
                 shouldDraw, knowSitePosAtStart=KNOW_SITE_POS_AT_START):
        """ randomly places site at a 2D location and assigns it a random state """
        self.myfont = pyg.font.SysFont('Comic Sans MS', 12)  # The font that is used on the value of the site
        self.screen = surface  # The screen on which the site is drawn
        self.shouldDraw = shouldDraw  # Whether the simulation should be drawn on the screen

        self.quality = self.setQuality(quality)  # The quality of a site on a scale of 0 - 255
        self.allSiteQualities = allSiteQualities  # A list storing the qualities of all sites in the simulation
        self.color = self.setColor(self.quality)  # The color of the site, representing its quality

        self.hubLocation = hubLocation  # Where the agents' original home is
        self.siteNoCloserThan = siteNoCloserThan  # The closest to the hub that the sites can be randomly generated
        self.siteNoFartherThan = siteNoFartherThan  # The furthest to the hub that the sites can be randomly generated
        self.pos = self.initializePosition(x, y)  # Where the site is located when the simulation starts
        self.radius = radius  # The radius of the circle that represents the site
        self.siteRect = Rect(self.pos[0] - self.radius, self.pos[1] - self.radius, self.radius * 2, self.radius * 2)
        self.siteRect.centerx = self.pos[0]  # The x coordinate of the center of the rectangle
        self.siteRect.centery = self.pos[1]  # The y coordinate of the center of the rectangle

        self.agentCount = 0  # The number of agents assigned to the site
        self.wasFound = False
        self.knowSitePosAtStart = knowSitePosAtStart

        self.isSelected = False  # Whether the site is selected (helps with user controls)
        self.command = None
        self.commandPosition = None
        self.marker = None

        self.estimatedPosition = None
        self.estimatedQuality = None
        self.estimatedAgentCount = None

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

    def initializePosition(self, x, y):
        angle = np.random.uniform(0, np.pi * 2)
        radius = np.random.uniform(self.siteNoCloserThan, self.siteNoFartherThan)
        if x is None:
            x = int(self.hubLocation[0] + np.round(radius * np.cos(angle)))
        if y is None:
            y = int(self.hubLocation[1] + np.round(radius * np.sin(angle)))
        return [x, y]

    def drawSite(self):
        if self.wasFound or self.knowSitePosAtStart:
            pyg.draw.circle(self.screen, (115, 110, 80), self.pos, self.radius + 2, 0)
            if self.isSelected:
                pyg.draw.circle(self.screen, SELECTED_COLOR, self.pos, self.radius + 2, 0)
            self.siteRect = pyg.draw.circle(self.screen, self.color, self.pos, self.radius, 0)
            drawCircleLines(self.screen, self.siteRect, (115, 110, 80), self.getDensity(self.quality))
            img = self.myfont.render(str(self.agentCount), True, (0, 0, 0))
            self.screen.blit(img, (self.pos[0] - (img.get_width() / 2), self.pos[1] - (self.radius + 20), 15, 10))
        self.drawMarker()

    def drawMarker(self):
        if self.marker is not None:
            self.screen.blit(self.marker[0], self.marker[1])

    def setEstimates(self, est):
        self.estimatedPosition = est[0]
        self.estimatedQuality = est[1]
        self.estimatedAgentCount = est[2]

    def drawEstimatedSite(self):
        if self.wasFound or self.knowSitePosAtStart:
            try:
                if self.quality == -1:
                    color = 0, 0, 0
                    self.estimatedQuality = -1
                elif self.estimatedQuality < 0:
                    color = 255, 0, 0
                    self.estimatedQuality = 0
                elif self.estimatedQuality > 255:
                    color = 0, 255, 0
                else:
                    color = 255 - self.estimatedQuality, self.estimatedQuality, 0
                if self.isSelected:
                    pyg.draw.circle(self.screen, SELECTED_COLOR, self.estimatedPosition, self.radius + 2, 0)
                # TODO: Estimate the radius as well
                siteRect = pyg.draw.circle(self.screen, color, self.estimatedPosition, SITE_RADIUS, 0)
                drawCircleLines(self.screen, siteRect, (255, 255, 255), Site.getDensity(self.estimatedQuality))
                img = pyg.font.SysFont('Comic Sans MS', 12).render(str(self.estimatedAgentCount), True, color)
                self.screen.blit(img, (self.estimatedPosition[0] - (img.get_width() / 2), self.estimatedPosition[1] - (SITE_RADIUS + 20), 15, 10))
            except TypeError:
                self.drawSite()

    @staticmethod
    def getDensity(quality):
        return int(quality / 20) + 2

    def getQuality(self):
        return self.quality

    def normalizeQuality(self, span, zero):
        if self.allSiteQualities.count(self.quality) == 0:  # Only normalize if the quality was not manually set
            self.quality = int(round((self.quality - zero) / span * 255))
            # 255 is the maximum color range
            self.color = 255 - self.quality, self.quality, 0

    def getPosition(self):
        return [self.siteRect.centerx, self.siteRect.centery]

    def setPosition(self, pos):
        self.pos = pos
        self.siteRect.centerx = self.pos[0]
        self.siteRect.centery = self.pos[1]

    def getColor(self):
        return self.color

    def getSiteRect(self):
        return self.siteRect

    def incrementCount(self):
        self.agentCount += 1

    def decrementCount(self):
        self.agentCount -= 1

    def select(self):
        self.isSelected = True

    def unselect(self):
        self.isSelected = False

    def setCommand(self, command, position, marker):
        self.command = command
        self.commandPosition = position
        self.marker = marker

    def executeCommand(self, agent):
        if self.command is None:
            return False
        self.command(agent, self.commandPosition)
        return True
