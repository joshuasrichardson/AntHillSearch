import pygame

from config import Config
from Constants import *
from display import Display


class SimulationGraphs:

    def __init__(self, numAgents, controlOptions=CONTROL_OPTIONS):
        self.executedCommands = []
        self.scrollIndex = -1
        self.pageNumber = 0
        self.remainingTime = 0
        self.controlOptions = controlOptions

        self.font = pygame.font.SysFont('Comic Sans MS', Config.FONT_SIZE)  # The font used on the graphs
        self.x = GRAPHS_TOP_LEFT[0]
        self.x1 = self.x + self.font.size("TRANSPORT")[0] + 10
        self.x2 = self.x1 + numAgents + 20
        self.x3 = self.x2 + self.font.size("Select Agent Sites: ")[0] + 10
        self.x4 = self.x3 + Config.FONT_SIZE * 2
        self.x5 = self.x4 + self.font.size("Command Site Agents: ")[0] + 10

        self.y = GRAPHS_TOP_LEFT[1]
        self.y2 = Display.screen.get_height() - 100
        self.commandHistBox = pygame.draw.rect(Display.screen, BORDER_COLOR,
                                               pygame.Rect(self.x - 5, self.y2, self.x1 + (Config.FONT_SIZE * 20), 50), 1)
        self.pauseButton = pygame.draw.rect(Display.screen, BORDER_COLOR,
                                            pygame.Rect(Display.screen.get_width() - 60, self.y, 20, 20), 1)

        self.selectAgentsRect = pygame.Rect(Display.origWidth - 3 * (14 * Config.FONT_SIZE), Display.origHeight - (7 * Config.FONT_SIZE + 2), 13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)
        self.selectSitesRect = pygame.Rect(Display.origWidth - 2 * (14.25 * Config.FONT_SIZE), Display.origHeight - (7 * Config.FONT_SIZE + 2), 13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)
        if not Config.DRAW_FAR_AGENTS:
            self.selectAgentsRect = pygame.Rect(Display.origWidth - 3 * (14 * Config.FONT_SIZE), Display.origHeight - (5 * Config.FONT_SIZE), 13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)
            self.selectSitesRect = pygame.Rect(Display.origWidth - 2 * (14.25 * Config.FONT_SIZE), Display.origHeight - (5 * Config.FONT_SIZE), 13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)
        self.selectAgentsSitesRect = pygame.Rect(Display.origWidth - 3 * (14 * Config.FONT_SIZE), Display.origHeight - (5 * Config.FONT_SIZE), 13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)
        self.selectSitesAgentsRect = pygame.Rect(Display.origWidth - 2 * (14.25 * Config.FONT_SIZE), Display.origHeight - (5 * Config.FONT_SIZE), 13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)
        self.commandSiteAgentsRect = pygame.Rect(Display.origWidth - (15 * Config.FONT_SIZE), Display.origHeight - (5 * Config.FONT_SIZE), 13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)
        self.showOptionsRect = pygame.Rect(Display.origWidth / 2 - (6.5 * Config.FONT_SIZE), Display.origHeight / 2 - Config.FONT_SIZE, 13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)
        self.nextButton = None
        self.previousButton = None
        self.closeButton = None
        self.exitButton = pygame.Rect(Display.origWidth / 2 - (6.5 * Config.FONT_SIZE), Display.origHeight - 140, 13 * Config.FONT_SIZE, 2 * Config.FONT_SIZE)
        self.screenBorder = None

        self.shouldDrawGraphs = True
        self.shouldDrawStateNumbers = False

    def incrementY(self):
        self.y += Config.FONT_SIZE

    def write(self, words):
        """ Write the given words on the screen starting where the x and y coordinates are set """
        img = self.font.render(words, True, WORDS_COLOR).convert_alpha()
        Display.screen.blit(img, (self.x, self.y))

    def write2(self, words):
        """ Write the given words on the screen starting where the second x and y coordinates are set """
        img = self.font.render(words, True, WORDS_COLOR).convert_alpha()
        Display.screen.blit(img, (self.x2, self.y))

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

    def drawGraphs(self, world):
        self.drawStateGraph(world.states)
        self.drawPhaseGraph(world.phases)
        self.drawPredictionsGraph(world.siteList)
        self.drawExecutedCommands()
        self.drawRemainingTime()
        self.drawPauseButton()
        self.drawStateNumbers()

    def drawStateGraph(self, states):
        """ Draw the graph showing the number of agents in each state """
        if self.shouldDrawGraphs and Config.DRAW_FAR_AGENTS:
            self.y = GRAPHS_TOP_LEFT[1]
            pygame.draw.rect(Display.screen, BORDER_COLOR, pygame.Rect(self.x - 5, self.y - 3, self.x2 - 29, (
                        Config.FONT_SIZE - 1) * len(states) + (Config.FONT_SIZE * 2.4)), 1)
            self.write("STATES:")
            for state, width in enumerate(states):
                self.incrementY()
                pygame.draw.rect(Display.screen, WORDS_COLOR, pygame.Rect(self.x1 - 1, self.y + 4, width + 2, Config.FONT_SIZE))
                pygame.draw.rect(Display.screen, STATE_COLORS[state], pygame.Rect(self.x1, self.y + 5, width, Config.FONT_SIZE - 2))
                self.write(STATES_LIST[state])
            self.incrementY()
            self.incrementY()
            self.incrementY()

    def drawPhaseGraph(self, phases):
        """ Draw the graph showing the number of agents in each phase """
        if self.shouldDrawGraphs and Config.DRAW_FAR_AGENTS:
            pygame.draw.rect(Display.screen, BORDER_COLOR, pygame.Rect(self.x - 5, self.y - 3, self.x2 - 29, (
                        Config.FONT_SIZE - 1) * len(phases) + (Config.FONT_SIZE * 2.1)), 1)
            self.write("PHASES:")
            for phase, width in enumerate(phases):
                self.incrementY()
                pygame.draw.rect(Display.screen, WORDS_COLOR, pygame.Rect(self.x1 - 1, self.y + 4, width + 2, Config.FONT_SIZE))
                pygame.draw.rect(Display.screen, PHASE_COLORS[phase], pygame.Rect(self.x1, self.y + 5, width, Config.FONT_SIZE - 2))
                self.write(PHASES_LIST[phase])
            self.incrementY()
            self.incrementY()
            self.incrementY()

    def drawPredictionsGraph(self, siteList):
        """ Draw the graph showing the probability of converging to each site and the predicted time """
        pass
        # if self.shouldDrawGraphs:
        #     top = self.y - 3
        #     self.write("PREDICTIONS:")
        #
        #     self.incrementY()
        #     self.write("LIKELIHOOD OF CONVERGING TO SITE:")
        #     numFound = 0
        #     for siteIndex, site in enumerate(siteList):
        #         if site.wasFound or site.knowSitePosAtStart:
        #             numFound += 1
        #             self.incrementY()
        #             self.write("SITE " + str(siteList[siteIndex].getPosition()) + ": " + str(siteIndex * 10) + "%")  # TODO: Insert actual prediction here
        #
        #     self.incrementY()
        #     self.write("PREDICTED TIME TO COVERAGE: 59 seconds")  # TODO: Insert actual predicted time here
        #     pygame.draw.rect(Display.screen, BORDER_COLOR, pygame.Rect(self.x - 5, top, self.x2 - 29, 11 * numFound + 46), 1)
        #     self.incrementY()
        #     self.incrementY()

    def drawSelectionOptions(self, shouldSelectAgents, shouldSelectSites, shouldSelectSiteAgents, shouldSelectAgentSites,
                             commandSiteAgents, shouldShowOptions, paused):
        """ Draw boxes that can be selected to change what objects are selectable """
        if self.shouldDrawGraphs:
            if Config.DRAW_FAR_AGENTS:
                self.drawSelectBox(shouldSelectAgents, self.selectAgentsRect)
                self.write4("Select Agents", shouldSelectAgents, self.selectAgentsRect)

                self.drawSelectBox(shouldSelectSites, self.selectSitesRect)
                self.write4("Select Sites", shouldSelectSites, self.selectSitesRect)

                self.drawSelectBox(shouldSelectAgentSites, self.selectAgentsSitesRect)
                self.write4("Select Agents Sites", shouldSelectAgentSites, self.selectAgentsSitesRect)

                self.drawSelectBox(shouldSelectSiteAgents, self.selectSitesAgentsRect)
                self.write4("Select Sites Agents", shouldSelectSiteAgents, self.selectSitesAgentsRect)

            if len(self.controlOptions["siteOptions"]) > 5:  # If it's not the recording interface
                self.drawSelectBox(commandSiteAgents, self.commandSiteAgentsRect)
                self.write4("Command Site Agents", commandSiteAgents, self.commandSiteAgentsRect)

            if paused:
                self.drawSelectBox(shouldShowOptions, self.showOptionsRect)
                self.write4("Options", shouldShowOptions, self.showOptionsRect)

    def drawSelectBox(self, shouldSelect, rectangle):
        """ Draw a box that is either selected or not """
        color = self.getShouldSelectColor(shouldSelect)
        Display.drawRect(Display.screen, color, rectangle, adjust=False)

    @staticmethod
    def getShouldSelectColor(shouldSelect):
        return WORDS_COLOR if shouldSelect else BORDER_COLOR

    def collidesWithAnyButton(self, position, paused):
        return self.collidesWithSelectAgentsButton(position) or \
                    self.collidesWithSelectSitesButton(position) or \
                    self.collidesWithSelectAgentsSitesButton(position) or \
                    self.collidesWithSelectSitesAgentsButton(position) or \
                    self.collidesWithCommandSiteAgentsButton(position) or \
                    self.collidesWithOptionsButton(position, paused) or \
                    self.collidesWithPauseButton(position) or \
                    self.collidesWithNextButton(position, paused) or \
                    self.collidesWithPreviousButton(position, paused) or \
                    self.collidesWithCloseButton(position, paused) or \
                    self.collidesWithExitButton(position, paused)

    def collidesWithSelectAgentsButton(self, position):
        return self.selectAgentsRect.collidepoint(position[0], position[1])

    def collidesWithSelectSitesButton(self, position):
        return self.selectSitesRect.collidepoint(position[0], position[1])

    def collidesWithSelectAgentsSitesButton(self, position):
        return self.selectAgentsSitesRect.collidepoint(position[0], position[1])

    def collidesWithSelectSitesAgentsButton(self, position):
        return self.selectSitesAgentsRect.collidepoint(position[0], position[1])

    def collidesWithCommandSiteAgentsButton(self, position):
        return self.commandSiteAgentsRect.collidepoint(position[0], position[1]) \
               and len(self.controlOptions["siteOptions"]) > 5

    def collidesWithOptionsButton(self, position, paused):
        return paused and self.showOptionsRect.collidepoint(position[0], position[1])

    def collidesWithPauseButton(self, position):
        return self.pauseButton.collidepoint(position[0], position[1])

    def collidesWithNextButton(self, position, paused):
        return self.nextButton is not None and paused and self.nextButton.collidepoint(position)

    def collidesWithPreviousButton(self, position, paused):
        return self.previousButton is not None and paused and self.previousButton.collidepoint(position)

    def collidesWithCloseButton(self, position, paused):
        return self.closeButton is not None and paused and self.closeButton.collidepoint(position)

    def collidesWithExitButton(self, position, paused):
        return self.exitButton is not None and paused and self.exitButton.collidepoint(position)

    def drawStateNumbers(self):
        if self.shouldDrawStateNumbers:
            pos = list(pygame.mouse.get_pos())
            for i, state in enumerate(STATES_LIST):
                if i == GO:
                    break
                img = self.font.render(str(i) + ": " + state, True, WORDS_COLOR).convert_alpha()
                Display.screen.blit(img, pos)
                pos[1] += Config.FONT_SIZE

    def nextScreen(self):
        self.pageNumber = 1

    def previousScreen(self):
        self.pageNumber = 0

    def drawOptions(self):
        x, y = Display.screen.get_size()
        left = x / 4
        top = y / 4
        width = x / 2
        height = y / 2
        pygame.draw.rect(Display.screen, WORDS_COLOR, pygame.Rect(left - 4, top - 4, width + 8, height + 8))
        pygame.draw.rect(Display.screen, SCREEN_COLOR, pygame.Rect(left, top, width, height))
        leftMargin = x / 40

        optionsFont = pygame.font.SysFont('Comic Sans MS', Config.LARGE_FONT_SIZE)
        img = optionsFont.render("Options", True, WORDS_COLOR).convert_alpha()
        Display.screen.blit(img, (left * 2 - img.get_width() / 2, top - 60))
        left = left + leftMargin
        if self.pageNumber == 0:
            color = WORDS_COLOR
            if self.collidesWithNextButton(pygame.mouse.get_pos(), True):
                color = BLUE
            self.drawOptionsPage0(left, top, height, leftMargin, x)
            nextImg = self.font.render("NEXT >", True, color).convert_alpha()
            self.nextButton = pygame.Rect(x * 3 / 4 - 2 * nextImg.get_width(), top + height - 25,
                                          nextImg.get_width(), nextImg.get_height())
            Display.screen.blit(nextImg, self.nextButton.topleft)
        else:
            color = WORDS_COLOR
            if self.collidesWithPreviousButton(pygame.mouse.get_pos(), True):
                color = BLUE
            self.drawOptionsPage1(left, top, height)
            prevImg = self.font.render("< PREVIOUS", True, color).convert_alpha()
            self.previousButton = pygame.Rect(x * 1 / 4 + prevImg.get_width() / 2, top + height - 25,
                                              prevImg.get_width(), prevImg.get_height())
            Display.screen.blit(prevImg, self.previousButton.topleft)

        color = WORDS_COLOR
        if self.collidesWithCloseButton(pygame.mouse.get_pos(), True):
            color = BLUE
        closeImg = self.font.render("CLOSE", True, color).convert_alpha()
        self.closeButton = pygame.Rect(x * 3 / 4 - 2 * closeImg.get_width(), top + 10,
                                       closeImg.get_width(), closeImg.get_height())
        Display.screen.blit(closeImg, self.closeButton.topleft)

        pygame.draw.rect(Display.screen, SCREEN_COLOR, self.exitButton)
        pygame.draw.rect(Display.screen, WORDS_COLOR, self.exitButton, 2)
        self.write4("Exit Simulation", False, self.exitButton)

    def drawOptionsPage0(self, left, top, height, leftMargin, x):
        agentOptions = self.controlOptions["agentOptions"]
        agentOptionButtons = self.controlOptions["agentOptionButtons"]

        longerListSize = len(agentOptions)

        siteOptions = self.controlOptions["siteOptions"]
        siteOptionButtons = self.controlOptions["siteOptionButtons"]

        if len(siteOptions) > longerListSize:
            longerListSize = len(siteOptions)

        img = self.font.render("Agent Options:", True, WORDS_COLOR).convert_alpha()
        Display.screen.blit(img, (left, top + 10))

        for i, option in enumerate(agentOptions):
            img = self.font.render(option, True, WORDS_COLOR).convert_alpha()
            Display.screen.blit(img, (left, top + 25 + (i + 1) * (height / longerListSize - 5)))

        for i, option in enumerate(agentOptionButtons):
            img = self.font.render(option, True, WORDS_COLOR).convert_alpha()
            Display.screen.blit(img, (left + 120, top + 25 + (i + 1) * (height / longerListSize - 5)))

        img = self.font.render("Site Options:", True, WORDS_COLOR).convert_alpha()
        Display.screen.blit(img, ((x / 2) + (leftMargin / 2), top + 10))

        for i, option in enumerate(siteOptions):
            img = self.font.render(option, True, WORDS_COLOR).convert_alpha()
            Display.screen.blit(img, ((x / 2) + (leftMargin / 2), top + 25 + (i + 1) * (height / longerListSize - 5)))

        for i, option in enumerate(siteOptionButtons):
            img = self.font.render(option, True, WORDS_COLOR).convert_alpha()
            Display.screen.blit(img, ((x / 2) + (leftMargin / 2) + 120, top + 25 + (i + 1) * (height / longerListSize - 5)))

    def drawOptionsPage1(self, left, top, height):
        options = ['Pause',
                   'Zoom In',
                   'Zoom Out',
                   'Move Camera',
                   'Lock Screen',
                   'Show/Hide Graphs',
                   'Show/Hide Options',
                   'Enable/Disable',
                   'Expand/Shrink History Box',
                   'Scroll Through History']

        optionButtons = ['- P',
                         '- CTRL + MOUSE WHEEL UP',
                         '- CTRL + MOUSE WHEEL DOWN',
                         '- Move MOUSE to edge of screen',
                         '- CAPS LOCK',
                         '- G',
                         '- O',
                         '- LEFT CLICK (the corresponding box on the screen)',
                         '- DRAG LEFT CLICK',
                         '- MOUSE WHEEL UP/DOWN']

        img = self.font.render("Other Options:", True, WORDS_COLOR).convert_alpha()
        Display.screen.blit(img, (left, top + 10))

        for i, option in enumerate(options):
            img = self.font.render(option, True, WORDS_COLOR).convert_alpha()
            Display.screen.blit(img, (left, top + 25 + (i + 1) * (height / 16 - 5)))

        for i, option in enumerate(optionButtons):
            img = self.font.render(option, True, WORDS_COLOR).convert_alpha()
            Display.screen.blit(img, (left + 180, top + 25 + (i + 1) * (height / 16 - 5)))

    def addExecutedCommand(self, command):
        self.executedCommands.append('{:003d}'.format(int(self.remainingTime)) + ": " + command)
        self.scrollIndex = len(self.executedCommands) - 1

    def drawExecutedCommands(self):
        if self.shouldDrawGraphs and len(self.executedCommands) > 0:
            self.y2 = self.commandHistBox.top + 4
            pygame.draw.rect(Display.screen, BORDER_COLOR, self.commandHistBox, 1)

            if self.scrollIndex != len(self.executedCommands) - 1:
                self.drawScrollUpArrow()

            lastIndex = self.scrollIndex
            for i in range(self.scrollIndex, -1, -1):
                if self.y2 + 15 > self.commandHistBox.bottom:
                    break
                lastIndex = i
                command = self.executedCommands[i]
                img = self.font.render(command, True, WORDS_COLOR).convert_alpha()
                Display.screen.blit(img, (self.x, self.y2))
                self.y2 += 11

            if lastIndex > 0:
                self.drawScrollDownArrow()

    def drawScrollUpArrow(self):
        pygame.draw.line(Display.screen, BORDER_COLOR, [self.commandHistBox.right - 16, self.commandHistBox.top + 10],
                         [self.commandHistBox.right - 12, self.commandHistBox.top + 6])
        pygame.draw.line(Display.screen, BORDER_COLOR, [self.commandHistBox.right - 12, self.commandHistBox.top + 6],
                         [self.commandHistBox.right - 8, self.commandHistBox.top + 10])

    def drawScrollDownArrow(self):
        pygame.draw.line(Display.screen, BORDER_COLOR, [self.commandHistBox.right - 16, self.commandHistBox.bottom - 10],
                         [self.commandHistBox.right - 12, self.commandHistBox.bottom - 6])
        pygame.draw.line(Display.screen, BORDER_COLOR, [self.commandHistBox.right - 12, self.commandHistBox.bottom - 6],
                         [self.commandHistBox.right - 8, self.commandHistBox.bottom - 10])

    def collidesWithCommandHistBoxTop(self, pos):
        return abs(pos[1] - self.commandHistBox.top) < 3 and \
               abs(pos[0] - self.commandHistBox.centerx) <= (self.commandHistBox.width / 2)

    def setHistBoxTop(self, top):
        self.commandHistBox = pygame.Rect(self.commandHistBox.left, top, self.commandHistBox.width,
                                          self.commandHistBox.height + self.commandHistBox.top - top)

    def scrollUp(self):
        if self.scrollIndex < len(self.executedCommands) - 1:
            self.scrollIndex += 1

    def scrollDown(self):
        if self.scrollIndex > 0:
            self.scrollIndex -= 1

    def drawPauseButton(self):
        if self.shouldDrawGraphs:
            borderRect = pygame.draw.rect(Display.screen, BORDER_COLOR, self.pauseButton, 1)
            color = WORDS_COLOR
            if borderRect.collidepoint(pygame.mouse.get_pos()):
                color = BLUE
            pygame.draw.rect(Display.screen, color, (self.pauseButton.left + 4, self.pauseButton.top + 3,
                                                     self.pauseButton.width / 4, self.pauseButton.height / 3 * 2 + 1))
            pygame.draw.rect(Display.screen, color, (self.pauseButton.left + 11, self.pauseButton.top + 3,
                                                     self.pauseButton.width / 4, self.pauseButton.height / 3 * 2 + 1))

    def drawPlayButton(self):
        if self.shouldDrawGraphs:
            borderRect = pygame.draw.rect(Display.screen, BORDER_COLOR, self.pauseButton, 1)
            color = WORDS_COLOR
            if borderRect.collidepoint(pygame.mouse.get_pos()):
                color = BLUE
            pygame.draw.polygon(Display.screen, color, [[self.pauseButton.left + 4, self.pauseButton.top + 4],
                                                        [self.pauseButton.right - 4, self.pauseButton.centery],
                                                        [self.pauseButton.left + 4, self.pauseButton.bottom - 4]])

    def setRemainingTime(self, seconds):
        self.remainingTime = seconds

    def drawRemainingTime(self):
        if self.shouldDrawGraphs:
            if Config.USE_ROUNDS_AS_DURATION:
                img = self.font.render(str(round(self.remainingTime)) + '/' + str(Config.SIM_DURATION), True, WORDS_COLOR).convert_alpha()
            else:
                img = self.font.render(str(round(self.remainingTime)), True, WORDS_COLOR).convert_alpha()
            Display.screen.blit(img, (Display.origWidth - 125, img.get_height()))

    def drawScreenBorder(self):
        if self.shouldDrawGraphs and self.screenBorder is not None:
            Display.drawRect(Display.screen, ORANGE, pygame.Rect(self.screenBorder), 1, True)
