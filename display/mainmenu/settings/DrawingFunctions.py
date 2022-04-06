import math

import pygame

from config import Config
from config.Config import AGENT_IMAGES
from Constants import GREEN, RED, BLUE, BORDER_COLOR, FONT_SIZE_NAME, SITE_RADIUS_NAME, \
    HUB_LOCATIONS_NAME, SHOULD_RECORD_NAME, AGENT_IMAGE_NAME, LARGE_FONT_SIZE_NAME, SITE_NO_FARTHER_THAN_NAME, \
    SITE_NO_CLOSER_THAN_NAME, MEDIUM_QUALITY, FULL_CONTROL_NAME, DISTRACTED_NAME, USE_ROUNDS_AS_DURATION_NAME, \
    FLOOD_ZONE_CORNERS_NAME
from display import Display, AgentDisplay, SiteDisplay, PredatorDisplay, LadybugDisplay, FloodZoneDisplay
from model.FloodZone import FloodZone
from model.builder.SiteBuilder import getNewSite


def showSimDuration(self):
    Display.write(Display.screen, self.value, int(Config.FONT_SIZE * 1.5), Display.origWidth - 100, 50)


def showFontSize(self):
    Display.writeCenter(Display.screen, "Simulation size", self.value)
    Display.writeCenterPlus(Display.screen, "Settings size", int(self.value * 1.5),
                            int(self.value * 1.5))


def showLargeFontSize(self):
    Display.writeCenter(Display.screen, "This size", self.value)


def drawHubsPositions(self):
    drawNestPositions(self, -1)


def drawSitesPositions(self):
    drawNestPositions(self, MEDIUM_QUALITY)


def drawNestPositions(self, quality):
    if self.arrayStates.isComplete2:
        # TODO: If the hubs are too close together, force them to be farther apart
        for pos in self.value:
            drawSite(pos, Config.SITE_RADIUS, quality)
    else:
        drawSites(self, Config.HUB_LOCATIONS, quality)


def drawPredPositions(self):
    if self.arrayStates.isComplete2:
        for pos in self.value:
            drawPredator(pos)


def drawLadybugPositions(self):
    if self.arrayStates.isComplete2:
        for pos in self.value:
            drawLadybug(pos)


def drawShouldRecord(self):
    if Config.SHOULD_RECORD:
        Display.drawCircle(Display.screen, (220, 0, 0), [15, 15], 10, width=1, adjust=False)
        Display.drawLine(Display.screen, (220, 0, 0), [4, 24], [25, 5], adjust=False)
    else:
        Display.drawCircle(Display.screen, (220, 0, 0), [15, 15], 10, adjust=False)


def drawSiteRadius(self):
    drawSite([Display.origWidth / 2, Display.origHeight / 2], self.value, 200)


def drawNoFartherThan(self):
    drawArea(self, GREEN, self.value)
    drawArea(self, RED, Config.SITE_NO_CLOSER_THAN)


def drawNoCloserThan(self):
    drawArea(self, GREEN, Config.SITE_NO_FARTHER_THAN)
    drawArea(self, RED, self.value)


def drawSearchArea(self):
    drawArea(self, BLUE, self.value)


def drawConvergenceFraction(self):
    fraction = self.value
    Config.AGENT_IMAGE = Config.AGENT_IMAGE
    image = AgentDisplay.getAgentImage([Display.origWidth / 2, Display.origHeight / 2])
    w = image.get_width() * 5
    h = image.get_height() * 20
    x = Display.origWidth / 2 - w / 2
    y = Display.origHeight / 2 - h / 2
    rect = pygame.Rect(x, y, w, h)
    Display.drawRect(Display.screen, BORDER_COLOR, rect, 2, False)

    fraction = int(math.ceil(fraction * 100))
    j = 0
    d = h
    dif = h / 20
    for i in range(fraction):
        if j % 5 == 0:
            d -= dif
        Display.blitImage(Display.screen, image, [x + (dif * (i % 5)), y + d], False)
        j += 1
    for i in range(100 - fraction):
        if j % 5 == 0:
            d -= dif
        Display.blitImage(Display.screen, image, [2 * w + 10 + x - (dif * (i % 5)), y + d], False)
        j += 1


def drawSite(pos, radius, quality, numAgents=0):
    potentialSite = getNewSite(1, pos[0], pos[1], radius, quality)
    potentialSite.wasFound = True
    potentialSite.agentCount = numAgents
    SiteDisplay.drawSite(potentialSite, pos, radius, quality)
    del potentialSite


def drawSites(self, positions, quality):
    for pos in positions:
        drawSite(pos, Config.SITE_RADIUS, quality)


def drawNumHubs(self):
    drawNumNests(self, -1)


def drawNumSites(self):
    drawNumNests(self, MEDIUM_QUALITY)


def drawNumNests(self, quality):
    x = Display.origWidth / 2
    h = int((Display.origHeight - Config.LARGE_FONT_SIZE * 3) / (
            2 * (Config.SITE_RADIUS + 10)))  # The number of sites that can fit in a column
    for i in range(self.value):
        y = 2 * (i % h) * (Config.SITE_RADIUS + 10) + (Config.LARGE_FONT_SIZE * 3)
        if i % h == 0 and i > 0:
            x += 2 * (Config.SITE_RADIUS + 10)
        drawSite([x, y], Config.SITE_RADIUS, quality)


