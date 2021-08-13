""" Settings and methods related to the agents' display """
import numpy as np
import pygame

from Constants import HUB_OBSERVE_DIST, SHOW_ESTIMATED_QUALITY, BORDER_COLOR, SCREEN_COLOR, FOLLOW_COLOR, SITE_RADIUS, \
    DRAW_FAR_AGENTS
from display.Display import rotateImage, drawDashedLine, getDestinationMarker
from display.SiteDisplay import drawAssignmentMarker


drawFarAgents = DRAW_FAR_AGENTS


def drawAgent(agent, surface):
    if not drawFarAgents and agent.isClose(agent.getHub().getPosition(), agent.getHub().radius + HUB_OBSERVE_DIST):
        drawPath(agent, surface)  # If we are only drawing close agents, then only show their path when they are close to the hub and can report it. Else this part is taken care of in the world class.
    if drawFarAgents or agent.isClose(agent.getHub().getPosition(), agent.getHub().radius + HUB_OBSERVE_DIST):
        if agent.isTheSelected:  # Only draw the following for one of the selected agents
            drawKnownSiteMarkers(agent, surface)
            drawAssignedSite(agent)
            drawTarget(agent, surface)
        if agent.isSelected:  # Only draw state and phase circles for the selected agents
            pygame.draw.circle(surface, agent.state.getColor(), agent.agentRect.center, agent.agentHandle.get_width() * 3 / 5, 2)
            pygame.draw.circle(surface, agent.phase.getColor(), agent.agentRect.center, agent.agentHandle.get_width() * 3 / 4, 2)
        w, h = agent.agentHandle.get_size()  # Rotate the agent's image to face the direction they are heading
        rotateImage(surface, agent.agentHandle, agent.pos, [w / 2, h / 2], (-agent.angle * 180 / np.pi) - 132)

        if SHOW_ESTIMATED_QUALITY:
            img = agent.world.font.render(str(agent.estimatedQuality), True, agent.assignedSite.color)
            surface.blit(img, (agent.pos[0] + 10, agent.pos[1] + 5, 15, 10))  # Draws the agent's estimated quality of their assigned site to the bottom right of their image


def drawTarget(agent, surface):
    """ Draws the position on the screen that the agent is heading toward """
    if agent.target is not None:
        agent.marker = getDestinationMarker(agent.target)
        drawMarker(agent, surface)


def drawMarker(agent, surface):
    """ Draws the agent's specified marker on the screen (i.e. the go marker) """
    if agent.marker is not None:
        drawDashedLine(surface, BORDER_COLOR, agent.pos, agent.marker[1].center)
        surface.blit(agent.marker[0], agent.marker[1])


def drawPath(agent, surface):
    """ Draws a path behind the agent the fades as it gets farther away from them """
    color = SCREEN_COLOR
    for pos in agent.path:
        color = color[0] - 1,  color[1] - 1, color[2] - 1
        pygame.draw.circle(surface, color, pos, 2)


def drawKnownSiteMarkers(agent, surface):
    """ Draws a circle around each site the agent knows about """
    for pos in agent.knownSitesPositions:
        pygame.draw.circle(surface, FOLLOW_COLOR, pos, SITE_RADIUS + 8, 2)


def drawAssignedSite(agent):
    """ Marks the site the agent is assigned to and draws a line from the agent to the site """
    drawAssignmentMarker(agent.assignedSite, agent.pos, agent.getPhaseColor())
