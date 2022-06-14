""" Settings and methods related to the display """
import numpy as np
import pygame

from config import Config
from Constants import WORDS_COLOR, GREEN, BORDER_COLOR, HOME_QUALITIES_NAME, SIM_TIMES_NAME, NUM_ARRIVALS_NAME, \
    TOTAL_NAME, NUM_DEAD_NAME, HOME_POSITIONS_NAME, NUM_ROUNDS_NAME, IN_FLOOD_ZONE_NAME
from display.simulation import SiteDisplay

screen = None
displacementX = 0
displacementY = 0
drawLastCommands = []
zoom = 0
origWidth = 0
origHeight = 0
newWidth = 0
newHeight = 0
worldSize = 0, 0
worldLeft = 0
worldTop = 0
worldRight = 0
worldBottom = 0


def createScreen():
    """ Creates and returns the main screen that the interface will be drawn on """
    global screen, origWidth, origHeight, newWidth, newHeight
    if not pygame.display.get_init():
        pygame.display.init()
        pygame.font.init()
        pygame.event.set_allowed(
            [pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])
        screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        origWidth = screen.get_width()
        origHeight = screen.get_height()
        initWorldSize()
        resetScreen()
    return screen


def resetScreen():
    global zoom, origWidth, origHeight, newWidth, newHeight, displacementX, displacementY
    zoom = 0
    newWidth = origWidth
    newHeight = origHeight
    displacementX = 0
    displacementY = 0
    while zoom < Config.INITIAL_ZOOM:
        zoomIn()
    while zoom > Config.INITIAL_ZOOM:
        zoomOut()


def writeCenter(surface, words, fontSize=Config.LARGE_FONT_SIZE, color=WORDS_COLOR):
    """ Writes words in middle of the surface with the given font size and color """
    font = pygame.font.SysFont('Comic Sans MS', fontSize)
    img = font.render(f"{words}", True, color).convert_alpha()
    surface.blit(img, (surface.get_size()[0] / 2 - (img.get_width() / 2),
                       surface.get_size()[1] / 2 - (img.get_height() / 2) - 60))
    del img


def writeCenterPlus(surface, words, fontSize, y, color=WORDS_COLOR):
    """ Writes words in middle of the surface (x-axis) with the given font size and color in the given y position """
    font = pygame.font.SysFont('Comic Sans MS', fontSize)
    img = font.render(f"{words}", True, color).convert_alpha()
    return surface.blit(img, (surface.get_size()[0] / 2 - (img.get_width() / 2),
                              surface.get_size()[1] / 2 - (img.get_height() / 2) - 60 + y))


def write(surface, words, fontSize, x, y, color=WORDS_COLOR):
    """ Writes words on the surface with the given font size and color in the given position """
    font = pygame.font.SysFont('Comic Sans MS', fontSize)
    img = font.render(f"{words}", True, color).convert_alpha()
    return surface.blit(img, (x, y))


def drawFinish(surface, results):
    """ Tells the user the simulation has ended and shows some of the results on the screen """
    surf = pygame.Surface((origWidth, origHeight), pygame.SRCALPHA)
    # Draw a partially transparent surface over the screen
    pygame.draw.rect(surf, (225, 220, 190, 200), (0, 0, origWidth, origHeight))
    surface.blit(surf, (0, 0))

    writeCenterPlus(surface, "Complete", Config.LARGE_FONT_SIZE, -(origHeight / 2 - 3 * Config.LARGE_FONT_SIZE))
    x = origWidth * 4 / 9
    y = origHeight / 6
    write(surface, "Click anywhere or press", Config.FONT_SIZE, x, y)
    y += Config.FONT_SIZE
    write(surface, "any key to continue.", Config.FONT_SIZE, x, y)

    words = ["Colony", "Rounds", "Time", "Quality", "Positions", "Arrivals", "Deaths", "In Flood Zone"]
    for i in range(len(results[HOME_QUALITIES_NAME])):
        words.append(f"{i + 1}")
        words.append(f"{results[NUM_ROUNDS_NAME][i]}")
        words.append(f"{round(results[SIM_TIMES_NAME][i], 2)}")
        words.append(f"{results[HOME_QUALITIES_NAME][i]}")
        words.append(f"{results[HOME_POSITIONS_NAME][i]}")
        words.append(f"{results[NUM_ARRIVALS_NAME][i]}/{results[TOTAL_NAME][i]}")
        words.append(f"{results[NUM_DEAD_NAME][i]}")
        words.append(f"{results[IN_FLOOD_ZONE_NAME][i]}")
    drawResultsGrid(len(results[HOME_QUALITIES_NAME]) + 1, len(results), words)


