import numpy as np

from model.Site import Site
from model.builder import SiteSettings

hIndex = 0


def getNewSite(numHubs, x, y, radius, quality, hubLocations=None):
    if hubLocations is not None:
        global hIndex
        pos = initializePosition(hubLocations[hIndex], x, y)
        if hIndex < len(hubLocations) - 1:
            hIndex += 1
        else:
            hIndex = 0
    else:
        pos = list([x, y])
    return Site(numHubs, pos, radius, quality)


def initializePosition(hubLocation, x, y):
    """ Sets the site in its starting position at a random distance from the hub that is within the range
    specified with the initialization of the class or to the (x, y) coordinates if they are specified """
    angle = np.random.uniform(0, np.pi * 2)
    radius = np.random.uniform(SiteSettings.siteNoCloserThan, SiteSettings.siteNoFartherThan)
    if x is None:
        x = int(hubLocation[0] + np.round(radius * np.cos(angle)))
    if y is None:
        y = int(hubLocation[1] + np.round(radius * np.sin(angle)))
    return list([x, y])
