""" Settings and methods related to the display """
import numpy
import numpy as np
import pygame

from Constants import AGENT_IMAGE, SHOULD_DRAW, DRAW_FAR_AGENTS, WORDS_COLOR, SHOULD_DRAW_PATHS

screen = None
shouldDraw = SHOULD_DRAW
shouldDrawPaths = SHOULD_DRAW_PATHS
canSelectAnywhere = DRAW_FAR_AGENTS
drawFarAgents = DRAW_FAR_AGENTS
displacementX = 0
displacementY = 0


def createScreen():
    """ Creates and returns the main screen that the interface will be drawn on """
    pygame.display.init()
    pygame.font.init()
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])
    return pygame.display.set_mode((0, 0), pygame.RESIZABLE)


def writeBigCenter(surface, words):
    font = pygame.font.SysFont('Comic Sans MS', 40)
    img = font.render(words, True, WORDS_COLOR).convert_alpha()
    surface.blit(img, (surface.get_size()[0] / 2 - (img.get_width() / 2),
                       surface.get_size()[1] / 2 - (img.get_height() / 2) - 60))


def drawPause(surface):
    writeBigCenter(surface, "Paused")


def drawFinish(surface):
    writeBigCenter(surface, "Finish")


def drawCircleLines(surface, circle, color, inc, adjust=True):
    """ Draws vertical and horizontal lines on the circle with the specified color and distance between lines """
    drawVerticalCircleLines(surface, circle, color, inc, adjust)
    drawHorizontalCircleLines(surface, circle, color, inc, adjust)


def drawVerticalCircleLines(surface, circle, color, inc, adjust):
    """ Draws vertical lines on the circle with the specified color and distance between lines """
    x = circle.left
    r = (circle.height / 2)
    while x < circle.right:
        o = x - circle.left
        a = numpy.sqrt(numpy.abs(numpy.square(r) - numpy.square(r - o)))
        drawLine(surface, color, (x, circle.centery - a), (x,  circle.centery + a), adjust=adjust)
        x += inc


def drawHorizontalCircleLines(surface, circle, color, inc, adjust):
    """ Draws horizontal lines on the circle with the specified color and distance between lines """
    y = circle.top
    r = (circle.width / 2)
    while y < circle.bottom:
        o = y - circle.top
        a = numpy.sqrt(numpy.abs(numpy.square(r) - numpy.square(r - o)))
        drawLine(surface, color, (circle.centerx - a, y), (circle.centerx + a, y), adjust=adjust)
        y += inc


def getAgentImage(pos):
    """ Loads, adjusts the size, and returns the image representing an agent """
    agent = pygame.image.load(AGENT_IMAGE).convert_alpha()
    if agent.get_size()[0] > 30 or agent.get_size()[1] > 30:
        agent = pygame.transform.scale(agent, (30, 30))
        rect = agent.get_rect().move(pos)
        rect.center = pos
    return agent


def getDestinationMarker(pos):
    """ Loads, adjusts the size, and returns the image representing a destination """
    arrows = pygame.image.load("resources/arrows.png").convert_alpha()
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

    return [drawLine(surface, color, tuple(dashKnots[n]), tuple(dashKnots[n+1]), width)
            for n in range(int(excludeCorners), numDashes - int(excludeCorners), 2)]


def getBlurredImage(surface, amount):
    """ Blur the given surface by the given 'amount'. Only values 1 and greater
    are valid. Value 1 = no blur. """
    if amount < 1.0:
        raise ValueError("Arg 'amount' must be greater than 1.0, passed in value is %s" % amount)
    scale = 1.0 / float(amount)
    surfSize = surface.get_size()
    scaleSize = (int(surfSize[0] * scale), int(surfSize[1] * scale))
    surface = pygame.transform.smoothscale(surface, scaleSize)
    surface = pygame.transform.smoothscale(surface, surfSize)
    return surface


def rotateImage(surface, image, pos, originPos, angle):
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
    blitImage(surface, rotatedImage, origin)


def drawRect(img, color, rect, width=0):
    rectangle = pygame.Rect(rect.left + displacementX, rect.top + displacementY, rect.width, rect.height)
    return pygame.draw.rect(img, color, rectangle, width)


def drawCircle(surface, color, pos, radius, width=0):
    position = [pos[0] + displacementX, pos[1] + displacementY]
    return pygame.draw.circle(surface, color, position, radius, width)


def drawPolygon(surface, color, positions):
    newPositions = []
    for pos in positions:
        newPositions.append([pos[0] + displacementX, pos[1] + displacementY])
    return pygame.draw.polygon(surface, color, newPositions)


def drawLine(surface, color, startPos, endPos, width=1, adjust=True):
    if not adjust:
        return pygame.draw.line(surface, color, startPos, endPos, width)
    pos0 = [startPos[0] + displacementX, startPos[1] + displacementY]
    pos1 = [endPos[0] + displacementX, endPos[1] + displacementY]
    return pygame.draw.line(surface, color, pos0, pos1, width)


def blitImage(surface, source, destination):
    try:
        dest = [destination[0] + displacementX, destination[1] + displacementY]
    except:
        dest = [destination.left + displacementX, destination.top + displacementY]
    return surface.blit(source, dest)
