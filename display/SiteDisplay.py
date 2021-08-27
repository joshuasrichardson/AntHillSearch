""" Settings and methods related to the sites' display """
import pygame

from Constants import BORDER_COLOR, SELECTED_COLOR, WORDS_COLOR, SCREEN_COLOR, DRAW_ESTIMATES
from display import Display
from display.Display import drawCircleLines, drawDashedLine, getBlurredImage


knowSitePosAtStart = DRAW_ESTIMATES  # Whether the user knows where the sites are at the start of the interface


def drawSite(site):
    """ Draws the site and some things associated with it on the screen """
    if site.wasFound or knowSitePosAtStart:  # If the agents have already discovered the site
        Display.drawCircle(Display.screen, BORDER_COLOR, site.pos, site.radius + 2, 0)  # Draw a background for the site that blends with the surface better than the site color
        if site.isSelected:
            Display.drawCircle(Display.screen, SELECTED_COLOR, site.pos, site.radius + 2, 0)  # Draw a circle over the background showing that the site is selected
        site.siteRect = pygame.Rect(site.pos[0] - site.radius, site.pos[1] - site.radius, site.radius * 2, site.radius * 2)
        Display.drawCircle(Display.screen, site.color, site.pos, site.radius, 0)  # Draw a circle the color representing the quality of the site
        drawCircleLines(Display.screen, site.siteRect, BORDER_COLOR, site.getDensity(site.quality))  # Draw grid lines representing the quality of the site (more lines is worse)
        img = pygame.font.SysFont('Comic Sans MS', 12).render(str(site.agentCount), True, BORDER_COLOR).convert_alpha()
        Display.blitImage(Display.screen, img, (site.pos[0] - (img.get_width() / 2), site.pos[1] - (site.radius + 20)))  # Show the number of agents assigned to the site above the site
        if site.isSelected:
            drawQuality(site)  # Draw the site's quality right in the middle of it if it is selected.


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
    if site.marker is not None:
        # Draw a dashed line from the site to the marker
        drawDashedLine(Display.screen, BORDER_COLOR, site.pos, site.marker[1].center)
        # Draw the marker
        Display.blitImage(Display.screen, site.marker[0], site.marker[1])


def drawAssignmentMarker(site, fromPos, color):
    drawDashedLine(Display.screen, color, fromPos, site.pos)
    if knowSitePosAtStart:  # If the agents know where the site is
        drawAssignmentMarker2(site.siteRect, color)  # Draw the marker around the site's actual location
    else:
        try:
            drawAssignmentMarker2(site.estimatedSiteRect, color)  # Draw the marker around where the agents think it is
        except:  # If the agents haven't estimated the position yet, an exception will be made.
            pass  # In that case, we just don't show anything


def drawAssignmentMarker2(rect, color):
    """ Draw triangles around the site that point in toward the site """
    Display.drawRightArrow([rect.left, rect.centery], color)
    Display.drawLeftArrow([rect.right, rect.centery], color)
    Display.drawUpArrow([rect.centerx, rect.bottom], color)
    Display.drawDownArrow([rect.centerx, rect.top], color)


def drawEstimatedSite(site):
    """ Draws what the user knows about the site from the hub """
    # Only draw the site if it has been found, or if the site positions are all known at the start of the interface
    if site.wasFound or knowSitePosAtStart:
        # Draw a background behind the site to make it blend with the screen better
        drawBlurredCircle(site.estimatedPosition, BORDER_COLOR, site.radius * 4,
                          site.estimatedRadius + site.blurRadiusDiff + 2, site.blurAmount + 0.7)

        if site.isSelected:  # Draw the selection circle
            drawBlurredCircle(site.estimatedPosition, SELECTED_COLOR, site.radius * 4,
                              site.estimatedRadius + site.blurRadiusDiff + 2, site.blurAmount)

        color = site.getEstimatedColor()  # Gets a color based on the estimated value of the site
        drawBlurredSite(site, site.estimatedPosition, color, site.radius * 4,
                        site.estimatedRadius + site.blurRadiusDiff, site.blurAmount)  # Draws the site with lines representing the quality and blurriness representing how well known the site is

        img = pygame.font.SysFont('Comic Sans MS', 12).render(str(int(site.estimatedAgentCount)), True, BORDER_COLOR).convert_alpha()  # Draw the estimated number of agents assigned to the site
        Display.blitImage(Display.screen, img, (site.estimatedPosition[0] - (img.get_width() / 2),
                          site.estimatedPosition[1] - (site.estimatedRadius + site.blurRadiusDiff + 24)))


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
    rect = pygame.draw.circle(image, color, (image.get_width() / 2, image.get_height() / 2), radius + 2, 0)
    drawCircleLines(image, rect, BORDER_COLOR, getDensity(site.estimatedQuality), False)
    blur = getBlurredImage(image, blurAmount)
    site.estimatedSiteRect = (pos[0] - (blur.get_width() / 2), pos[1] - (blur.get_height() / 2))
    Display.blitImage(Display.screen, blur, (pos[0] - (blur.get_width() / 2), pos[1] - (blur.get_height() / 2)))


def getDensity(quality):
    """ Get the space between lines """
    return int(quality / 20) + 2
