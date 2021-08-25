""" Settings and methods related to the display """
import numpy
import numpy as np
import pygame

from Constants import AGENT_IMAGE, SHOULD_DRAW, DRAW_FAR_AGENTS, WORDS_COLOR, SHOULD_DRAW_PATHS, LARGE_FONT_SIZE

screen = None
shouldDraw = SHOULD_DRAW
shouldDrawPaths = SHOULD_DRAW_PATHS
canSelectAnywhere = DRAW_FAR_AGENTS
drawFarAgents = DRAW_FAR_AGENTS
displacementX = 0
displacementY = 0
drawLastCommands = []
zoom = 0
origWidth = 0
origHeight = 0
newWidth = 0
newHeight = 0


def createScreen():
    """ Creates and returns the main screen that the interface will be drawn on """
    global screen
    global origWidth
    global origHeight
    global newWidth
    global newHeight
    pygame.display.init()
    pygame.font.init()
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    origWidth = screen.get_width()
    origHeight = screen.get_height()
    newWidth = origWidth
    newHeight = origHeight
    return screen


def writeBigCenter(surface, words):
    font = pygame.font.SysFont('Comic Sans MS', LARGE_FONT_SIZE)
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


def drawVerticalCircleLines(surface, circle, color, inc, adjust=True):
    """ Draws vertical lines on the circle with the specified color and distance between lines """
    x = circle.left
    r = (circle.height / 2)
    while x < circle.right:
        o = x - circle.left
        a = numpy.sqrt(numpy.abs(numpy.square(r) - numpy.square(r - o)))
        drawLine(surface, color, (x, circle.centery - a), (x,  circle.centery + a), adjust=adjust)
        x += inc


def drawHorizontalCircleLines(surface, circle, color, inc, adjust=True):
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
    agent = pygame.image.load(AGENT_IMAGE)
    if shouldDraw:
        agent = agent.convert_alpha()
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


def drawRect(surf, color, rect, width=0, adjust=True):
    if not adjust:
        rectangle = rect
    else:
        left, top = getAdjustedPos(rect.left, rect.top)
        w, h = getZoomedSize(rect.width, rect.height)
        rectangle = pygame.Rect(left, top, w, h)
    return pygame.draw.rect(surf, color, rectangle, width)


def drawCircle(surface, color, pos, radius, width=0, adjust=True):
    if not adjust:
        position = pos
    else:
        position = getAdjustedPos(pos[0], pos[1])
        radius = getZoomedSize(radius, radius)[0]
    return pygame.draw.circle(surface, color, position, radius, width)


def drawPolygon(surface, color, positions, adjust=True):
    newPositions = []
    if adjust:
        for pos in positions:
            newPositions.append(getAdjustedPos(pos[0], pos[1]))
    else:
        for pos in positions:
            newPositions.append([pos[0], pos[1]])
    return pygame.draw.polygon(surface, color, newPositions)


def drawLine(surface, color, startPos, endPos, width=1, adjust=True):
    if not adjust:
        return pygame.draw.line(surface, color, startPos, endPos, width)
    pos0 = getAdjustedPos(startPos[0], startPos[1])
    pos1 = getAdjustedPos(endPos[0], endPos[1])
    return pygame.draw.line(surface, color, pos0, pos1, width)


def blitImage(surface, source, destination, adjust=True):
    if adjust:
        try:
            dest = getAdjustedPos(destination[0], destination[1])
            source = pygame.transform.scale(source, getZoomedSize(source.get_width(), source.get_height()))
        except:
            dest = getAdjustedPos(destination.left, destination.top)
            source = pygame.transform.scale(source, getZoomedSize(destination.width, destination.height))
    else:
        dest = destination
    return surface.blit(source, dest)


def drawRightArrow(pos, color, adjust=True):
    drawPolygon(screen, color,
                [[pos[0], pos[1]],
                 [pos[0] - 20, pos[1] - 10],
                 [pos[0] - 20, pos[1] + 10]],
                adjust)


def drawUpArrow(pos, color, adjust=True):
    drawPolygon(screen, color,
                [[pos[0], pos[1]],
                 [pos[0] - 10, pos[1] + 20],
                 [pos[0] + 10, pos[1] + 20]],
                adjust)


def drawLeftArrow(pos, color, adjust=True):
    drawPolygon(screen, color,
                [[pos[0], pos[1]],
                 [pos[0] + 20, pos[1] - 10],
                 [pos[0] + 20, pos[1] + 10]],
                adjust)


def drawDownArrow(pos, color, adjust=True):
    drawPolygon(screen, color,
                [[pos[0], pos[1]],
                 [pos[0] - 10, pos[1] - 20],
                 [pos[0] + 10, pos[1] - 20]],
                adjust)


def addToDrawLast(command, arg1=None, arg2=None, adjust=None):
    global drawLastCommands
    drawLastCommands.append([command, arg1, arg2, adjust])


def drawLast():
    global drawLastCommands
    for command in drawLastCommands:
        if command[1] is None:
            command[0]()
        elif command[2] is None:
            command[0](command[1])
        elif command[3] is None:
            command[0](command[1], command[2])
        else:
            command[0](command[1], command[2], command[3])
    drawLastCommands = []


def zoomIn():
    global newWidth
    global newHeight
    global zoom
    if newWidth < 2000:
        zoom += 10
        newWidth = int(screen.get_width() + ((zoom / 100) * screen.get_width()))
        newHeight = int(screen.get_height() + ((zoom / 100) * screen.get_height()))


def zoomOut():
    global newWidth
    global newHeight
    global zoom
    if newWidth > 200 or newWidth == 0:
        zoom -= 10
        newWidth = int(screen.get_width() + ((zoom / 100) * screen.get_width()))
        newHeight = int(screen.get_height() + ((zoom / 100) * screen.get_height()))


def getAdjustedPos(origX, origY):
    newX = ((origX + displacementX) / origWidth) * newWidth
    newY = ((origY + displacementY) / origHeight) * newHeight
    return [newX, newY]


def getReadjustedPos(origX, origY):
    newX = (origX / newWidth) * origWidth - displacementX
    newY = (origY / newHeight) * origHeight - displacementY
    return [newX, newY]


def getZoomedSize(origW, origH):
    newW = int((origW / origWidth) * newWidth)
    newH = int((origH / origHeight) * newHeight)
    return [newW, newH]


def getUnzoomedSize(origW, origH):
    newW = int((origW / newWidth) * origWidth)
    newH = int((origH / newHeight) * origHeight)
    return [newW, newH]
