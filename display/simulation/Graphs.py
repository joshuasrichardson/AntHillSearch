import pygame

from config import Config
from Constants import *
from display import Display


class SimulationGraphs:

    def __init__(self):

        self.font = pygame.font.SysFont('Comic Sans MS', Config.FONT_SIZE)  # The font used on the graphs

        self.selectAgentsRect = pygame.Rect(Display.origWidth - 3 * (14 * Config.FONT_SIZE), Display.origHeight - (7 * Config.FONT_SIZE + 2), 13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)
        self.selectSitesRect = pygame.Rect(Display.origWidth - 2 * (14.25 * Config.FONT_SIZE), Display.origHeight - (7 * Config.FONT_SIZE + 2), 13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)
        if not Config.DRAW_FAR_AGENTS:
            self.selectAgentsRect = pygame.Rect(Display.origWidth - 3 * (14 * Config.FONT_SIZE), Display.origHeight - (5 * Config.FONT_SIZE), 13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)
            self.selectSitesRect = pygame.Rect(Display.origWidth - 2 * (14.25 * Config.FONT_SIZE), Display.origHeight - (5 * Config.FONT_SIZE), 13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)
        self.selectAgentsSitesRect = pygame.Rect(Display.origWidth - 3 * (14 * Config.FONT_SIZE), Display.origHeight - (5 * Config.FONT_SIZE), 13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)
        self.selectSitesAgentsRect = pygame.Rect(Display.origWidth - 2 * (14.25 * Config.FONT_SIZE), Display.origHeight - (5 * Config.FONT_SIZE), 13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)
        self.commandSiteAgentsRect = pygame.Rect(Display.origWidth - (15 * Config.FONT_SIZE), Display.origHeight - (5 * Config.FONT_SIZE), 13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)
        self.screenBorder = None

        self.shouldDrawStateNumbers = False

    def write4(self, words, selected, box):
        """ Write the given words on the screen in the given box and change the color if it is selected """
        color = WORDS_COLOR
        if selected:
            color = SCREEN_COLOR
        if box.collidepoint(pygame.mouse.get_pos()):
            color = BLUE
        img = self.font.render(words, True, color).convert_alpha()
        Display.screen.blit(img, (box.centerx - (img.get_width() / 2),
                                  box.centery - (img.get_height() / 2)))

    def drawSelectionOptions(self, shouldSelectAgents, shouldSelectSites, shouldSelectSiteAgents, shouldSelectAgentSites,
                             commandSiteAgents):
        """ Draw boxes that can be selected to change what objects are selectable """
        if Config.DRAW_FAR_AGENTS:
            self.drawSelectBox(shouldSelectAgents, self.selectAgentsRect)
            self.write4("Select Agents", shouldSelectAgents, self.selectAgentsRect)

            self.drawSelectBox(shouldSelectSites, self.selectSitesRect)
            self.write4("Select Sites", shouldSelectSites, self.selectSitesRect)

            self.drawSelectBox(shouldSelectAgentSites, self.selectAgentsSitesRect)
            self.write4("Select Agents Sites", shouldSelectAgentSites, self.selectAgentsSitesRect)

            self.drawSelectBox(shouldSelectSiteAgents, self.selectSitesAgentsRect)
            self.write4("Select Sites Agents", shouldSelectSiteAgents, self.selectSitesAgentsRect)

            self.drawSelectBox(commandSiteAgents, self.commandSiteAgentsRect)
            self.write4("Command Site Agents", commandSiteAgents, self.commandSiteAgentsRect)

    def drawSelectBox(self, shouldSelect, rectangle):
        """ Draw a box that is either selected or not """
        color = self.getShouldSelectColor(shouldSelect)
        Display.drawRect(Display.screen, color, rectangle, adjust=False)

    @staticmethod
    def getShouldSelectColor(shouldSelect):
        return WORDS_COLOR if shouldSelect else BORDER_COLOR

    def collidesWithAnyButton(self, position):
        return self.collidesWithSelectAgentsButton(position) or \
                    self.collidesWithSelectSitesButton(position) or \
                    self.collidesWithSelectAgentsSitesButton(position) or \
                    self.collidesWithSelectSitesAgentsButton(position) or \
                    self.collidesWithCommandSiteAgentsButton(position)

    def collidesWithSelectAgentsButton(self, position):
        return self.selectAgentsRect.collidepoint(position[0], position[1])

    def collidesWithSelectSitesButton(self, position):
        return self.selectSitesRect.collidepoint(position[0], position[1])

    def collidesWithSelectAgentsSitesButton(self, position):
        return self.selectAgentsSitesRect.collidepoint(position[0], position[1])

    def collidesWithSelectSitesAgentsButton(self, position):
        return self.selectSitesAgentsRect.collidepoint(position[0], position[1])

    def collidesWithCommandSiteAgentsButton(self, position):
        return self.commandSiteAgentsRect.collidepoint(position[0], position[1])

    def drawStateNumbers(self):
        if self.shouldDrawStateNumbers:
            pos = list(pygame.mouse.get_pos())
            for i, state in enumerate(STATES_LIST):
                if i == GO:
                    break
                img = self.font.render(str(i) + ": " + state, True, WORDS_COLOR).convert_alpha()
                Display.screen.blit(img, pos)
                pos[1] += Config.FONT_SIZE

    def drawScreenBorder(self):
        if self.screenBorder is not None:
            Display.drawRect(Display.screen, ORANGE, pygame.Rect(self.screenBorder), 1, True)
