import copy
import random
from operator import lt, gt

import pygame
from numpy import pi, square, sqrt, sin
from pygame import mask, SRCALPHA
from shapely.geometry import Polygon

import Utils
from Constants import ANY, SHAPE_CHOICES, SECTOR, SEGMENT, RIVER, SCREEN_COLOR, FOG_COLOR, FLOOD_ZONE_COLOR
from display import Display
from display.simulation import FloodZoneDisplay
from config import Config


class FloodZone:
    """ A semi-transparent shape on the screen indicating where floods are likely to occur. Agents do not know about
    this, but users do. It is the user's responsibility to make sure that the agents do not end up at a site that is
    in the flood zone. The flood zone can be generated in various shapes, including sector, segment, river, and
    polygon. """

    def __init__(self):
        self.coverage = Config.FLOOD_ZONE_COVERAGE
        self.corners = copy.deepcopy(Config.FLOOD_ZONE_CORNERS)
        self.center = [Display.origWidth / 2, Display.origHeight / 2]

        if len(self.corners) < 3 and self.coverage > 0.0:
            self.numCorners = 32
            self.explorableRadius = Config.MAX_SEARCH_DIST
            self.explorableArea = pi * square(self.explorableRadius)  # The area of the circle the ants can move around in
            self.desiredArea = self.explorableArea * self.coverage  # How much area we want to cover with the flood zone in the circle
            self.corners = self.generateCorners(Config.FLOOD_ZONE_SHAPE)

        for corner in self.corners:
            corner[0] -= Display.worldLeft
            corner[1] -= Display.worldTop

        self.surface = pygame.Surface(Display.worldSize, SRCALPHA)
        if len(self.corners) >= 3:
            FloodZoneDisplay.initFloodZoneDisplay(self.surface, self.corners)
            self.mask = mask.from_surface(self.surface, threshold=50)

    def overlaps(self, rect, radius):
        if self.coverage == 0.0:
            return False
        offset = Display.worldLeft - rect[0], Display.worldTop - rect[1]

        surface = pygame.Surface((radius * 2, radius * 2), SRCALPHA)
        Display.drawCircle(surface, (0, 0, 0), [rect.w / 2, rect.h / 2],
                           rect.w / 2, adjust=False)
        otherMask = mask.from_surface(surface, threshold=50)

        return otherMask.overlap(self.mask, offset) is not None

    def generateCorners(self, shape):
        while shape == ANY:
            shape = random.choice(SHAPE_CHOICES)
        if shape == SECTOR:
            return self.generateSector()
        elif shape == SEGMENT:
            return self.generateSegment()
        elif shape == RIVER:
            return self.generateRiver()
        else:
            return self.generatePolygon()

    def getCircularPoints(self, positions, angle, angleDiffSmall, angleDiffBig, extraAngle=0.0):
        for _ in range(int(self.numCorners / 2)):
            positions.append(Utils.getNextPosition(self.center, self.explorableRadius, angle))
            if self.coverage <= 0.5:
                angle += angleDiffSmall
            else:
                angle += angleDiffBig
        angle += extraAngle
        for _ in range(int(self.numCorners / 2)):
            positions.append(Utils.getNextPosition(self.center, self.explorableRadius, angle))
            if self.coverage <= 0.5:
                angle += angleDiffSmall
            else:
                angle += angleDiffBig
        return positions

    def generateSector(self):
        angle = self.coverage * 2 * pi  # Get the angle from the coverage percentage
        startAngle = random.uniform(0, 2 * pi)  # Get a random start angle
        endAngle = startAngle + angle
        angleDiffSmall = Utils.getAngleDiff(endAngle, startAngle) / (self.numCorners - 1)
        angleDiffBig = (2 * pi - Utils.getAngleDiff(startAngle, endAngle)) / (self.numCorners - 1)
        return self.getCircularPoints([self.center], startAngle, angleDiffSmall, angleDiffBig)

    def generateSegment(self):
        sectorAngle = 2 * (self.desiredArea / square(Config.MAX_SEARCH_DIST))

        if self.coverage < 0.5:
            sectorAngle = self.calcAcuteSectorAngle(sectorAngle, self.desiredArea)
        elif self.coverage > 0.5:
            sectorAngle = self.calcObtuseSectorAngle(sectorAngle)

        startAngle = random.uniform(0, 2 * pi)  # Get a random angle
        endAngle = startAngle + sectorAngle
        angleDiffSmall = Utils.getAngleDiff(endAngle, startAngle) / (self.numCorners - 1)
        angleDiffBig = (2 * pi - Utils.getAngleDiff(endAngle, startAngle)) / (self.numCorners - 1)
        return self.getCircularPoints([], startAngle, angleDiffSmall, angleDiffBig)

    @staticmethod
    def calcAcuteSectorAngle(sectorAngle, desiredArea):
        segmentArea = 0

        while segmentArea < desiredArea:
            sectorArea = square(Config.MAX_SEARCH_DIST) * (sectorAngle / 2)
            base = Config.MAX_SEARCH_DIST * (sin(sectorAngle) / sin(
                (2 * pi - sectorAngle) / 2))  # Base of the triangle to add in or subtract out
            height = Config.MAX_SEARCH_DIST * sin((2 * pi - sectorAngle) / 2)
            triangleArea = base * height / 2

            segmentArea = sectorArea - triangleArea
            sectorAngle += 0.01

        return sectorAngle % (2 * pi)

    def calcObtuseSectorAngle(self, sectorAngle):
        return self.calcAcuteSectorAngle((2 * pi - sectorAngle), self.explorableArea - self.desiredArea)

    def generateRiver(self):
        startAngle = random.uniform(0, 2 * pi)  # Get a random angle relative to hub
        endAngle = random.uniform(0, 2 * pi)  # Get a random angle relative to hub
        angleDiff = (2 * pi - abs(Utils.getAngleDiff(startAngle, endAngle))) / (self.numCorners - 1)
        positions = self.getCircularPoints([], startAngle, angleDiff, angleDiff)

        area = self.pointsToPolygonArea(positions)
        if self.desiredArea < area:
            return self.getSmallerRiver(area, startAngle, endAngle, positions)
        elif self.coverage <= 0.97:
            return self.getBiggerRiver(area, startAngle, endAngle, positions)
        else:
            return self.getFullCoverage()

    def getSmallerRiver(self, area, startAngle, endAngle, positions):
        angleDiff = (2 * pi - abs(Utils.getAngleDiff(startAngle, endAngle))) / (self.numCorners - 1)
        extraAngle = 0
        while self.desiredArea < area:
            angleDiff -= 0.005
            extraAngle += 0.08
            positions = self.getCircularPoints([], startAngle, angleDiff, angleDiff, extraAngle)

            area = self.pointsToPolygonArea(positions)
        return positions

    def getBiggerRiver(self, area, startAngle, endAngle, positions):
        while self.desiredArea > area:
            startAngle += 0.005
            endAngle -= 0.005
            angleDiff = (2 * pi - abs(Utils.getAngleDiff(startAngle, endAngle))) / (self.numCorners - 1)
            positions = self.getCircularPoints([], startAngle, angleDiff, angleDiff)
            area = self.pointsToPolygonArea(positions)
        return positions

    def getFullCoverage(self):
        angleDiff = 2 * pi / self.numCorners
        return self.getCircularPoints([], 0, angleDiff, angleDiff)

    @staticmethod
    def pointsToPolygonArea(points):
        x = []
        y = []
        for point in points:
            x.append(point[0])
            y.append(point[1])
        return Polygon(zip(x, y)).area

    def generatePolygon(self):
        averageRadius = sqrt((self.explorableArea * self.coverage) / pi)
        irregularity = 1 - self.coverage if self.coverage > 0.5 else random.uniform(0, 1)
        spikiness = 1 - self.coverage if self.coverage > 0.5 else random.uniform(0, 1)
        minVertices = 3 if int(self.coverage * 10) < 3 else int(self.coverage * 10)
        maxVertices = 6 if int(self.coverage * 100 / 3) < 6 else int(self.coverage * 100 / 3)
        numVertices = random.randint(minVertices, maxVertices)
        center = self.generateCenter()
        positions = createPolygon(center, averageRadius, irregularity, spikiness, numVertices)
        positions = self.resizePolygon(positions)
        return positions

    def generateCenter(self):
        radius = int(self.explorableRadius * (1 - self.coverage))  # Cut the radius in half so that the center isn't so far out.
        centerX = random.randint(-radius, radius)  # Center x coordinate relative to (0, 0)
        maxY = int(sqrt(square(radius) - square(centerX)))
        centerY = random.randint(-maxY, maxY)  # Center y coordinate relative to (0, 0)
        return [centerX + self.center[0], centerY + self.center[1]]  # Add the center of the simulation to make the center relative to that.

    def resizePolygon(self, positions):
        # Create surface with the circle that represents the area that can be explored
        explorableSurf = pygame.Surface(Display.worldSize, SRCALPHA)
        center = [self.center[0] - Display.worldLeft, self.center[1] - Display.worldTop]
        Display.drawCircle(explorableSurf, SCREEN_COLOR, center, self.explorableRadius, adjust=False)

        # Convert that surface to a Mask of the same size as the previous one
        circleMask = mask.from_surface(explorableSurf)

        # Calculate the number of pixels needed to cover self.coverage% of the explorable area
        desiredAreaPixels = circleMask.overlap_area(circleMask, (0, 0)) * self.coverage

        # Generate a polygon that is roughly the right size and see if it is too big or too small
        origOverlap, _ = getPolygonOverlap(positions, circleMask)
        compare = lt if origOverlap < desiredAreaPixels else gt
        move = movePositionsOut if origOverlap < desiredAreaPixels else movePositionsIn
        overlap = origOverlap

        #  If it's too small, move each point out from the center a little; else, move them inward
        while compare(overlap, desiredAreaPixels):
            center = Utils.getAveragePos(positions)
            positions = move(positions, center)
            overlap, polySurf = getPolygonOverlap(positions, circleMask)
            debugPolyGen(explorableSurf, polySurf)
            # There are a few shapes that will put this in an infinite loop, so we should just try again if it goes too long.
            if compare(overlap, origOverlap):
                return self.generatePolygon()

        return positions


