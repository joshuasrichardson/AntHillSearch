import numpy as np
from pygame.rect import Rect

from Constants import INITIAL_BLUR


class Site:
    """ Represents possible sites for agents to move to, including their old home """
    def __init__(self, numHubs, pos, radius, quality, numAgents=0):
        self.quality = self.setQuality(quality)  # The quality of a site on a scale of 0 - 255
        self.color = self.setColor(self.quality)  # The color of the site, representing its quality

        self.pos = pos  # Where the site is located when the interface starts
        self.radius = radius  # The radius of the circle that represents the site
        self.siteRect = Rect(self.pos[0] - self.radius, self.pos[1] - self.radius, self.radius * 2, self.radius * 2)
        self.siteRect.centerx = self.pos[0]  # The x coordinate of the center of the rectangle
        self.siteRect.centery = self.pos[1]  # The y coordinate of the center of the rectangle

        self.agentCount = numAgents  # The number of agents assigned to the site
        self.agentCounts = self.initAgentCounts(numHubs)  # The number of agents assigned to the site from each hub
        self.wasFound = False  # Whether the agents have visited the site yet

        self.isSelected = False  # Whether the site is selected (helps with user controls)
        self.command = None  # The command that is executed on agents when they arrive at the site
        self.commandPosition = None  # The position of the command (for commands like go)
        self.marker = None  # A marker to be drawn on the screen representing the command

        self.estimatedPosition = None  # The average position of where agents think the site is located
        self.estimatedQuality = None  # The average quality of what agents think it is
        self.estimatedAgentCount = None  # The average number of agents of how many agents think there are
        self.estimatedRadius = None  # The average radius of how big agents think it is
        self.estimatedSiteRect = None  # The rect based on estimated values

        self.blurAmount = INITIAL_BLUR  # How blurry the site appears on the screen. Higher is blurrier.
        self.blurRadiusDiff = INITIAL_BLUR  # How much bigger the estimated site appear than its actual size (helps it look blurrier)

    @staticmethod
    def initAgentCounts(numHubs):
        agentCounts = []
        for i in range(numHubs):
            agentCounts.append(0)
        return agentCounts

    def setQuality(self, quality):
        """ Sets the quality to the specified value unless it is outside the range 0 - 255 """
        try:  # Prevent the hub's quality from being changed
            if self.quality < 0 or self.quality >= 0 > quality:
                return self.quality
        except AttributeError:
            pass
        if quality is None:
            self.quality = np.random.uniform(0, 255)  # 255 is maximum color, so maximum quality
        elif quality > 255:  # If the quality is greater than the max,
            self.quality = 255  # Set the quality to the max
        elif quality < -1:  # If the quality is less than the min, (less than -1 because the hub is arbitrarily set to -1. Every other site has to be at least 0)
            self.quality = 0  # Set the quality to the min
        else:
            self.quality = quality
        return self.quality

    def setColor(self, quality):
        """ Sets the color based on the given quality """
        try:  # Prevent the hub's quality from being changed
            if self.quality < 0 or self.quality >= 0 > quality:
                return self.color
        except AttributeError:
            pass
        if quality < 0:  # If the quality is less than the min, set the color to black (just for the hub)
            self.color = (0, 0, 0)
        else:
            self.color = 255 - quality, quality, 0
        return self.color

    def setEstimates(self, est):
        """ Takes an array with each values' estimate and updates the site's estimated values """
        self.estimatedPosition = est[0]
        self.estimatedQuality = est[1]
        self.estimatedAgentCount = est[2]
        self.estimatedRadius = est[3]

    def updateBlur(self):
        """ Make the blur gradually get clearer """
        if self.blurAmount > 1.05:
            self.blurAmount -= 0.05
        elif self.blurAmount > 1:
            self.blurAmount = 1
        if self.blurRadiusDiff > 0.05:
            self.blurRadiusDiff -= 0.05
        elif self.blurRadiusDiff > 0:
            self.blurRadiusDiff = 0

    @staticmethod
    def getDensity(quality):
        """ Get the space between lines """
        return int(quality / 20) + 2

    def getQuality(self):
        return self.quality

    def normalizeQuality(self, span, zero, siteQualities):
        """ Sets the qualities to have a max of 255 and a min of 0 and adjusts qualities in between the min and max
         to be spaced out accordingly """
        if siteQualities.count(self.quality) == 0 and self.quality >= 0:  # Only normalize if the quality was not manually set
            self.quality = int(round((self.quality - zero) / span * 255))
            # 255 is the maximum color range
            self.color = 255 - self.quality, self.quality, 0

    def getPosition(self):
        return [self.siteRect.centerx, self.siteRect.centery]

    def setPosition(self, pos):
        self.pos = list(pos)
        self.siteRect.centerx = self.pos[0]
        self.siteRect.centery = self.pos[1]

    def getColor(self):
        return self.color

    def getEstimatedColor(self):
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
        return color

    def getSiteRect(self):
        return self.siteRect

    def incrementCount(self, hubIndex):
        self.agentCount += 1
        self.agentCounts[hubIndex] += 1

    def decrementCount(self, hubIndex):
        self.agentCount -= 1
        self.agentCounts[hubIndex] -= 1

    def select(self):
        self.isSelected = True

    def unselect(self):
        self.isSelected = False

    def setCommand(self, command, position, marker):
        self.command = command
        self.commandPosition = list(position)
        self.marker = marker

    def executeCommand(self, agent):
        if self.command is None:
            return False
        self.command(agent, self.commandPosition)
        return True
