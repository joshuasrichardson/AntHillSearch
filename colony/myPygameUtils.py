""" Classes and methods for supporting pygame """
import numpy
import numpy as np
import pygame


def createScreen(shouldDraw):
    if shouldDraw:
        pygame.display.init()
        return pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    else:
        return None


def drawCircleLines(screen, circle, color, inc):
    drawVerticalCircleLines(screen, circle, color, inc)
    drawHorizontalCircleLines(screen, circle, color, inc)


def drawVerticalCircleLines(screen, circle, color, inc):
    x = circle.left
    r = (circle.height / 2)
    while x < circle.right:
        o = x - circle.left
        a = numpy.sqrt(numpy.abs(numpy.square(r) - numpy.square(r - o)))
        pygame.draw.line(screen, color, (x, circle.centery - a), (x,  circle.centery + a))
        x += inc


def drawHorizontalCircleLines(screen, circle, color, inc):
    y = circle.top
    r = (circle.width / 2)
    while y < circle.bottom:
        o = y - circle.top
        a = numpy.sqrt(numpy.abs(numpy.square(r) - numpy.square(r - o)))
        pygame.draw.line(screen, color, (circle.centerx - a, y), (circle.centerx + a, y))
        y += inc


def getDestinationMarker(pos):
    arrow = pygame.image.load("arrows.png")
    arrow = pygame.transform.scale(arrow, (30, 30))
    rect = arrow.get_rect().move(pos)
    rect.center = pos
    return arrow, rect


def drawDashedLine(surface, color, startPos, endPos, width=1, dashLength=10, excludeCorners=True):

    # convert tuples to numpy arrays
    startPos = np.array(startPos)
    endPos = np.array(endPos)

    # get Euclidean distance between start_pos and end_pos
    length = np.linalg.norm(endPos - startPos)

    # get number of pieces that line will be split up in (half of it are amount of dashes)
    numDashes = int(length / dashLength)

    # x-y-value-pairs of where dashes start (and on next, will end)
    dashKnots = np.array([np.linspace(startPos[i], endPos[i], numDashes) for i in range(2)]).transpose()

    return [pygame.draw.line(surface, color, tuple(dashKnots[n]), tuple(dashKnots[n+1]), width)
            for n in range(int(excludeCorners), numDashes - int(excludeCorners), 2)]


def getBlurredImage(surface, amount):
    """ Blur the given surface by the given 'amount'.  Only values 1 and greater
    are valid.  Value 1 = no blur. """
    if amount < 1.0:
        raise ValueError("Arg 'amount' must be greater than 1.0, passed in value is %s" % amount)
    scale = 1.0 / float(amount)
    surfSize = surface.get_size()
    scaleSize = (int(surfSize[0] * scale), int(surfSize[1] * scale))
    surf = pygame.transform.smoothscale(surface, scaleSize)
    surf = pygame.transform.smoothscale(surf, surfSize)
    return surf


# def blitRotate(surf, image, pos, originPos, angle):
#
#     # calcaulate the axis aligned bounding box of the rotated image
#     w, h       = image.get_size()
#     box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
#     box_rotate = [p.rotate(angle) for p in box]
#     min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
#     max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
#
#     # calculate the translation of the pivot
#     pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
#     pivot_rotate = pivot.rotate(angle)
#     pivot_move   = pivot_rotate - pivot
#
#     # calculate the upper left origin of the rotated image
#     origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])
#
#     # get a rotated image
#     rotated_image = pygame.transform.rotate(image, angle)
#
#     # rotate and blit the image
#     surf.blit(rotated_image, origin)
#
#     # draw rectangle around the image
#     pygame.draw.rect(surf, (255, 0, 0), (*origin, *rotated_image.get_size()),2)
