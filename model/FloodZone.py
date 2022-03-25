import pygame
from pygame import mask, SRCALPHA

from display import Display, FloodZoneDisplay
from config import Config


class FloodZone:
    def __init__(self):
        self.coverage = Config.FLOOD_ZONE_COVERAGE
        self.corners = Config.FLOOD_ZONE_CORNERS

        if len(self.corners) < 3:
            # TODO: Make this generate corners in a super cool way
            self.corners = [[Display.worldLeft, Display.worldTop], [Display.worldLeft, Display.worldBottom],
                            [Display.origWidth / 2, Display.worldBottom], [Display.origWidth / 2, Display.worldTop]]

        self.surface = pygame.Surface((Display.worldSize[0], Display.worldSize[1]), SRCALPHA)
        self.rect = FloodZoneDisplay.initFloodZoneDisplay(self.surface, self.corners)
        self.mask = mask.from_surface(self.surface, threshold=50)

    def overlaps(self, surface, rect):
        offset = self.rect[0] - rect[0], self.rect[1] - rect[1]
        Display.drawCircle(surface, (0, 0, 0), [rect.w / 2, rect.h / 2], rect.w / 2)
        otherMask = mask.from_surface(surface, threshold=50)
        return otherMask.overlap(self.mask, offset) is not None
