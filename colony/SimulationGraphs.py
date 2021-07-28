import pygame

from Constants import *


class SimulationGraphs:

    def __init__(self, screen):
        self.screen = screen

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 12)  # The font used on the graphs

        self.x = GRAPHS_TOP_LEFT[0]
        self.x1 = self.x + 100
        self.x2 = self.x + 350
        self.x3 = self.x + 490
        self.x4 = self.x + 540
        self.x5 = self.x + 640

        self.y = GRAPHS_TOP_LEFT[1]

        self.selectAgentsRect = pygame.Rect(self.x3, self.y + 5, 10, 10)
        self.selectSitesRect = pygame.Rect(self.x3, self.y + 16, 10, 10)
        self.selectAgentsSitesRect = pygame.Rect(self.x3, self.y + 27, 10, 10)
        self.selectSitesAgentsRect = pygame.Rect(self.x3, self.y + 38, 10, 10)
        self.showOptionsRect = pygame.Rect(self.x5, self.y + 5, 10, 10)

    def incrementY(self):
        self.y += 11

    def drawStateGraph(self, states):
        self.y = GRAPHS_TOP_LEFT[1]
        img = self.font.render("STATES:", True, (0, 0, 0))
        self.screen.blit(img, (self.x, self.y))
        for state, width in enumerate(states):
            self.incrementY()
            pygame.draw.rect(self.screen, STATE_COLORS[state], pygame.Rect(self.x1, self.y + 5, width, 10))
            img = self.font.render(STATES_LIST[state], True, STATE_COLORS[state])
            self.screen.blit(img, (self.x, self.y))
        self.incrementY()
        self.incrementY()
        self.incrementY()

    def drawPhaseGraph(self, phases):
        img = self.font.render("PHASES:", True, (0, 0, 0))
        self.screen.blit(img, (self.x, self.y))
        for phase, width in enumerate(phases):
            self.incrementY()
            pygame.draw.rect(self.screen, PHASE_COLORS[phase], pygame.Rect(self.x1, self.y + 5, width, 10))
            img = self.font.render(PHASES_LIST[phase], True, PHASE_COLORS[phase])
            self.screen.blit(img, (self.x, self.y))
        self.incrementY()
        self.incrementY()
        self.incrementY()

    def drawPredictionsGraph(self, siteList):
        img = self.font.render("PREDICTIONS:", True, (0, 0, 0))
        self.screen.blit(img, (self.x, self.y))

        self.incrementY()
        img = self.font.render("LIKELIHOOD OF CONVERGING TO SITE:", True, (0, 0, 0))
        self.screen.blit(img, (self.x, self.y))
        for siteIndex, site in enumerate(siteList):
            if site.wasFound:
                self.incrementY()
                img = self.font.render("SITE " + str(siteList[siteIndex].getPosition()) + ": " +
                                       str(siteIndex * 10) + "%", True, (0, 0, 0))  # TODO: Insert actual probability here
                self.screen.blit(img, (self.x, self.y))

        self.incrementY()
        img = self.font.render("PREDICTED TIME TO COVERAGE: 59 seconds", True, (0, 0, 0))  # TODO: Insert actual predicted time here
        self.screen.blit(img, (self.x, self.y))
        self.incrementY()
        self.incrementY()

    def drawSelectedAgentInfo(self, agent):
        attributes = agent.getAttributes()
        for i, attribute in enumerate(attributes):
            self.incrementY()
            img = self.font.render(attribute, True, (0, 0, 0))
            self.screen.blit(img, (self.x, self.y))
        self.incrementY()
        self.incrementY()

    def drawSelectedSiteInfo(self, site, agentsPositions):
        attributes = ["SELECTED SITE:",
                      "Position: " + str(site.getPosition()),
                      "Quality: " + str(site.getQuality()),
                      "Agent Count: " + str(site.agentCount),
                      "Agents' Positions: "]

        for position in agentsPositions:
            attributes.append(str(position))

        for i, attribute in enumerate(attributes):
            self.incrementY()
            img = self.font.render(attribute, True, (0, 0, 0))
            self.screen.blit(img, (self.x, self.y))

    def drawSelectionOptions(self, shouldSelectAgents, shouldSelectSites, shouldSelectSiteAgents, shouldSelectAgentSites,
                             shouldShowOptions, paused):
        if CAN_SELECT_ANYWHERE:
            self.y = GRAPHS_TOP_LEFT[1]
            selectAgentsColor = self.getShouldSelectColor(shouldSelectAgents)
            img = self.font.render("Select Agents:", True, (0, 0, 0))
            self.screen.blit(img, (self.x2, self.y))
            pygame.draw.rect(self.screen, selectAgentsColor, self.selectAgentsRect)

            self.incrementY()
            selectSitesColor = self.getShouldSelectColor(shouldSelectSites)
            img = self.font.render("Select Sites:", True, (0, 0, 0))
            self.screen.blit(img, (self.x2, self.y))
            pygame.draw.rect(self.screen, selectSitesColor, self.selectSitesRect)

            self.incrementY()
            selectAgentsSitesColor = self.getShouldSelectColor(shouldSelectAgentSites)
            img = self.font.render("Select Agents Sites:", True, (0, 0, 0))
            self.screen.blit(img, (self.x2, self.y))
            pygame.draw.rect(self.screen, selectAgentsSitesColor, self.selectAgentsSitesRect)

            self.incrementY()
            selectSitesAgentsColor = self.getShouldSelectColor(shouldSelectSiteAgents)
            img = self.font.render("Select Sites Agents:", True, (0, 0, 0))
            self.screen.blit(img, (self.x2, self.y))
            pygame.draw.rect(self.screen, selectSitesAgentsColor, self.selectSitesAgentsRect)

        if paused:
            self.y = GRAPHS_TOP_LEFT[1]
            showOptionsColor = self.getShouldSelectColor(shouldShowOptions)
            img = self.font.render("Show Options:", True, (0, 0, 0))
            self.screen.blit(img, (self.x4, self.y))
            pygame.draw.rect(self.screen, showOptionsColor, self.showOptionsRect)

    def collidesWithSelectAgentsButton(self, position):
        return self.selectAgentsRect.collidepoint(position[0], position[1])

    def collidesWithSelectSitesButton(self, position):
        return self.selectSitesRect.collidepoint(position[0], position[1])

    def collidesWithSelectAgentsSitesButton(self, position):
        return self.selectAgentsSitesRect.collidepoint(position[0], position[1])

    def collidesWithSelectSitesAgentsButton(self, position):
        return self.selectSitesAgentsRect.collidepoint(position[0], position[1])

    def collidesWithOptionsButton(self, position):
        return self.showOptionsRect.collidepoint(position[0], position[1])

    @staticmethod
    def getShouldSelectColor(shouldSelect):
        if shouldSelect:
            return 0, 0, 255
        else:
            return 120, 120, 120

    def drawOptions(self):
        x, y = self.screen.get_size()
        left = x / 4
        top = y / 4
        width = x / 2
        height = y / 2
        pygame.draw.rect(self.screen, (0, 128, 128), pygame.Rect(left - 4, top - 4, width + 8, height + 8))
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(left, top, width, height))
        leftMargin = x / 40

        optionsFont = pygame.font.SysFont('Comic Sans MS', 40)
        img = optionsFont.render("Options", True, (123, 123, 123))
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
                        'Delete Agent']

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
                              '- DEL or /']

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
                       'Delete Site']

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
                             '- DEL or /']

        if len(siteOptions) > longerListSize:
            longerListSize = len(siteOptions)

        img = self.font.render("Agent Options:", True, (0, 0, 0))
        self.screen.blit(img, (left, top + 10))

        for i, option in enumerate(agentOptions):
            img = self.font.render(option, True, (0, 0, 0))
            self.screen.blit(img, (left, top + 25 + (i + 1) * (height / longerListSize - 5)))

        for i, option in enumerate(agentOptionButtons):
            img = self.font.render(option, True, (0, 0, 0))
            self.screen.blit(img, (left + 120, top + 25 + (i + 1) * (height / longerListSize - 5)))

        img = self.font.render("Site Options:", True, (0, 0, 0))
        self.screen.blit(img, ((x / 2) + (leftMargin / 2), top + 10))

        for i, option in enumerate(siteOptions):
            img = self.font.render(option, True, (0, 0, 0))
            self.screen.blit(img, ((x / 2) + (leftMargin / 2), top + 25 + (i + 1) * (height / longerListSize - 5)))

        for i, option in enumerate(siteOptionButtons):
            img = self.font.render(option, True, (0, 0, 0))
            self.screen.blit(img, ((x / 2) + (leftMargin / 2) + 120, top + 25 + (i + 1) * (height / longerListSize - 5)))

    def drawPause(self):
        pausedFont = pygame.font.SysFont('Comic Sans MS', 40)
        img = pausedFont.render("Paused", True, (123, 123, 123))
        self.screen.blit(img, (self.screen.get_size()[0] / 2 - (img.get_width() / 2), self.screen.get_size()[1] / 2 - (img.get_height() / 2)))

    def drawFinish(self):
        finishFont = pygame.font.SysFont('Comic Sans MS', 40)
        img = finishFont.render("Finished", True, (123, 123, 123))
        self.screen.blit(img, (self.screen.get_size()[0] / 2 - (img.get_width() / 2), self.screen.get_size()[1] / 2 - (img.get_height() / 2)))