def drawResultsGrid(numRows, numColumns, words):
    x = origWidth / 6
    y = origHeight / 4
    w = (origWidth / numColumns) / 1.5
    h = (origHeight / numRows) / 2
    for row in range(numRows):
        for column in range(numColumns):
            drawRect(screen, BORDER_COLOR, pygame.Rect(x, y, w, h), 1, False)
            font = pygame.font.SysFont('Comic Sans MS', Config.FONT_SIZE)
            img = font.render(f"{words[row * numColumns + column]}", True, WORDS_COLOR).convert_alpha()
            screen.blit(img, (x + ((w - img.get_width()) / 2), y + ((h - img.get_height()) / 2)))
            x += w
        y += h
        x = origWidth / 6


def getDestinationMarker(pos):
    """ Loads, adjusts the size, and returns the image representing a destination """
    arrows = pygame.image.load("resources/arrows.png").convert_alpha()
    if arrows.get_size()[0] > 30 or arrows.get_size()[1] > 30:
        arrows = pygame.transform.scale(arrows, (30, 30))
    rect = arrows.get_rect().move(pos)
    rect.center = pos
    return arrows, rect


def getAssignmentMarker(pos):
    """ Loads, adjusts the size, and returns the image representing an assignment """
    target = pygame.image.load("resources/target.png").convert_alpha()
    if target.get_size()[0] > 2 * Config.SITE_RADIUS or target.get_size()[1] > 2 * Config.SITE_RADIUS:
        target = pygame.transform.scale(target, (2 * Config.SITE_RADIUS, 2 * Config.SITE_RADIUS))
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

    return [drawLine(surface, color, tuple(dashKnots[n]), tuple(dashKnots[n + 1]), width)
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


def onScreenX(x):
    return 0 < x < origWidth


def onScreenY(y):
    return 0 < y < origHeight


def drawRect(surf, color, rect, width=0, adjust=True):
    if not adjust:
        rectangle = rect
    else:
        left, top = getAdjustedPos(rect.left, rect.top)
        w, h = getZoomedSize(rect.width, rect.height)
        rectangle = pygame.Rect(left, top, w, h)
    if onScreenX(rectangle.left) or onScreenX(rectangle.right) or \
            onScreenY(rectangle.top) or onScreenY(rectangle.bottom):
        return pygame.draw.rect(surf, color, rectangle, width)
    else:
        return rectangle


def drawCircle(surface, color, pos, radius, width=0, adjust=True):
    if not adjust:
        position = pos
    else:
        position = getAdjustedPos(*pos)
        radius = getZoomedSize(radius, radius)[0]
    x, y = position
    if onScreenX(x - radius) or onScreenX(x + radius) or \
            onScreenY(y - radius) or onScreenY(y + radius):
        return pygame.draw.circle(surface, color, position, radius, width)
    else:
        return pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)


def drawPolygon(surface, color, positions, adjust=True, width=0):
    newPositions = []
    if adjust:
        for pos in positions:
            newPositions.append(getAdjustedPos(*pos))
    else:
        return pygame.draw.polygon(surface, color, positions, width)
    return pygame.draw.polygon(surface, color, newPositions, width)


def drawLine(surface, color, startPos, endPos, width=1, adjust=True):
    if not adjust:
        return pygame.draw.line(surface, color, startPos, endPos, width)
    pos0 = getAdjustedPos(*startPos)
    pos1 = getAdjustedPos(*endPos)
    return pygame.draw.line(surface, color, pos0, pos1, width)


def blitImage(surface, source, destination, adjust=True):
    if adjust:
        try:
            dest = getAdjustedPos(destination[0], destination[1])
        except AttributeError:
            dest = getAdjustedPos(destination.left, destination.top)
        try:
            source = pygame.transform.scale(source, getZoomedSize(source.get_width(), source.get_height()))
        except AttributeError as e:
            print(e.__cause__)
            source = pygame.transform.scale(source, getZoomedSize(source.width, source.height))
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


def addToDrawLast(command, args):
    drawLastCommands.append((command, args))


def drawLast():
    for command in drawLastCommands:
        command[0](*command[1])
    del drawLastCommands[:]


def zoomIn():
    global newWidth, newHeight, zoom, displacementX, displacementY
    if newWidth < 1600:
        oldCenterX, oldCenterY = getReadjustedPos(origWidth / 2, origHeight / 2)
        zoom += 1
        newWidth = int(origWidth + ((zoom / 15) * origWidth))
        newHeight = int(origHeight + ((zoom / 15) * origHeight))
        newCenterX, newCenterY = getReadjustedPos(origWidth / 2, origHeight / 2)
        diffX = newCenterX - oldCenterX
        diffY = newCenterY - oldCenterY
        displacementX += diffX
        displacementY += diffY
    SiteDisplay.siteFontSize = Config.FONT_SIZE if zoom >= 0 else Config.FONT_SIZE + 3 * -zoom


