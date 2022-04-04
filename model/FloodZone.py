import copy
import random

import pygame
from numpy import pi, square, sin
from pygame import mask, SRCALPHA
from shapely.geometry import Polygon

import Utils
from display import Display, FloodZoneDisplay
from config import Config


class FloodZone:
    def __init__(self, hubPosition):
        self.coverage = Config.FLOOD_ZONE_COVERAGE
        self.corners = Config.FLOOD_ZONE_CORNERS
        self.center = copy.copy(hubPosition)

        if len(self.corners) < 3:
            self.corners = self.generateCorners(random.randint(0, 3))
            print(f"Corners: {self.corners}")

        for corner in self.corners:
            corner[0] -= Display.worldLeft
            corner[1] -= Display.worldTop

        self.surface = pygame.Surface(Display.worldSize, SRCALPHA)
        self.rect = FloodZoneDisplay.initFloodZoneDisplay(self.surface, self.corners)
        self.mask = mask.from_surface(self.surface, threshold=50)

    def generateCorners(self, shape):
        if shape == 0:
            return self.generateSector()
        if shape == 1:
            return self.generateSegment()
        elif shape == 2:
            return self.generateRiver()
        else:
            return self.generatePolygon()

    def generateSector(self):
        angle = self.coverage * 2 * pi  # Get the angle from the coverage percentage
        startAngle = random.uniform(0, 2 * pi)  # Get a random start angle
        endAngle = startAngle + angle
        positions = [self.center]
        angle = startAngle
        angleDiff1 = Utils.getAngleDiff(endAngle, startAngle) / 15
        angleDiff2 = (2 * pi - Utils.getAngleDiff(startAngle, endAngle)) / 15
        for _ in range(16):
            positions.append(Utils.getNextPosition(self.center, Config.MAX_SEARCH_DIST + Config.SITE_RADIUS, angle))
            if self.coverage <= 0.5:
                angle += angleDiff1
            else:
                angle += angleDiff2

        return positions

    def generateSegment(self):
        explorableArea = pi * square(Config.MAX_SEARCH_DIST)  # The area of the circle the ants can move around in
        desiredArea = explorableArea * self.coverage  # How much area we want to cover with the flood zone in the circle
        sectorAngle = 2 * (desiredArea / square(Config.MAX_SEARCH_DIST))  # this is an underestimate if coverage is less than 50%, else overestimate

        if self.coverage < 0.5:
            sectorAngle = self.calcAcuteSectorAngle(sectorAngle, desiredArea)
        elif self.coverage > 0.5:
            sectorAngle = self.calcObtuseSectorAngle(explorableArea, sectorAngle, desiredArea)

        startAngle = random.uniform(0, 2 * pi)  # Get a random angle
        endAngle = startAngle + sectorAngle
        positions = []
        angle = startAngle
        for _ in range(16):
            positions.append(Utils.getNextPosition(self.center, Config.MAX_SEARCH_DIST + Config.SITE_RADIUS, angle))
            if self.coverage <= 0.5:
                angle += Utils.getAngleDiff(endAngle, startAngle) / 15
            else:
                angle += (2 * pi - Utils.getAngleDiff(endAngle, startAngle)) / 15

        return positions

    @staticmethod
    def calcAcuteSectorAngle(sectorAngle, desiredArea):
        segmentArea = 0

        while segmentArea < desiredArea:
            sectorArea = square(Config.MAX_SEARCH_DIST) * (sectorAngle / 2)
            base = Config.MAX_SEARCH_DIST * (sin(sectorAngle) / sin((2 * pi - sectorAngle) / 2))  # Base of the triangle to add in or subtract out
            height = Config.MAX_SEARCH_DIST * sin((2 * pi - sectorAngle) / 2)
            triangleArea = base * height / 2

            segmentArea = sectorArea - triangleArea
            sectorAngle += 0.05

        return sectorAngle % (2 * pi)

    def calcObtuseSectorAngle(self, explorableArea, sectorAngle, desiredArea):
        return self.calcAcuteSectorAngle((2 * pi - sectorAngle), explorableArea - desiredArea)

    def generateRiver(self):
        explorableArea = pi * square(Config.MAX_SEARCH_DIST + Config.SITE_RADIUS)  # The area of the circle the ants can move around in
        desiredArea = explorableArea * self.coverage  # How much area we want to cover with the flood zone in the circle
        startAngle = random.uniform(0, 2 * pi)  # Get a random angle relative to hub
        endAngle = random.uniform(0, 2 * pi)  # Get a random angle relative to hub
        angle = startAngle
        positions = []
        angleDiff = (2 * pi - abs(Utils.getAngleDiff(startAngle, endAngle))) / 15
        for _ in range(16):
            positions.append(Utils.getNextPosition(self.center, Config.MAX_SEARCH_DIST + Config.SITE_RADIUS, angle))
            angle += angleDiff

        area = self.pointsToPolygonArea(positions)
        print(f"Too big: {desiredArea < area}")
        if desiredArea < area:
            return self.getSmallerRiver(desiredArea, area, startAngle, endAngle, positions)
        elif self.coverage <= 0.97:
            return self.getBiggerRiver(desiredArea, area, startAngle, endAngle, positions)
        else:
            return self.getFullCoverage()

    def getSmallerRiver(self, desiredArea, area, startAngle, endAngle, positions):
        print("Get smaller river")
        angleDiff = (2 * pi - abs(Utils.getAngleDiff(startAngle, endAngle))) / 15
        extraAngle = 0
        while desiredArea < area:
            angle = startAngle
            positions = []
            angleDiff -= 0.005
            extraAngle += 0.08
            for _ in range(8):
                positions.append(Utils.getNextPosition(self.center, Config.MAX_SEARCH_DIST + Config.SITE_RADIUS, angle))
                angle += angleDiff
            angle += extraAngle
            for _ in range(8):
                positions.append(Utils.getNextPosition(self.center, Config.MAX_SEARCH_DIST + Config.SITE_RADIUS, angle))
                angle += angleDiff

            area = self.pointsToPolygonArea(positions)
        return positions

    def getBiggerRiver(self, desiredArea, area, startAngle, endAngle, positions):
        print("Get bigger river")
        while desiredArea > area:
            startAngle += 0.005
            endAngle -= 0.005
            angle = startAngle
            positions = []
            angleDiff = (2 * pi - abs(Utils.getAngleDiff(startAngle, endAngle))) / 15
            for _ in range(16):
                positions.append(Utils.getNextPosition(self.center, Config.MAX_SEARCH_DIST + Config.SITE_RADIUS, angle))
                angle += angleDiff
            area = self.pointsToPolygonArea(positions)
        return positions

    def pointsToPolygonArea(self, points):
        x = []
        y = []
        for point in points:
            x.append(point[0])
            y.append(point[1])
        return Polygon(zip(x, y)).area

    def generatePolygon(self):
        # TODO
        return [[Display.worldLeft, Display.worldTop],
                [Display.worldLeft, Display.worldBottom],
                [Display.origWidth / 2 - Config.MAX_SEARCH_DIST, Display.worldBottom],
                [Display.origWidth / 2, Display.worldTop]]

    def getFullCoverage(self):
        positions = []
        angle = 0
        angleDiff = 2 * pi / 32
        for _ in range(32):
            positions.append(Utils.getNextPosition(self.center, Config.MAX_SEARCH_DIST + Config.SITE_RADIUS, angle))
            angle += angleDiff
        return positions

    def overlaps(self, rect, radius):
        offset = Display.worldLeft - rect[0], Display.worldTop - rect[1]

        surface = pygame.Surface((radius * 2, radius * 2), SRCALPHA)
        Display.drawCircle(surface, (0, 0, 0), [rect.w / 2, rect.h / 2],
                           rect.w / 2, adjust=False)
        otherMask = mask.from_surface(surface, threshold=50)

        return otherMask.overlap(self.mask, offset) is not None
