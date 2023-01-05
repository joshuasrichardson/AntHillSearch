""" Functions used to display an agent and markers belonging to them """
import numpy as np
import pygame

from config import Config
from Constants import BORDER_COLOR, SCREEN_COLOR, ORANGE, DEAD, SIMPLIFY_STATES
from display import Display
from display.Display import rotateImage, drawDashedLine
from display.simulation.SiteDisplay import drawAssignmentMarker


def drawAgent(agent, surface):
    if not Config.DRAW_FAR_AGENTS:
        if agent.isClose(agent.getHub().getPosition(), Config.HUB_OBSERVE_DIST):
            drawPath(agent, surface)  # If we are only drawing close agents, then only show their path when they are close to the hub and can report it. Else this part is taken care of in the world display class.
        # else:
        #     drawLastKnownPos(agent)
    if Config.DRAW_FAR_AGENTS or agent.isClose(agent.getHub().getPosition(), Config.HUB_OBSERVE_DIST):
        if agent.isMainSelected:  # Only draw the following for one of the selected agents
            drawKnownSiteMarkers(agent, surface)
            drawAssignedSite(agent)
            drawPlacesToAvoid(agent)
        if agent.isSelected:  # Only draw state and phase circles for the selected agents
            Display.drawCircle(surface, agent.getStateColor(), agent.agentRect.center, agent.agentHandle.get_width() * 3 / 5, 2)
            if not SIMPLIFY_STATES:
                Display.drawCircle(surface, agent.getPhaseColor(), agent.agentRect.center, agent.agentHandle.get_width() * 3 / 4, 2)
        w, h = agent.agentHandle.get_size()  # Rotate the agent's image to face the direction they are heading
        rotateImage(surface, agent.agentHandle, agent.pos, [w / 2, h / 2], (-agent.angle * 180 / np.pi) - 132)


def drawLastKnownPos(agent):
    Display.drawCircle(Display.screen, agent.lastKnownPhaseColor, agent.lastSeenPos, 4, adjust=True)


def getAgentImage(pos):
    """ Loads, adjusts the size, and returns the image representing an agent """
    agent = pygame.image.load(Config.AGENT_IMAGE)
    if Config.SHOULD_DRAW:
        agent = agent.convert_alpha()
    if agent.get_size()[0] > 30 or agent.get_size()[1] > 30:
        agent = pygame.transform.scale(agent, (30, 30))
        rect = agent.get_rect().move(pos)
        rect.center = pos
    return agent


def drawMarker(agent, surface):
    """ Draws the agent's specified marker on the screen (i.e. the go marker) """
    if (Config.DRAW_FAR_AGENTS or agent.isCloseToHub()) and agent.marker is not None:
        drawDashedLine(surface, BORDER_COLOR, agent.pos, agent.marker[1].center)
        Display.blitImage(Display.screen, agent.marker[0], agent.marker[1])


def drawPlacesToAvoid(agent):
    """ Draws the places the agent should avoid on the screen """
    if Config.DRAW_FAR_AGENTS or agent.isCloseToHub():
        for pos in agent.placesToAvoid:
            Display.drawLine(Display.screen, (155, 0, 0, 120), [pos[0] - Config.AVOID_MARKER_XY, pos[1] +
                                                                Config.AVOID_MARKER_XY], [pos[0] + Config.AVOID_MARKER_XY, pos[1] - Config.AVOID_MARKER_XY], 4)
            Display.drawCircle(Display.screen, (155, 0, 0, 120), pos, Config.MIN_AVOID_DIST, 4)


def drawPath(agent, surface):
    """ Draws a path behind the agent the fades as it gets farther away from them """
    color = SCREEN_COLOR
    for pos in agent.path:
        color = color[0] - 1,  color[1] - 1, color[2] - 1
        Display.drawCircle(surface, color, pos, 2)


def drawKnownSiteMarkers(agent, surface):
    """ Draws a circle around each site the agent knows about """
    for pos in agent.knownSitesPositions:
        Display.drawCircle(surface, ORANGE, pos, Config.SITE_RADIUS + 8, 2)


def drawAssignedSite(agent):
    """ Marks the site the agent is assigned to and draws a line from the agent to the site """
    if agent.getStateNumber() != DEAD:
        drawAssignmentMarker(agent.assignedSite, agent.pos, agent.getPhaseColor())