def zoomOut():
    global newWidth, newHeight, zoom, displacementX, displacementY
    w, h = worldSize
    adjW, _ = getZoomedSize(w, h)
    if adjW > origWidth or newWidth == 0:
        oldCenterX, oldCenterY = getReadjustedPos(origWidth / 2, origHeight / 2)
        zoom -= 1
        newWidth = int(origWidth + ((zoom / 15) * origWidth))
        newHeight = int(origHeight + ((zoom / 15) * origHeight))
        newCenterX, newCenterY = getReadjustedPos(origWidth / 2, origHeight / 2)
        diffX = newCenterX - oldCenterX
        diffY = newCenterY - oldCenterY
        displacementX += diffX
        displacementY += diffY
    adjW, _ = getZoomedSize(w, h)
    if adjW < origWidth:
        newWidth = int((origWidth ** 2) / w)
        newHeight = int((origHeight ** 2) / h)
    adjustScreen()
    SiteDisplay.siteFontSize = Config.FONT_SIZE if zoom >= 0 else Config.FONT_SIZE + 3 * -zoom


def adjustScreen():
    global displacementX, displacementY
    adjW, adjH = getUnzoomedSize(origWidth, origHeight)
    while adjW - displacementX > worldRight:  # Too far right
        displacementX += 25  # Move left
    while adjH - displacementY > worldBottom:  # Too far down
        displacementY += 25  # Move up
    while -displacementY < worldTop:  # Too far up
        displacementY -= 25  # Move down
    while -displacementX < worldLeft:  # Too far left
        displacementX -= 25  # Move right


def moveScreen():
    dx, dy = 0, 0
    if not pygame.key.get_mods() & pygame.KMOD_CAPS:
        mousePos = pygame.mouse.get_pos()
        global displacementX, displacementY, worldLeft, worldTop, worldRight, worldBottom
        adjW, adjH = getUnzoomedSize(origWidth, origHeight)
        if mousePos[0] >= origWidth - 3 and adjW - displacementX < worldRight:
            displacementX -= 25
            addToDrawLast(drawRightArrow, [mousePos, GREEN, False])
            dx = -25
        if mousePos[1] <= 3 and -displacementY > worldTop:
            displacementY += 25
            addToDrawLast(drawUpArrow, [mousePos, GREEN, False])
            dy = 25
        if mousePos[0] <= 3 and -displacementX > worldLeft:
            displacementX += 25
            addToDrawLast(drawLeftArrow, [mousePos, GREEN, False])
            dx = 25
        if mousePos[1] >= origHeight - 30 and adjH - displacementY < worldBottom:
            displacementY -= 25
            addToDrawLast(drawDownArrow, [mousePos, GREEN, False])
            dy = -25
    return dx, dy


def getAdjustedPos(origX, origY):
    global origWidth, origHeight, newWidth, newHeight
    newX = ((origX + displacementX) / origWidth) * newWidth
    newY = ((origY + displacementY) / origHeight) * newHeight
    return [newX, newY]


def getReadjustedPos(origX, origY):
    global origWidth, origHeight, newWidth, newHeight
    newX = (origX / newWidth) * origWidth - displacementX
    newY = (origY / newHeight) * origHeight - displacementY
    return [newX, newY]


def getZoomedSize(origW, origH):
    global origWidth, origHeight, newWidth, newHeight
    newW = round((origW / origWidth) * newWidth)
    newH = round((origH / origHeight) * newHeight)
    return [newW, newH]


def getUnzoomedSize(origW, origH):
    global origWidth, origHeight, newWidth, newHeight
    newW = int((origW / newWidth) * origWidth)
    newH = int((origH / newHeight) * origHeight)
    return [newW, newH]


def initWorldSize():
    global origWidth, origHeight, worldSize, worldLeft, worldTop, worldRight, worldBottom
    w, h = origWidth, origHeight
    m = Config.MAX_SEARCH_DIST * 2 + h
    while h < m:
        w += (origWidth / 16)
        h += (origHeight / 16)
    worldSize = w, h
    worldLeft = (origWidth - w) / 2
    worldTop = (origHeight - h) / 2
    worldRight = worldLeft + w
    worldBottom = worldTop + h


def drawBorder():
    global worldSize, worldLeft, worldTop, worldRight, worldBottom
    w, h = worldSize
    drawRect(screen, BORDER_COLOR, pygame.Rect(worldLeft, worldTop, w, h), 20)