def debugPolyGen(explorableSurf, polySurf):
    """ Draw the surfaces on the screen to see how generation is going """
    Display.screen.fill(FOG_COLOR)
    Display.blitImage(Display.screen, explorableSurf, (Display.worldLeft, Display.worldTop))
    Display.blitImage(Display.screen, polySurf, (Display.worldLeft, Display.worldTop))
    pygame.display.flip()


def getPolygonOverlap(positions, circleMask):
    # Draw positions on a surface
    surface = pygame.Surface(Display.worldSize, SRCALPHA)
    drawingPositions = [[pos[0] - Display.worldLeft, pos[1] - Display.worldTop] for pos in positions]
    Display.drawPolygon(surface, FLOOD_ZONE_COLOR[0:3], drawingPositions, adjust=False)
    # Convert that surface to a Mask
    polyMask = mask.from_surface(surface)
    # Get the area of the overlap
    return polyMask.overlap_area(circleMask, (0, 0)), surface


def movePositionsIn(positions, center):
    return [Utils.getNextPosition(pos, 10, Utils.getAngleFromPositions(pos, center)) for pos in positions]


def movePositionsOut(positions, center):
    return [Utils.getNextPosition(pos, 10, Utils.getAngleFromPositions(center, pos)) for pos in positions]


# The rest of this is taken from https://stackoverflow.com/questions/8997099/algorithm-to-generate-random-2d-polygon
# and slightly adjusted
import math
from typing import List, Tuple


