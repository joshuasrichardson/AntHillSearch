import pygame

from Constants import *


class SimulationGraphs:

    def __init__(self, screen, canSelectAnywhere=CAN_SELECT_ANYWHERE):
        self.screen = screen
        self.canSelectAnywhere = canSelectAnywhere

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 12)  # The font used on the graphs

        self.x = GRAPHS_TOP_LEFT[0]
        self.x1 = self.x + 100
        self.x2 = self.x + 350
        self.x3 = self.x + 490
        self.x4 = self.x + 540
        self.x5 = self.x + 680

        self.y = GRAPHS_TOP_LEFT[1]

        self.selectAgentsRect = pygame.Rect(self.x3, self.y + 5, 10, 10)
        self.selectSitesRect = pygame.Rect(self.x3, self.y + 16, 10, 10)
        self.selectAgentsSitesRect = pygame.Rect(self.x3, self.y + 27, 10, 10)
        self.selectSitesAgentsRect = pygame.Rect(self.x3, self.y + 38, 10, 10)
        self.commandSiteAgentsRect = pygame.Rect(self.x5, self.y + 5, 10, 10)
        self.showOptionsRect = pygame.Rect(self.x5, self.y + 16, 10, 10)

        self.shouldDrawGraphs = True

    def incrementY(self):
        self.y += 11

    def write(self, words):
        img = self.font.render(words, True, WORDS_COLOR)
        self.screen.blit(img, (self.x, self.y))

    def write2(self, words):
        img = self.font.render(words, True, WORDS_COLOR)
        self.screen.blit(img, (self.x2, self.y))

    def write4(self, words):
        img = self.font.render(words, True, WORDS_COLOR)
        self.screen.blit(img, (self.x4, self.y))

    def drawStateGraph(self, states):
        if self.shouldDrawGraphs:
            self.y = GRAPHS_TOP_LEFT[1]
            pygame.draw.rect(self.screen, BORDER_COLOR, pygame.Rect(self.x - 5, self.y - 3, self.x2 - 29, 11 * len(states) + 24), 1)
            self.write("STATES:")
            for state, width in enumerate(states):
                self.incrementY()
                pygame.draw.rect(self.screen, WORDS_COLOR, pygame.Rect(self.x1 - 1, self.y + 4, width + 2, 12))
                pygame.draw.rect(self.screen, STATE_COLORS[state], pygame.Rect(self.x1, self.y + 5, width, 10))
                self.write(STATES_LIST[state])
            self.incrementY()
            self.incrementY()
            self.incrementY()

    def drawPhaseGraph(self, phases):
        if self.shouldDrawGraphs:
            pygame.draw.rect(self.screen, BORDER_COLOR, pygame.Rect(self.x - 5, self.y - 3, self.x2 - 29, 11 * len(phases) + 24), 1)
            self.write("PHASES:")
            for phase, width in enumerate(phases):
                self.incrementY()
                pygame.draw.rect(self.screen, WORDS_COLOR, pygame.Rect(self.x1 - 1, self.y + 4, width + 2, 12))
                pygame.draw.rect(self.screen, PHASE_COLORS[phase], pygame.Rect(self.x1, self.y + 5, width, 10))
                self.write(PHASES_LIST[phase])
            self.incrementY()
            self.incrementY()
            self.incrementY()

    def drawPredictionsGraph(self, siteList):
        if self.shouldDrawGraphs:
            top = self.y - 3
            self.write("PREDICTIONS:")

            self.incrementY()
            self.write("LIKELIHOOD OF CONVERGING TO SITE:")
            numFound = 0
            for siteIndex, site in enumerate(siteList):
                if site.wasFound or site.knowSitePosAtStart:
                    numFound += 1
                    self.incrementY()
                    self.write("SITE " + str(siteList[siteIndex].getPosition()) + ": " + str(siteIndex * 10) + "%")  # TODO: Insert actual prediction here

            self.incrementY()
            self.write("PREDICTED TIME TO COVERAGE: 59 seconds")  # TODO: Insert actual predicted time here
            pygame.draw.rect(self.screen, BORDER_COLOR, pygame.Rect(self.x - 5, top, self.x2 - 29, 11 * numFound + 46), 1)
            self.incrementY()
            self.incrementY()

    def drawSelectedAgentInfo(self, agent):
        if self.shouldDrawGraphs:
            attributes = agent.getAttributes()
            pygame.draw.rect(self.screen, BORDER_COLOR, pygame.Rect(self.x - 5, self.y + 8, self.x2 - 29, 11 * len(attributes) + 13), 1)
            for i, attribute in enumerate(attributes):
                self.incrementY()
                self.write(attribute)
            self.incrementY()
            self.incrementY()

    def drawSelectedSiteInfo(self, site, agentsPositions):
        if self.shouldDrawGraphs:
            top = self.y + 8

            attributes = ["SELECTED SITE:",
                          "Position: " + str(site.getPosition()),
                          "Quality: " + str(site.getQuality()),
                          "Agent Count: " + str(site.agentCount),
                          "Agents' Positions: "]

            for position in agentsPositions:
                attributes.append(str(position))

            for i, attribute in enumerate(attributes):
                self.incrementY()
                self.write(attribute)

            pygame.draw.rect(self.screen, BORDER_COLOR, pygame.Rect(self.x - 5, top, self.x2 - 29, 11 * len(attributes) + 13), 1)

    def drawSelectionOptions(self, shouldSelectAgents, shouldSelectSites, shouldSelectSiteAgents, shouldSelectAgentSites,
                             commandSiteAgents, shouldShowOptions, paused):
        if self.shouldDrawGraphs:
            if self.canSelectAnywhere:
                self.y = GRAPHS_TOP_LEFT[1]
                self.write2("Select Agents:")
                self.drawSelectBox(shouldSelectAgents, self.selectAgentsRect)

                self.incrementY()
                self.write2("Select Sites:")
                self.drawSelectBox(shouldSelectSites, self.selectSitesRect)

                self.incrementY()
                self.write2("Select Agents Sites:")
                self.drawSelectBox(shouldSelectAgentSites, self.selectAgentsSitesRect)

                self.incrementY()
                self.write2("Select Sites Agents:")
                self.drawSelectBox(shouldSelectSiteAgents, self.selectSitesAgentsRect)

            self.y = GRAPHS_TOP_LEFT[1]
            self.write4("Command Site Agents:")
            self.drawSelectBox(commandSiteAgents, self.commandSiteAgentsRect)

            if paused:
                self.incrementY()
                self.write4("Show Options:")
                self.drawSelectBox(shouldShowOptions, self.showOptionsRect)

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

    def collidesWithOptionsButton(self, position):
        return self.showOptionsRect.collidepoint(position[0], position[1])

    def drawSelectBox(self, shouldSelect, rectangle):
        color = self.getShouldSelectColor(shouldSelect)
        pygame.draw.rect(self.screen, color, rectangle)

    @staticmethod
    def getShouldSelectColor(shouldSelect):
        if shouldSelect:
            return 0, 0, 255
        else:
            return BORDER_COLOR

    def drawOptions(self):
        x, y = self.screen.get_size()
        left = x / 4
        top = y / 4
        width = x / 2
        height = y / 2
        pygame.draw.rect(self.screen, WORDS_COLOR, pygame.Rect(left - 4, top - 4, width + 8, height + 8))
        pygame.draw.rect(self.screen, SCREEN_COLOR, pygame.Rect(left, top, width, height))
        leftMargin = x / 40

        optionsFont = pygame.font.SysFont('Comic Sans MS', 40)
        img = optionsFont.render("Options", True, WORDS_COLOR)
        self.screen.blit(img, (left * 2 - img.get_width() / 2, top - 60))
        left = left + leftMargin

        agentOptions = ['Select Agent',
                        'Wide Select',
                        'Half',
                        'Next Agent',
                        'Previous Agent',
                        'Speed Up',
                        'Slow Down',
                        'Move Agent',
                        'Assign Agent to Site',
                        'Create Agent',
                        'Delete Agent',
                        'Unselect']

        agentOptionButtons = ['- MOUSE_BUTTON (click)',
                              '- MOUSE_BUTTON (drag)',
                              '- H',
                              '- RIGHT_ARROW',
                              '- LEFT_ARROW',
                              '- F',
                              '- S',
                              '- SPACE_BAR',
                              '- A',
                              '- X',
                              '- DEL or /',
                              '- ESC']

        longerListSize = len(agentOptions)

        siteOptions = ['Select Site',
                       'Wide Select',
                       'Next Site',
                       'Previous Site',
                       'Move Site',
                       'Set Quality',
                       'Increase Quality',
                       'Decrease Quality',
                       'Expand Site',
                       'Shrink Site',
                       'Create Site',
                       'Delete Site',
                       'Tell Agents to Go',
                       'Unselect']

        siteOptionButtons = ['- MOUSE_BUTTON (click)',
                             '- MOUSE_BUTTON (drag)',
                             '- RIGHT_ARROW',
                             '- LEFT_ARROW',
                             '- MOUSE_BUTTON (drag)',
                             '- 0-9 (BACKSPACE)',
                             '- UP_ARROW',
                             '- DOWN_ARROW',
                             '- = (+)',
                             '- -',
                             '- C',
                             '- DEL or /',
                             '- SPACE_BAR',
                             '- ESC']

        if len(siteOptions) > longerListSize:
            longerListSize = len(siteOptions)

        img = self.font.render("Agent Options:", True, WORDS_COLOR)
        self.screen.blit(img, (left, top + 10))

        for i, option in enumerate(agentOptions):
            img = self.font.render(option, True, WORDS_COLOR)
            self.screen.blit(img, (left, top + 25 + (i + 1) * (height / longerListSize - 5)))

        for i, option in enumerate(agentOptionButtons):
            img = self.font.render(option, True, WORDS_COLOR)
            self.screen.blit(img, (left + 120, top + 25 + (i + 1) * (height / longerListSize - 5)))

        img = self.font.render("Site Options:", True, WORDS_COLOR)
        self.screen.blit(img, ((x / 2) + (leftMargin / 2), top + 10))

        for i, option in enumerate(siteOptions):
            img = self.font.render(option, True, WORDS_COLOR)
            self.screen.blit(img, ((x / 2) + (leftMargin / 2), top + 25 + (i + 1) * (height / longerListSize - 5)))

        for i, option in enumerate(siteOptionButtons):
            img = self.font.render(option, True, WORDS_COLOR)
            self.screen.blit(img, ((x / 2) + (leftMargin / 2) + 120, top + 25 + (i + 1) * (height / longerListSize - 5)))

    def writeBigCenter(self, words):
        font = pygame.font.SysFont('Comic Sans MS', 40)
        img = font.render(words, True, WORDS_COLOR)
        self.screen.blit(img, (self.screen.get_size()[0] / 2 - (img.get_width() / 2),
                               self.screen.get_size()[1] / 2 - (img.get_height() / 2) - 60))

    def drawPause(self):
        self.writeBigCenter("Paused")

    def drawFinish(self):
        self.writeBigCenter("Finish")
