""" Classes and methods for supporting pygame """
from Constants import *
import pygame


def create_screen():
    size = [WORLD_DIM, WORLD_DIM]
    pygame.display.init()
    return pygame.display.set_mode(size, pygame.RESIZABLE)

# def load_agent_image():
#    return pygame.image.load("copter.png")
