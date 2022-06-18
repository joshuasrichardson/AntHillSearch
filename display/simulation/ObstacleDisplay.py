""" Functions used to draw obstacles """
import numpy as np
import pygame

from config import Config
from display.Display import rotateImage


def getObstacleImage(pos):
    """Loads, adjusts the size, and returns the image representing an obstacle"""
    obstacle = pygame.image.load(Config.OBSTACLE_IMAGE)
    if Config.SHOULD_DRAW:
        obstacle = obstacle.convert_alpha()
    if obstacle.get_size()[0] > 38 or obstacle.get_size()[1] > 52:
        obstacle = pygame.transform.scale(obstacle, (100, 100))
        rect = obstacle.get_rect().move(pos)
        rect.center = pos
    return obstacle


def drawObstacle(obstacle, surface):
    w, h = obstacle.obstacleHandle.get_size()
    rotateImage(surface, obstacle.obstacleHandle, obstacle.pos, [w / 2, h / 2], np.pi)
