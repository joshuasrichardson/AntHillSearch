""" Settings and methods related to the sites' display """
import numpy
import pygame

from config import Config
from Constants import BORDER_COLOR, SELECTED_COLOR, WORDS_COLOR, SCREEN_COLOR, STATE_COLORS, CONVERGED_COLOR
from display import Display
from display.Display import drawDashedLine, getBlurredImage, drawCircle, drawLine


def drawSite(site, pos, radius, quality, blurAmount=0):
    if site.wasFound or not Config.DRAW_ESTIMATES:
        if site.getQuality() != -1:
            color = site.getColor() if blurAmount == 0 else site.getEstimatedColor()
            Display.drawRect(Display.screen, color,
                             pygame.Rect(pos[0] + radius + Config.FONT_SIZE / 2, pos[1] - radius +
                                         ((255 - quality) / 255) * 2 * radius,
                                         Config.FONT_SIZE, (quality / 255) * 2 * radius))
            Display.drawRect(Display.screen, BORDER_COLOR,
                             pygame.Rect(pos[0] + radius + Config.FONT_SIZE / 2, pos[1] - radius,
                                         Config.FONT_SIZE, radius * 2), 1)

        if blurAmount > 0:
            drawBlurredCircle(pos, BORDER_COLOR, site.radius * 4, radius + 2, blurAmount + 0.7)
        else:
            Display.drawCircle(Display.screen, BORDER_COLOR, pos, radius + 2, 0)

        if site.isSelected:
            if blurAmount > 0:
                drawBlurredCircle(pos, SELECTED_COLOR, site.radius * 4, radius + 2, blurAmount)
            else:
                Display.drawCircle(Display.screen, SELECTED_COLOR, pos, site.radius + 2, 0)

        if blurAmount > 0:
            drawBlurredSite(site, pos, site.getEstimatedColor(), site.radius * 4, radius, blurAmount)
        else:
            Display.drawCircle(Display.screen, site.color, pos, radius, 0)

        fontSize = Config.FONT_SIZE if Display.zoom >= 0 else Config.FONT_SIZE + 3 * -Display.zoom

        if site.wasFound:
            count = site.agentCount if blurAmount == 0 else site.estimatedAgentCount
            words = f"Agents: {int(count)}" if site.isSelected else f"{int(count)}"
            img = pygame.font.SysFont('Comic Sans MS', fontSize).render(words, True, WORDS_COLOR).convert_alpha()
            Display.addToDrawLast(Display.blitImage, Display.screen, img, (pos[0] - (img.get_width() / 2),
                                                                           pos[1] - (radius + 2 * fontSize)))

        if site.isSelected and site.quality != -1:
            img = pygame.font.SysFont('Comic Sans MS', fontSize).render(f"Quality: {int(quality)}", True, WORDS_COLOR).convert_alpha()
            Display.addToDrawLast(Display.blitImage, Display.screen, img,
                                  (pos[0] - (img.get_width() / 2), pos[1] - (radius + 3 * fontSize)))  # Show the site quality above the site

        if site.chosen:
            drawConvergedMark(site)


def drawCircleLines(surface, circle, color, inc, adjust=True):
    """ Draws vertical and horizontal lines on the circle with the specified color and distance between lines """
    drawVerticalCircleLines(surface, circle, color, inc, adjust)
    drawHorizontalCircleLines(surface, circle, color, inc, adjust)


def drawVerticalCircleLines(surface, circle, color, inc, adjust=True):
    """ Draws vertical lines on the circle with the specified color and distance between lines """
    x = circle.left
    r = (circle.height / 2)
    while x < circle.right:
        o = x - circle.left
        a = numpy.sqrt(numpy.abs(numpy.square(r) - numpy.square(r - o)))
        drawLine(surface, color, (x, circle.centery - a), (x,  circle.centery + a), adjust=adjust)
        x += inc


def drawHorizontalCircleLines(surface, circle, color, inc, adjust=True):
    """ Draws horizontal lines on the circle with the specified color and distance between lines """
    y = circle.top
    r = (circle.width / 2)
    while y < circle.bottom:
        o = y - circle.top
        a = numpy.sqrt(numpy.abs(numpy.square(r) - numpy.square(r - o)))
        drawLine(surface, color, (circle.centerx - a, y), (circle.centerx + a, y), adjust=adjust)
        y += inc


