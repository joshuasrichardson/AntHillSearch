import numpy as np
import pygame

from config import Config
from display.Display import rotateImage


def getRockImage(pos):
    """Loads, adjusts the size, and returns the image representing a rock"""
    rock = pygame.image.load(Config.ROCK_IMAGE)
    if Config.SHOULD_DRAW:
        rock = rock.convert_alpha()
    if rock.get_size()[0] > 38 or rock.get_size()[1] > 52:
        rock = pygame.transform.scale(rock, (100, 100))
        rect = rock.get_rect().move(pos)
        rect.center = pos
    return rock


def drawRock(rock, surface):
    w, h = rock.rockHandle.get_size()
    rotateImage(surface, rock.rockHandle, rock.pos, [w / 2, h / 2], (np.pi))
