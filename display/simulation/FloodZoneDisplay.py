""" Functions used to draw the flood zone """
from Constants import FLOOD_ZONE_COLOR
from display import Display


def initFloodZoneDisplay(surface, corners):
    # Draw a partially transparent surface over the screen
    Display.drawPolygon(surface, FLOOD_ZONE_COLOR, corners, adjust=False)


def drawFloodZone(floodZone):
    Display.blitImage(Display.screen, floodZone.surface, (Display.worldLeft, Display.worldTop))