def drawQuality(site):
    """ Draw the quality of the site directly on top of the site """
    img = pygame.font.SysFont('Comic Sans MS', 15).render("        ", True, WORDS_COLOR).convert_alpha()  # Make this image for all the sites to get a consistently sized rectangle
    rect = img.get_rect()
    newRect = pygame.Rect(rect.left - Display.displacementX, rect.top - Display.displacementY, rect.width, rect.height)
    Display.drawRect(img, SCREEN_COLOR, newRect)  # Draw a rectangle on top of the site so the quality will be easier to read
    Display.drawRect(img, BORDER_COLOR, newRect, 1)  # Draw a nice little border around that rectangle
    words = pygame.font.SysFont('Comic Sans MS', 12).render(str(int(site.quality)), True, WORDS_COLOR).convert_alpha()  # Draw the quality
    Display.blitImage(img, words, [((img.get_width() / 2) - (words.get_width() / 2)) - Display.displacementX, ((img.get_height() / 2) - (words.get_height() / 2)) - Display.displacementY])  # on the rectangle
    Display.blitImage(Display.screen, img, (site.pos[0] - (img.get_width() / 2), site.pos[1] - (img.get_height() / 2)))  # Draw the rectangle with the quality on it on the screen


def drawMarker(site):
    """ Draw a marker on the screen representing the command that will be applied to agents that come to the site """
    for pos in site.areasToAvoid:
        Display.drawLine(Display.screen, (155, 0, 0, 120), [pos[0] - Config.AVOID_MARKER_XY, pos[1] + Config.AVOID_MARKER_XY],
                         [pos[0] + Config.AVOID_MARKER_XY, pos[1] - Config.AVOID_MARKER_XY], 4)
        Display.drawCircle(Display.screen, (155, 0, 0, 120), pos, Config.MIN_AVOID_DIST, 4)
    lastPoint = site.pos
    for point in site.checkPoints:
        drawDashedLine(Display.screen, BORDER_COLOR, lastPoint, point)
        lastPoint = point
    if site.marker is not None:
        try:
            # Draw a dashed line from the site to the marker
            drawDashedLine(Display.screen, BORDER_COLOR, lastPoint, site.marker[1].center)
            # Draw the marker
            Display.blitImage(Display.screen, site.marker[0], site.marker[1])
        except TypeError:
            drawCircle(Display.screen, STATE_COLORS[site.marker], site.getPosition(), site.radius + 5, width=2)


def drawAssignmentMarker(site, fromPos, color):
    drawDashedLine(Display.screen, color, fromPos, site.pos)
    if not Config.DRAW_ESTIMATES:  # If the agents know where the site is
        drawAssignmentMarker2(site.siteRect, color)  # Draw the marker around the site's actual location
    else:
        try:
            drawAssignmentMarker2(site.estimatedSiteRect, color)  # Draw the marker around where the agents think it is
        except AttributeError:  # If the agents haven't estimated the position yet, an exception will be made.
            pass  # In that case, we just don't show anything


def drawAssignmentMarker2(rect, color):
    """ Draw triangles around the site that point in toward the site """
    Display.drawDownRightArrow(rect.topleft, color)
    Display.drawUpRightArrow(rect.bottomleft, color)
    Display.drawUpLeftArrow(rect.bottomright, color)
    Display.drawDownLeftArrow(rect.topright, color)


def drawBlurredCircle(pos, color, size, radius, blurAmount):
    """ Draws a blurry circle """
    image = pygame.Surface([size, size], pygame.SRCALPHA, 32)
    image = image.convert_alpha()
    pygame.draw.circle(image, color, (image.get_width() / 2, image.get_height() / 2), radius + 2, 0)
    blur = getBlurredImage(image, blurAmount)
    Display.blitImage(Display.screen, blur, (pos[0] - (blur.get_width() / 2), pos[1] - (blur.get_height() / 2)))


def drawBlurredSite(site, pos, color, size, radius, blurAmount):
    """ Draws a blurry circle with blurred lines """
    image = pygame.Surface([size, size], pygame.SRCALPHA, 32)
    image = image.convert_alpha()
    pygame.draw.circle(image, color, (image.get_width() / 2, image.get_height() / 2), radius + 2, 0)
    blur = getBlurredImage(image, blurAmount)
    site.estimatedSiteRect = pygame.Rect(pos[0] - site.estimatedRadius, pos[1] - site.estimatedRadius,
                                         site.estimatedRadius * 2, site.estimatedRadius * 2)
    Display.blitImage(Display.screen, blur, (pos[0] - (blur.get_width() / 2), pos[1] - (blur.get_height() / 2)))


def drawConvergedMark(site):
    rect = site.getSiteRect()
    Display.drawDownRightArrow(rect.topleft, CONVERGED_COLOR)
    Display.drawUpRightArrow(rect.bottomleft, CONVERGED_COLOR)
    Display.drawUpLeftArrow(rect.bottomright, CONVERGED_COLOR)
    Display.drawDownLeftArrow(rect.topright, CONVERGED_COLOR)
    Display.drawDownArrow([rect.centerx, rect.top], CONVERGED_COLOR)
    Display.drawRightArrow([rect.left, rect.centery], CONVERGED_COLOR)
    Display.drawUpArrow([rect.centerx, rect.bottom], CONVERGED_COLOR)
    Display.drawLeftArrow([rect.right, rect.centery], CONVERGED_COLOR)
