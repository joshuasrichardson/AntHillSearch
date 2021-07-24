""" Classes and methods for supporting pygame """
import random

import numpy
import pygame


def createScreen(shouldDraw):
    if shouldDraw:
        pygame.display.init()
        return pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    else:
        return None


def drawCircleLines(screen, circle, color, inc):
    y = circle.top
    r = (circle.width / 2)
    while y < circle.bottom:
        o = y - circle.top
        a = numpy.sqrt(numpy.square(r) - numpy.square(r - o))
        pygame.draw.line(screen, color, (circle.centerx - a, y), (circle.centerx + a, y))
        y += inc