def createPolygon(center: List[float], avgRadius: float,
                  irregularity: float, spikiness: float,
                  numVertices: int) -> List[List[float]]:
    """ Start with the center of the polygon at center, then creates the
    polygon by sampling points on a circle around the center.
    Random noise is added by varying the angular spacing between
    sequential points, and by varying the radial distance of each
    point from the centre.

    Args:
        center (Tuple[float, float]):
            a pair representing the center of the circumference used
            to generate the polygon.
        avgRadius (float):
            the average radius (distance of each generated vertex to
            the center of the circumference) used to generate points
            with a normal distribution.
        irregularity (float):
            variance of the spacing of the angles between consecutive
            vertices.
        spikiness (float):
            variance of the distance of each vertex to the center of
            the circumference.
        numVertices (int):
            the number of vertices of the polygon.
    Returns:
        List[Tuple[float, float]]: list of vertices, in CCW order. """
    # Parameter check
    if irregularity < 0 or irregularity > 1:
        raise ValueError("Irregularity must be between 0 and 1.")
    if spikiness < 0 or spikiness > 1:
        raise ValueError("Spikiness must be between 0 and 1.")

    irregularity *= 2 * math.pi / numVertices
    spikiness *= avgRadius
    angleSteps = randomAngleSteps(numVertices, irregularity)

    # now generate the points
    points = []
    angle = random.uniform(0, 2 * math.pi)
    for i in range(numVertices):
        radius = clip(random.gauss(avgRadius, spikiness), 0, 2 * avgRadius)
        point = [center[0] + radius * math.cos(angle),
                 center[1] + radius * math.sin(angle)]
        points.append(point)
        angle += angleSteps[i]

    return points


def randomAngleSteps(steps: int, irregularity: float) -> List[float]:
    """ Generates the division of a circumference in random angles.
    Args:
        steps (int):
            the number of angles to generate.
        irregularity (float):
            variance of the spacing of the angles between consecutive vertices.
    Returns:
        List[float]: the list of the random angles. """
    # generate n angle steps
    angles = []
    lower = (2 * math.pi / steps) - irregularity
    upper = (2 * math.pi / steps) + irregularity
    cumsum = 0
    for i in range(steps):
        angle = random.uniform(lower, upper)
        angles.append(angle)
        cumsum += angle

    # normalize the steps so that point 0 and point n+1 are the same
    cumsum /= (2 * math.pi)
    for i in range(steps):
        angles[i] /= cumsum
    return angles


def clip(value, lower, upper):
    """ Given an interval, values outside the interval are clipped to the interval
    edges. """
    return min(upper, max(value, lower))
