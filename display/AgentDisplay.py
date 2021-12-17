""" Methods related to the agents' display """
import numpy as np
import pygame

from Constants import BORDER_COLOR, SCREEN_COLOR, FOLLOW_COLOR, SITE_RADIUS, AGENT_IMAGE, ASSESS_COLOR, HUB_OBSERVE_DIST
from display import Display
from display.Display import rotateImage, drawDashedLine, getDestinationMarker
from display.SiteDisplay import drawAssignmentMarker


agentImage = AGENT_IMAGE


def drawAgent(agent, surface):
    if not Display.drawFarAgents:
        if agent.isClose(agent.getHub().getPosition(), HUB_OBSERVE_DIST):
            drawPath(agent, surface)  # If we are only drawing close agents, then only show their path when they are close to the hub and can report it. Else this part is taken care of in the world display class.
        else:
            drawLastKnownPos(agent)
    if Display.drawFarAgents or agent.isClose(agent.getHub().getPosition(), HUB_OBSERVE_DIST):
        if agent.isTheSelected:  # Only draw the following for one of the selected agents
            drawKnownSiteMarkers(agent, surface)
            drawAssignedSite(agent)
            setAgentMarker(agent)
            drawPlacesToAvoid(agent, surface)
        if agent.isSelected:  # Only draw state and phase circles for the selected agents
            Display.drawCircle(surface, agent.getStateColor(), agent.agentRect.center, agent.agentHandle.get_width() * 3 / 5, 2)
            Display.drawCircle(surface, agent.getPhaseColor(), agent.agentRect.center, agent.agentHandle.get_width() * 3 / 4, 2)
        w, h = agent.agentHandle.get_size()  # Rotate the agent's image to face the direction they are heading
        rotateImage(surface, agent.agentHandle, agent.pos, [w / 2, h / 2], (-agent.angle * 180 / np.pi) - 132)


def drawLastKnownPos(agent):
    Display.drawCircle(Display.screen, agent.lastKnownPhaseColor, agent.lastSeenPos, 3, adjust=True)


def getAgentImage(pos):
    """ Loads, adjusts the size, and returns the image representing an agent """
    agent = pygame.image.load(agentImage)
    if Display.shouldDraw:
        agent = agent.convert_alpha()
    if agent.get_size()[0] > 30 or agent.get_size()[1] > 30:
        agent = pygame.transform.scale(agent, (30, 30))
        rect = agent.get_rect().move(pos)
        rect.center = pos
    return agent


def setAgentMarker(agent):
    """ Draws the position on the screen that the agent is heading toward """
    if agent.target is not None:
        agent.marker = getDestinationMarker(agent.target)
    else:
        agent.marker = None


def drawMarker(agent, surface):
    """ Draws the agent's specified marker on the screen (i.e. the go marker) """
    if (Display.drawFarAgents or agent.isCloseToHub()) \
            and agent.marker is not None:
        drawDashedLine(surface, BORDER_COLOR, agent.pos, agent.marker[1].center)
        Display.blitImage(Display.screen, agent.marker[0], agent.marker[1])


def drawPlacesToAvoid(agent, surface):
    """ Draws the places the agent should avoid on the screen """
    if Display.drawFarAgents or agent.isCloseToHub():
        for marker in agent.avoidMarkers:
            drawDashedLine(surface, ASSESS_COLOR, agent.pos, marker[1].center, width=4, dashLength=3)
            Display.blitImage(Display.screen, marker[0], marker[1])


def drawPath(agent, surface):
    """ Draws a path behind the agent the fades as it gets farther away from them """
    color = SCREEN_COLOR
    for pos in agent.path:
        color = color[0] - 1,  color[1] - 1, color[2] - 1
        Display.drawCircle(surface, color, pos, 2)


def drawKnownSiteMarkers(agent, surface):
    """ Draws a circle around each site the agent knows about """
    for pos in agent.knownSitesPositions:
        Display.drawCircle(surface, FOLLOW_COLOR, pos, SITE_RADIUS + 8, 2)


def drawAssignedSite(agent):
    """ Marks the site the agent is assigned to and draws a line from the agent to the site """
    drawAssignmentMarker(agent.assignedSite, agent.pos, agent.getPhaseColor())
