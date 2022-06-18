""" Functions used to draw the world """
import pygame

from config import Config
from Constants import SCREEN_COLOR, NO_MARKER_NAME, RED, BLACK
from display.simulation.ObstacleDisplay import drawObstacle
from display import Display
from display.simulation import AgentDisplay, FloodZoneDisplay, SiteDisplay, FogDisplay
from display.simulation.AgentDisplay import drawAgent
from display.simulation.PredatorDisplay import drawPredator
from display.simulation.LadybugDisplay import drawLadybug
from display.simulation.SiteDisplay import drawSite


def drawWorldObjects(world, drawFarAgents=None):
    """ Draws the paths, agents, sites, markers, and fog in the world"""
    if Config.SHOULD_DRAW_PATHS:
        drawPaths(world)
    drawAgents(world)
    drawPredators(world)
    drawLadybugs(world)
    drawObstacles(world)
    if drawFarAgents is None:
        drawFarAgents = Config.DRAW_FAR_AGENTS
    if not drawFarAgents:
        for site in world.siteList:
            if site.wasFound:
                drawSite(site, site.estimatedPosition, site.estimatedRadius + site.blurRadiusDiff,
                         site.estimatedQuality, site.blurAmount)
    else:
        for site in world.siteList:
            drawSite(site, site.pos, site.getRadius(), site.quality)
    drawPredators(world)
    FogDisplay.drawFog(world.fog)
    FloodZoneDisplay.drawFloodZone(world.floodZone)
    if not Config.DRAW_FAR_AGENTS:
        drawDangerZones(world)
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


def drawLadybugs(world):
    for ladybug in world.ladybugList:
        drawLadybug(ladybug, Display.screen)


def drawObstacles(world):
    for obstacle in world.obstacleList:
        drawObstacle(obstacle, Display.screen)


def drawDangerZones(world):
    for i, pos in enumerate(world.dangerZones):
        drawDangerZone(pos, world.dangerZonesVisibilities[i])


def drawDangerZone(pos, visibility):
    size = Display.getZoomedSize(80, 80)
    surf = pygame.Surface((size[0] + 1, size[1] + 1), pygame.SRCALPHA)

    # Draw triangle and exclamation mark warning sign
    pygame.draw.polygon(surf, [*RED, visibility], [[size[0] / 2, 0], [0, size[1]], size], 3)
    pygame.draw.line(surf, [*BLACK, visibility], [size[0] / 2, size[0] / 4], [size[0] / 2, 3 * size[0] / 4], 4)
    pygame.draw.line(surf, [*BLACK, visibility], [size[0] / 2, 13 * size[0] / 16], [size[0] / 2, 7 * size[0] / 8], 4)

    # Draw a partially transparent surface over the screen
    Display.screen.blit(surf, Display.getAdjustedPos(*pos))


def drawMarkers(world):
    for agent in world.agentList:
        if agent.isSelected is not None:
            AgentDisplay.drawMarker(agent, Display.screen)
    for site in world.siteList:
        if site.markerName is not NO_MARKER_NAME and site.isSelected:
            SiteDisplay.drawMarker(site)


def drawPotentialQuality(world, potentialQuality):
    """ Draws the value the selected sites will be set to if the user pushes Enter """
    img = pygame.font.SysFont('Comic Sans MS', SiteDisplay.siteFontSize).render(f"Set quality: {potentialQuality}", True,
                                                                                (255 - potentialQuality, potentialQuality, 0)).convert_alpha()
    for site in world.siteList:
        if site.isSelected and not site.isHub():
            Display.blitImage(Display.screen, img, (site.getPosition()[0] - (img.get_width() / 2),
                                                    site.getPosition()[1] - (site.getRadius() + 45), 15, 10))


def collidesWithSite(world, mousePos):
    """ Returns whether the mouse cursor is over any site in the world """
    for site in world.siteList:
        if site.wasFound and site.getSiteRect().collidepoint(mousePos):
            return True
    return False


def collidesWithEstimatedSite(world, mousePos):
    """ Returns whether the mouse cursor is over any site in the world """
    for site in world.siteList:
        try:
            if site.wasFound and site.getEstSiteRect().collidepoint(mousePos):
                return True
        except AttributeError:
            pass
    return False


def collidesWithAgent(world, mousePos):
    """" Returns whether the mouse cursor is over any agent in the world """
    for agent in world.agentList:
        if agent.getRect().collidepoint(mousePos):
            return True
    return False
