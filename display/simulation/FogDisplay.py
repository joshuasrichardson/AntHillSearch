""" Functions used to draw the fog of war (where the agents have not yet visited) """
import pygame

from Constants import TRANSPARENT, FOG_COLOR
from config import Config
from display import Display


def initFog(hubs):
    w, h = Display.worldSize
    fog = pygame.Surface((w, h))
    fog.fill(FOG_COLOR)
    fog.set_colorkey(TRANSPARENT)
    for hub in hubs:
        pos = hub.getPosition()
        x = pos[0] - Display.worldLeft
        y = pos[1] - Display.worldTop
        pygame.draw.circle(fog, TRANSPARENT, [x, y], Config.HUB_OBSERVE_DIST, 0)
    return fog


def drawFog(fog):
    Display.blitImage(Display.screen, fog, (Display.worldLeft, Display.worldTop))


def eraseFog(fog, pos):
    x = pos[0] - Display.worldLeft
    y = pos[1] - Display.worldTop
    pygame.draw.circle(fog, TRANSPARENT, [x, y], 20)


def clearExplorableArea(world):
    x = world.fog.get_width() / 2
    y = world.fog.get_height() / 2
    Display.drawCircle(world.fog, TRANSPARENT, [x, y], Config.MAX_SEARCH_DIST, 0, False)
