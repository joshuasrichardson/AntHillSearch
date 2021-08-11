import numpy as np
import pygame as pyg
from pygame.rect import Rect

from Constants import *
from colony.PygameUtils import drawCircleLines, drawDashedLine, getBlurredImage


class Site:
    """ Represents possible sites for agents to move to, including their old home """
    def __init__(self, surface, hubLocation, x, y, radius, quality, siteNoCloserThan, siteNoFartherThan,
                 knowSitePosAtStart=DRAW_ESTIMATES):
        self.screen = surface  # The screen on which the site is drawn

        self.quality = self.setQuality(quality)  # The quality of a site on a scale of 0 - 255
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
        self.wasFound = False  # Whether the agents have visited the site yet
        self.knowSitePosAtStart = knowSitePosAtStart  # Whether the user knows where the sites are at the start of the simulation

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

    def setQuality(self, quality):
        """ Sets the quality to the specified value unless it is outside the range 0 - 255 """
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
        if quality < 0:  # If the quality is less than the min, set the color to black (just for the hub)
            self.color = (0, 0, 0)
        else:
            self.color = 255 - quality, quality, 0
        return self.color

    def initializePosition(self, x, y):
        """ Sets the site in its starting position at a random distance from the hub that is within the range
        specified with the initialization of the class or to the (x, y) coordinates if they are specified """
        angle = np.random.uniform(0, np.pi * 2)
        radius = np.random.uniform(self.siteNoCloserThan, self.siteNoFartherThan)
        if x is None:
            x = int(self.hubLocation[0] + np.round(radius * np.cos(angle)))
        if y is None:
            y = int(self.hubLocation[1] + np.round(radius * np.sin(angle)))
        return [x, y]

    def drawSite(self):
        """ Draws the site and some things associated with it on the screen """
        if self.wasFound or self.knowSitePosAtStart:  # If the agents have already discovered the site
            self.drawMarker()  # Draw a marker if the site has one
            pyg.draw.circle(self.screen, BORDER_COLOR, self.pos, self.radius + 2, 0)  # Draw a background for the site that blends with the surface better than the site color
            if self.isSelected:
                pyg.draw.circle(self.screen, SELECTED_COLOR, self.pos, self.radius + 2, 0)  # Draw a circle over the background showing that the site is selected
            self.siteRect = pyg.draw.circle(self.screen, self.color, self.pos, self.radius, 0)  # Draw a circle the color representing the quality of the site
            drawCircleLines(self.screen, self.siteRect, BORDER_COLOR, self.getDensity(self.quality))  # Draw grid lines representing the quality of the site (more lines is worse)
            img = pyg.font.SysFont('Comic Sans MS', 12).render(str(self.agentCount), True, BORDER_COLOR)
            self.screen.blit(img, (self.pos[0] - (img.get_width() / 2), self.pos[1] - (self.radius + 20)))  # Show the number of agents assigned to the site above the site
            if self.isSelected:
                self.drawQuality()  # Draw the site's quality right in the middle of it if it is selected.

    def drawQuality(self):
        """ Draw the quality of the site directly on top of the site """
        img = pyg.font.SysFont('Comic Sans MS', 15).render("MM", True, WORDS_COLOR)  # Make this image for all the sites to get a consistently sized rectangle
        rect = img.get_rect()
        pyg.draw.rect(img, SCREEN_COLOR, rect)  # Draw a rectangle on top of the site so the quality will be easier to read
        pyg.draw.rect(img, BORDER_COLOR, rect, 1)  # Draw a nice little border around that rectangle
        words = pyg.font.SysFont('Comic Sans MS', 12).render(str(int(self.quality)), True, WORDS_COLOR)  # Draw the quality
        img.blit(words, [((img.get_width() / 2) - (words.get_width() / 2)), ((img.get_height() / 2) - (words.get_height() / 2))])  # on the rectangle
        self.screen.blit(img, (self.pos[0] - (img.get_width() / 2), self.pos[1] - (img.get_height() / 2)))  # Draw the rectangle with the quality on it on the screen

    def drawMarker(self):
        """ Draw a marker on the screen representing the command that will be applied to agents that come to the site """
        if self.marker is not None:
            # Draw a dashed line from the site to the marker
            drawDashedLine(self.screen, BORDER_COLOR, self.pos, self.marker[1].center)
            # Draw the marker
            self.screen.blit(self.marker[0], self.marker[1])

    def drawAssignmentMarker(self, fromPos, color):
        drawDashedLine(self.screen, color, fromPos, self.pos)
        if self.knowSitePosAtStart:  # If the agents know where the site is
            self.drawAssignmentMarker2(self.siteRect, color)  # Draw the marker around the site's actual location
        else:
            try:
                self.drawAssignmentMarker2(self.estimatedSiteRect, color)  # Draw the marker around where the agents think it is
            except:  # If the agents haven't estimated the position yet, an exception will be made.
                pass  # In that case, we just don't show anything

    def drawAssignmentMarker2(self, rect, color):
        """ Draw triangles around the site that point in toward the site """
        pyg.draw.polygon(self.screen, color,
                         [[rect.centerx, rect.top - 5],
                          [rect.centerx - 10, rect.top - 20],
                          [rect.centerx + 10, rect.top - 20]])
        pyg.draw.polygon(self.screen, color,
                         [[rect.centerx, rect.bottom + 5],
                          [rect.centerx - 10, rect.bottom + 20],
                          [rect.centerx + 10, rect.bottom + 20]])
        pyg.draw.polygon(self.screen, color,
                         [[rect.left - 5, rect.centery],
                          [rect.left - 20, rect.centery - 10],
                          [rect.left - 20, rect.centery + 10]])
        pyg.draw.polygon(self.screen, color,
                         [[rect.right + 5, rect.centery],
                          [rect.right + 20, rect.centery - 10],
                          [rect.right + 20, rect.centery + 10]])

    def setEstimates(self, est):
        """ Takes an array with each values' estimate and updates the site's estimated values """
        self.estimatedPosition = est[0]
        self.estimatedQuality = est[1]
        self.estimatedAgentCount = est[2]
        self.estimatedRadius = est[3]

    def drawEstimatedSite(self):
        """ Draws what the user knows about the site from the hub """
        # Only draw the site if it has been found, or if the site positions are all known at the start of the simulation
        if self.wasFound or self.knowSitePosAtStart:
            self.drawMarker()  # Draw the marker representing a command associated with the site
            # Draw a background behind the site to make it blend with the screen better
            self.drawBlurredSite(self.estimatedPosition, BORDER_COLOR, self.radius * 4,
                                 self.estimatedRadius + self.blurRadiusDiff + 2, self.blurAmount + 0.7)

            if self.isSelected:  # Draw the selection circle
                self.drawBlurredSite(self.estimatedPosition, SELECTED_COLOR, self.radius * 4,
                                     self.estimatedRadius + self.blurRadiusDiff + 2, self.blurAmount)

            color = self.getEstimatedColor()  # Gets a color based on the estimated value of the site
            self.drawBlurredSiteWithLines(self.estimatedPosition, color, self.radius * 4,
                                          self.estimatedRadius + self.blurRadiusDiff, self.blurAmount)  # Draws the site with lines representing the quality and blurriness representing how well known the site is

            img = pyg.font.SysFont('Comic Sans MS', 12).render(str(int(self.estimatedAgentCount)), True, BORDER_COLOR)  # Draw the estimated number of agents assigned to the site
            self.screen.blit(img, (self.estimatedPosition[0] - (img.get_width() / 2),
                                   self.estimatedPosition[1] - (self.estimatedRadius + self.blurRadiusDiff + 24)))

    def drawBlurredSite(self, pos, color, size, radius, blurAmount):
        """ Draws a blurry circle """
        image = pyg.Surface([size, size], pyg.SRCALPHA, 32)
        image = image.convert_alpha()
        pyg.draw.circle(image, color, (image.get_width() / 2, image.get_height() / 2), radius + 2, 0)
        blur = getBlurredImage(image, blurAmount)
        self.screen.blit(blur, (pos[0] - (blur.get_width() / 2), pos[1] - (blur.get_height() / 2)))

    def drawBlurredSiteWithLines(self, pos, color, size, radius, blurAmount):
        """ Draws a blurry circle with blurred lines """
        image = pyg.Surface([size, size], pyg.SRCALPHA, 32)
        image = image.convert_alpha()
        rect = pyg.draw.circle(image, color, (image.get_width() / 2, image.get_height() / 2), radius + 2, 0)
        drawCircleLines(image, rect, BORDER_COLOR, Site.getDensity(self.estimatedQuality))
        blur = getBlurredImage(image, blurAmount)
        self.estimatedSiteRect = self.screen.blit(blur, (pos[0] - (blur.get_width() / 2), pos[1] - (blur.get_height() / 2)))

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
        if siteQualities.count(self.quality) == 0:  # Only normalize if the quality was not manually set
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
