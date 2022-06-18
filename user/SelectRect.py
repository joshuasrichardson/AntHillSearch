import numpy as np
import pygame

from Constants import BORDER_COLOR
from display import Display


class SelectRect:
    """ A rectangle that can be used to select a group of objects by pressing the mouse button,
    moving the mouse, and releasing the mouse button """

    def __init__(self):
        self.rect = None
        self.corner = None

    def setCorner(self, mousePos):
        self.corner = mousePos

    def moveCorner(self, dx, dy):
        self.corner[0] += dx
        self.corner[1] += dy

    def isSelecting(self, mousePos=None):
        if mousePos is None:
            return self.corner is not None
        return self.corner is not None and np.abs(mousePos[0] - self.corner[0]) > 1\
            and np.abs(mousePos[1] - self.corner[1]) > 1

    def draw(self, mousePos):
        left = self.corner[0] if self.corner[0] < mousePos[0] else mousePos[0]
        top = self.corner[1] if self.corner[1] < mousePos[1] else mousePos[1]
        w = np.abs(self.corner[0] - mousePos[0])
        h = np.abs(self.corner[1] - mousePos[1])
        self.rect = Display.drawRect(Display.screen, BORDER_COLOR, pygame.Rect(left, top, w, h), 1, False)
