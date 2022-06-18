""" Functions used to display a predator """
import numpy as np
import pygame

from config import Config
from display.Display import rotateImage


def getPredatorImage(pos):
    """ Loads, adjusts the size, and returns the image representing a predator """
    predator = pygame.image.load(Config.PREDATOR_IMAGE)
    if Config.SHOULD_DRAW:
        predator = predator.convert_alpha()
    if predator.get_size()[0] > 38 or predator.get_size()[1] > 52:
        predator = pygame.transform.scale(predator, (38, 52))
        rect = predator.get_rect().move(pos)
        rect.center = pos
    return predator


def drawPredator(predator, surface):
    if Config.DRAW_FAR_AGENTS:
        w, h = predator.predatorHandle.get_size()  # Rotate the agent's image to face the direction they are heading
        rotateImage(surface, predator.predatorHandle, predator.pos, [w / 2, h / 2], (-predator.angle * 180 / np.pi))
