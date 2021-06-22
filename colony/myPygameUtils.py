""" Classes and methods for supporting pygame """
import pygame


def createScreen():
    pygame.display.init()
    return pygame.display.set_mode((0, 0), pygame.RESIZABLE)
