""" Classes and methods for supporting pygame """
import pygame


def create_screen():
    pygame.display.init()
    return pygame.display.set_mode((0, 0), pygame.RESIZABLE)
