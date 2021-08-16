""" Methods related to the world's display """
import pygame

from Constants import SCREEN_COLOR
from display import Display
from display.AgentDisplay import drawAgent
from display.SiteDisplay import drawEstimatedSite, drawSite


def drawWorldObjects(world):
    """ Draws the paths, agents, sites, markers, and fog in the world"""
    if Display.shouldDrawPaths:
        drawPaths(world)
    drawAgents(world)
    if not Display.drawFarAgents:
        for siteIndex in range(0, len(world.siteList)):
            drawEstimatedSite(world.siteList[siteIndex])
    else:
        for siteIndex in range(0, len(world.siteList)):
            drawSite(world.siteList[siteIndex])
    drawMarker(world)
    if world.shouldDrawFog:
        drawFog(world)


def drawPaths(world):
    color = SCREEN_COLOR
    try:
        for posIndex, pos in enumerate(world.paths):
            if posIndex % len(world.agentList) == 0:
                color = color[0] - 1,  color[1] - 1, color[2] - 1
            pygame.draw.circle(Display.screen, color, pos, 2)
    except ZeroDivisionError:
        pass


def drawAgents(world):
    for agent in world.agentList:
        drawAgent(agent, Display.screen)


def drawMarker(world):
    if world.marker is not None:
        Display.screen.blit(world.marker[0], world.marker[1])


def drawFog(world):
    r, g, b = 30, 30, 30
    for i in range(len(world.fog)):
        pygame.draw.rect(Display.screen, (r, g, b), world.fog[i])


def drawPotentialQuality(world, potentialQuality, font):
    """ Draws the value the selected sites will be set to if the user pushes Enter """
    img = font.render("Set quality: " + str(potentialQuality), True, (255 - potentialQuality, potentialQuality, 0))
    for site in world.siteList:
        if site.isSelected:
            Display.screen.blit(img, (site.getPosition()[0] - (img.get_width() / 2), site.getPosition()[1] - (site.radius + 31), 15, 10))


def collidesWithSite(world, mousePos):
    """ Returns whether the mouse cursor is over any site in the world """
    for site in world.siteList:
        if site.wasFound and site.getSiteRect().collidepoint(mousePos):
            return True
    return False


def collidesWithAgent(world, mousePos):
    """" Returns whether the mouse cursor is over any agent in the world """
    for agent in world.agentList:
        if agent.getAgentRect().collidepoint(mousePos):
            return True
    return False
