import numpy as np
import pygame

from Constants import LADYBUG_IMAGE
from display import Display
from display.Display import rotateImage

def getLadybugImage(pos):
    """Loads, adjusts the size, and returns the image representing a ladybug """
    ladybug = pygame.image.load(LADYBUG_IMAGE)
    if Display.shouldDraw:
        ladybug = ladybug.convert_alpha()
    if ladybug.get_size()[0] > 38 or ladybug.get_size()[1] > 52:
        ladybug = pygame.transform.scale(ladybug, (38, 52))
        rect = ladybug.get_rect().move(pos)
        rect.center = pos
    return ladybug

def drawLadybug(ladybug, surface):
    if Display.drawFarAgents:
        w, h = ladybug.ladybugHandle.get_size()
        rotateImage(surface, ladybug.ladybugHandle, ladybug.pos, [w / 2, h / 2], (-ladybug.angle * 180 / np.pi))