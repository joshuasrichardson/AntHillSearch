""" Settings and methods related to the display """

import numpy as np
import pygame

from Constants import SHOULD_DRAW, DRAW_FAR_AGENTS, WORDS_COLOR, SHOULD_DRAW_PATHS, LARGE_FONT_SIZE, \
    SITE_RADIUS, FONT_SIZE, MIN_AVOID_DIST

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
    if not pygame.display.get_init():
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
    writeCenter(surface, words, LARGE_FONT_SIZE)


def writeCenter(surface, words, fontSize):
    font = pygame.font.SysFont('Comic Sans MS', fontSize)
    img = font.render(f"{words}", True, WORDS_COLOR).convert_alpha()
    surface.blit(img, (surface.get_size()[0] / 2 - (img.get_width() / 2),
                       surface.get_size()[1] / 2 - (img.get_height() / 2) - 60))
    del img


def writeCenterPlus(surface, words, fontSize, y):
    font = pygame.font.SysFont('Comic Sans MS', fontSize)
    img = font.render(f"{words}", True, WORDS_COLOR).convert_alpha()
    return surface.blit(img, (surface.get_size()[0] / 2 - (img.get_width() / 2),
                        surface.get_size()[1] / 2 - (img.get_height() / 2) - 60 + y))


def write(surface, words, fontSize, x, y, color=WORDS_COLOR):
    font = pygame.font.SysFont('Comic Sans MS', fontSize)
    img = font.render(f"{words}", True, color).convert_alpha()
    return surface.blit(img, (x, y))


def drawPause(surface):
    writeBigCenter(surface, "Paused")


def drawFinish(surface, results):
    surf = pygame.Surface((origWidth, origHeight), pygame.SRCALPHA)
    pygame.draw.rect(surf, (225, 220, 190, 200), (0, 0, origWidth, origHeight))  # Draw partially transparent surface over the screen
    surface.blit(surf, (0, 0))

    writeBigCenter(surface, "Complete")

    x = origWidth * 4 / 9
    y = origHeight / 2 - 2 * FONT_SIZE
    simDuration = round(results[1], 2)
    write(surface, "Click anywhere or press", FONT_SIZE, x, y)
    y += FONT_SIZE
    write(surface, "any key to continue.", FONT_SIZE, x, y)
    y += FONT_SIZE * 2
    if simDuration == 10000:
        write(surface, "The ants did not move in time.", FONT_SIZE, x, y)
    else:
        write(surface, "Simulation Duration: " + str(simDuration), FONT_SIZE, x, y)
    y += FONT_SIZE

    for i, quality in enumerate(results[0]):
        y += FONT_SIZE
        write(surface, f"Colony {i + 1}'s Site Quality: {quality}", FONT_SIZE, x, y)

    y += FONT_SIZE
    write(surface, f"{results[2]}/{results[4]} agents made it to the new site.", FONT_SIZE, x, y)

    y += FONT_SIZE
    write(surface, f"{results[4] - results[3]}/{results[4]} agents survived.", FONT_SIZE, x, y)


def getDestinationMarker(pos):
    """ Loads, adjusts the size, and returns the image representing a destination """
    arrows = pygame.image.load("resources/arrows.png").convert_alpha()
    if arrows.get_size()[0] > 30 or arrows.get_size()[1] > 30:
        arrows = pygame.transform.scale(arrows, (30, 30))
    rect = arrows.get_rect().move(pos)
    rect.center = pos
    return arrows, rect


def getAvoidMarker(pos):
    """ Loads, adjusts the size, and returns the image representing a place to avoid """
    avoidPlace = pygame.image.load("resources/avoid.png").convert_alpha()
    if avoidPlace.get_size()[0] > 2 * MIN_AVOID_DIST or avoidPlace.get_size()[1] > 2 * MIN_AVOID_DIST:
        avoidPlace = pygame.transform.scale(avoidPlace, (2 * MIN_AVOID_DIST, 2 * MIN_AVOID_DIST))
    rect = avoidPlace.get_rect().move(pos)
    rect.center = pos
    return avoidPlace, rect


def getAssignmentMarker(pos):
    """ Loads, adjusts the size, and returns the image representing an assignment """
    target = pygame.image.load("resources/target.png").convert_alpha()
    if target.get_size()[0] > 2 * SITE_RADIUS or target.get_size()[1] > 2 * SITE_RADIUS:
        target = pygame.transform.scale(target, (2 * SITE_RADIUS, 2 * SITE_RADIUS))
    rect = target.get_rect().move(pos)
    rect.center = pos
    return target, rect


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


def drawDownRightArrow(pos, color, adjust=True):
    drawPolygon(screen, color,
                [[pos[0], pos[1]],
                 [pos[0] - 20, pos[1]],
                 [pos[0], pos[1] - 20]],
                adjust)


def drawUpRightArrow(pos, color, adjust=True):
    drawPolygon(screen, color,
                [[pos[0], pos[1]],
                 [pos[0] - 20, pos[1]],
                 [pos[0], pos[1] + 20]],
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


def drawDownLeftArrow(pos, color, adjust=True):
    drawPolygon(screen, color,
                [[pos[0], pos[1]],
                 [pos[0] + 20, pos[1]],
                 [pos[0], pos[1] - 20]],
                adjust)


def drawUpLeftArrow(pos, color, adjust=True):
    drawPolygon(screen, color,
                [[pos[0], pos[1]],
                 [pos[0] + 20, pos[1]],
                 [pos[0], pos[1] + 20]],
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
    del drawLastCommands[:]


def zoomIn():
    global newWidth
    global newHeight
    global zoom
    global displacementX
    global displacementY
    if newWidth < 2000:
        zoom += 1
        newWidth = int(origWidth + ((zoom / 10) * origWidth))
        newHeight = int(origHeight + ((zoom / 10) * origHeight))


def zoomOut():
    global newWidth
    global newHeight
    global zoom
    global displacementX
    global displacementY
    if newWidth > 200 or newWidth == 0:
        zoom -= 1
        newWidth = int(origWidth + ((zoom / 10) * origWidth))
        newHeight = int(origHeight + ((zoom / 10) * origHeight))


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
