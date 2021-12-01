""" Methods related to the world's display """
import pygame

import Constants
from Constants import SCREEN_COLOR, TRANSPARENT, HUB_OBSERVE_DIST, FOG_COLOR, NO_MARKER_NAME
from display import Display, AgentDisplay, SiteDisplay
from display.AgentDisplay import drawAgent
from display.PredatorDisplay import drawPredator
from display.SiteDisplay import drawEstimatedSite, drawSite


fog = None


def drawWorldObjects(world):
    """ Draws the paths, agents, sites, markers, and fog in the world"""
    if Display.shouldDrawPaths:
        drawPaths(world)
    drawAgents(world)
    drawPredators(world)
    if not Display.drawFarAgents:
        for siteIndex in range(0, len(world.siteList)):
            drawEstimatedSite(world.siteList[siteIndex])
        drawDangerZones(world)
    else:
        for siteIndex in range(0, len(world.siteList)):
            drawSite(world.siteList[siteIndex])
    drawFog()
    drawMarkers(world)
    Display.drawLast()


def drawPaths(world):
    color = SCREEN_COLOR
    try:
        for posIndex, pos in enumerate(world.paths):
            if posIndex % len(world.agentList) == 0:
                color = color[0] - 1,  color[1] - 1, color[2] - 1
            Display.drawCircle(Display.screen, color, pos, 2)
    except ZeroDivisionError:
        pass


def drawAgents(world):
    for agent in world.agentList:
        drawAgent(agent, Display.screen)


def drawPredators(world):
    for predator in world.predatorList:
        drawPredator(predator, Display.screen)


def drawDangerZones(world):
    for pos in world.dangerZones:
        drawDangerZone(pos)


def drawDangerZone(pos):
    SiteDisplay.drawBlurredCircle(pos, (0, 0, 0), 80, 30, 8)


def drawMarkers(world):
    for agent in world.agentList:
        if agent.isSelected is not None:
            AgentDisplay.drawMarker(agent, Display.screen)
    for site in world.siteList:
        if site.markerName is not NO_MARKER_NAME:
            SiteDisplay.drawMarker(site)


def initFog(hubs):
    global fog
    w, h = Display.screen.get_size()
    w += (Constants.MAX_SEARCH_DIST * 2)
    h += (Constants.MAX_SEARCH_DIST * 2)
    fog = pygame.Surface((w, h))
    fog.fill(FOG_COLOR)
    fog.set_colorkey(TRANSPARENT)
    for hub in hubs:
        pos = hub.getPosition()
        x = pos[0] + Constants.MAX_SEARCH_DIST
        y = pos[1] + Constants.MAX_SEARCH_DIST
        pygame.draw.circle(fog, TRANSPARENT, [x, y], HUB_OBSERVE_DIST + hub.radius * 2, 0)


def drawFog():
    if fog is not None:
        Display.blitImage(Display.screen, fog, (-Constants.MAX_SEARCH_DIST, -Constants.MAX_SEARCH_DIST))


def eraseFog(pos):
    if fog is not None:
        x = pos[0] + Constants.MAX_SEARCH_DIST
        y = pos[1] + Constants.MAX_SEARCH_DIST
        pygame.draw.circle(fog, TRANSPARENT, [x, y], 20, 0)


def drawPotentialQuality(world, potentialQuality, font):
    """ Draws the value the selected sites will be set to if the user pushes Enter """
    img = font.render("Set quality: " + str(potentialQuality), True, (255 - potentialQuality, potentialQuality, 0)).convert_alpha()
    for site in world.siteList:
        if site.isSelected and site.getQuality() != -1:
            Display.blitImage(Display.screen, img, (site.getPosition()[0] - (img.get_width() / 2), site.getPosition()[1] - (site.radius + 31), 15, 10))


def collidesWithSite(world, mousePos):
    """ Returns whether the mouse cursor is over any site in the world """
    for site in world.siteList:
        if site.wasFound and site.getSiteRect().collidepoint(mousePos):
            return True
    return False


def collidesWithAgent(world, mousePos):
    """" Returns whether the mouse cursor is over any agent in the world """
    for agent in world.agentList:
        if agent.getRect().collidepoint(mousePos):
            return True
    return False
