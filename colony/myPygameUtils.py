""" Classes and methods for supporting pygame """
import pygame


def createScreen(shouldDraw):
    if shouldDraw:
        pygame.display.init()
        return pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    else:
        return None