def drawHubsRadii(self):
    drawRadii(self, -1)


def drawSitesRadii(self):
    drawRadii(self, MEDIUM_QUALITY)


def drawRadii(self, quality):
    x = Display.origWidth / 2
    h = int((Display.origHeight - Config.LARGE_FONT_SIZE * 3) / (
            2 * (Config.SITE_RADIUS + 10)))  # The number of sites that can fit in a column
    if not isinstance(self.value, list):
        self.value = []
    for i in range(len(self.value)):
        y = 2 * (i % h) * (Config.SITE_RADIUS + 10) + (Config.LARGE_FONT_SIZE * 3)
        if i % h == 0 and i > 0:
            x += 2 * (Config.SITE_RADIUS + 10)
        drawSite([x, y], self.value[i], quality)


def drawHubsCounts(self):
    drawCounts(self, -1)


def drawSitesCounts(self):
    drawCounts(self, MEDIUM_QUALITY)


def drawCounts(self, quality):
    x = Display.origWidth / 2
    h = int((Display.origHeight - Config.LARGE_FONT_SIZE * 3) / (
            2 * (Config.SITE_RADIUS + 10)))  # The number of sites that can fit in a column
    if not isinstance(self.value, list):
        self.value = []
    for i in range(len(self.value)):
        y = 2 * (i % h) * (Config.SITE_RADIUS + 10) + (Config.LARGE_FONT_SIZE * 3)
        if i % h == 0 and i > 0:
            x += 2 * (Config.SITE_RADIUS + 10)
        drawSite([x, y], Config.SITE_RADIUS, quality, self.value[i])


def drawSitesQualities(self):
    x = Display.origWidth / 2
    h = int((Display.origHeight - Config.LARGE_FONT_SIZE * 3) / (
            2 * (Config.SITE_RADIUS + 10)))  # The number of sites that can fit in a column
    if not isinstance(self.value, list):
        self.value = []
    for i in range(len(self.value)):
        y = 2 * (i % h) * (Config.SITE_RADIUS + 10) + (Config.LARGE_FONT_SIZE * 3)
        if i % h == 0 and i > 0:
            x += 2 * (Config.SITE_RADIUS + 10)
        drawSite([x, y], Config.SITE_RADIUS, self.value[i])


def drawAgents(self):
    for i, imgFile in enumerate(AGENT_IMAGES):
        pos = [Display.origWidth / 2 + i * 30, Display.origHeight / 2]
        Config.AGENT_IMAGE = imgFile
        image = AgentDisplay.getAgentImage([Display.origWidth / 2, Display.origHeight / 2])
        if imgFile != Config.AGENT_IMAGE:
            Display.drawDownArrow([pos[0] + image.get_width() / 2, pos[1]], BORDER_COLOR, False)
        Display.blitImage(Display.screen, image, pos, False)


def getOtherFile():
    numImages = len(AGENT_IMAGES)
    for i in range(numImages - 1):
        if Config.AGENT_IMAGE == AGENT_IMAGES[i % numImages]:
            return AGENT_IMAGES[i + 1 % numImages]
    return AGENT_IMAGES[0]


def drawArea(self, color, radius):
    fadedColor = (color[0], color[1], color[2], 80)
    surf = pygame.Surface((Display.origWidth, Display.origHeight), pygame.SRCALPHA)
    Display.drawCircle(surf, fadedColor, [Display.origWidth / 2, Display.origHeight / 2], radius)
    Display.blitImage(Display.screen, surf, (0, 0), False)
    drawSite([Display.origWidth / 2, Display.origHeight / 2], Config.SITE_RADIUS, -1)


def drawPredator(pos):
    image = PredatorDisplay.getPredatorImage([0, 0])
    Display.blitImage(Display.screen, image, pos, False)


def drawPredators(self):
    for i in range(self.value):
        pos = [Display.origWidth / 2 + i * 50, Display.origHeight / 2]
        drawPredator(pos)


def drawLadybug(pos):
    image = LadybugDisplay.getLadybugImage([0, 0])
    Display.blitImage(Display.screen, image, pos, False)


def drawLadybugs(self):
    for i in range(self.value):
        pos = [Display.origWidth / 2 + i * 50, Display.origHeight / 2]
        drawLadybug(pos)


def drawControls(self):
    if Config.FULL_CONTROL:
        controls = ["Go"]
    else:
        controls = ["Go", "Assign", "Set Checkpoint", "Avoid"]
    for i, control in enumerate(controls):
        Display.writeCenterPlus(Display.screen, control, int(Config.FONT_SIZE * 1.5), i * Config.FONT_SIZE * 1.5)


def drawDistraction(self):
    if Config.DISTRACTED:
        pass
    else:
        pass


def drawRoundsAsDuration(self):
    if Config.USE_ROUNDS_AS_DURATION:
        pass
    else:
        pass


def drawFloodZone(self):
    FloodZoneDisplay.drawFloodZone(self.settingMenu.worldSettings.world.floodZone)
