""" Classes and methods for supporting pygame """
import numpy
import numpy as np
import pygame

from Constants import AGENT_IMAGE


def createScreen(shouldDraw):
    """ Creates and returns the main screen that the simulation will be drawn on """
    if shouldDraw:
        pygame.display.init()
        pygame.font.init()
        return pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    else:
        return None


def drawCircleLines(screen, circle, color, inc):
    """ Draws vertical and horizontal lines on the circle with the specified color and distance between lines """
    drawVerticalCircleLines(screen, circle, color, inc)
    drawHorizontalCircleLines(screen, circle, color, inc)


def drawVerticalCircleLines(screen, circle, color, inc):
    """ Draws vertical lines on the circle with the specified color and distance between lines """
    x = circle.left
    r = (circle.height / 2)
    while x < circle.right:
        o = x - circle.left
        a = numpy.sqrt(numpy.abs(numpy.square(r) - numpy.square(r - o)))
        pygame.draw.line(screen, color, (x, circle.centery - a), (x,  circle.centery + a))
        x += inc


def drawHorizontalCircleLines(screen, circle, color, inc):
    """ Draws horizontal lines on the circle with the specified color and distance between lines """
    y = circle.top
    r = (circle.width / 2)
    while y < circle.bottom:
        o = y - circle.top
        a = numpy.sqrt(numpy.abs(numpy.square(r) - numpy.square(r - o)))
        pygame.draw.line(screen, color, (circle.centerx - a, y), (circle.centerx + a, y))
        y += inc


def getAgentImage(pos):
    """ Loads, adjusts the size, and returns the image representing an agent """
    agent = pygame.image.load(AGENT_IMAGE)
    if agent.get_size()[0] > 30 or agent.get_size()[1] > 30:
        agent = pygame.transform.scale(agent, (30, 30))
        rect = agent.get_rect().move(pos)
        rect.center = pos
    return agent


def getDestinationMarker(pos):
    """ Loads, adjusts the size, and returns the image representing a destination """
    arrows = pygame.image.load("resources/arrows.png")
    arrows = pygame.transform.scale(arrows, (30, 30))
    rect = arrows.get_rect().move(pos)
    rect.center = pos
    return arrows, rect


def drawDashedLine(surface, color, startPos, endPos, width=1, dashLength=10, excludeCorners=True):
    """ Draws a dashed line from startPos to endPos with the specified color on the given surface """
    # Convert tuples to numpy arrays
    startPos = np.array(startPos)
    endPos = np.array(endPos)

    # Get Euclidean distance between start_pos and end_pos
    length = np.linalg.norm(endPos - startPos)

    # Get number of pieces that line will be split up in (half of it are amount of dashes)
    numDashes = int(length / dashLength)

    # x-y-value-pairs of where dashes start (and on next, will end)
    dashKnots = np.array([np.linspace(startPos[i], endPos[i], numDashes) for i in range(2)]).transpose()

    return [pygame.draw.line(surface, color, tuple(dashKnots[n]), tuple(dashKnots[n+1]), width)
            for n in range(int(excludeCorners), numDashes - int(excludeCorners), 2)]


def getBlurredImage(surface, amount):
    """ Blur the given surface by the given 'amount'. Only values 1 and greater
    are valid. Value 1 = no blur. """
    if amount < 1.0:
        raise ValueError("Arg 'amount' must be greater than 1.0, passed in value is %s" % amount)
    scale = 1.0 / float(amount)
    surfSize = surface.get_size()
    scaleSize = (int(surfSize[0] * scale), int(surfSize[1] * scale))
    surf = pygame.transform.smoothscale(surface, scaleSize)
    surf = pygame.transform.smoothscale(surf, surfSize)
    return surf


def rotateImage(surf, image, pos, originPos, angle):
    """ Rotates the given image on the given surface at the given position to the given angle """
    # Calculate the axis aligned bounding box of the rotated image
    w, h = image.get_size()
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    boxRotate = [p.rotate(angle) for p in box]
    minBox = (min(boxRotate, key=lambda p: p[0])[0], min(boxRotate, key=lambda p: p[1])[1])
    maxBox = (max(boxRotate, key=lambda p: p[0])[0], max(boxRotate, key=lambda p: p[1])[1])

    # Calculate the translation of the pivot
    pivot = pygame.math.Vector2(originPos[0], -originPos[1])
    pivotRotate = pivot.rotate(angle)
    pivotMove = pivotRotate - pivot

    # Calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + minBox[0] - pivotMove[0], pos[1] - originPos[1] - maxBox[1] + pivotMove[1])
    # Get a rotated image
    rotatedImage = pygame.transform.rotate(image, angle)
    # Rotate and blit the image
    surf.blit(rotatedImage, origin)
