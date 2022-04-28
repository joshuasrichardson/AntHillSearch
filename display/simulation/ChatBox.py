from Constants import BORDER_COLOR, SCREEN_COLOR
from config import Config
from display import Display
from display.mainmenu.buttons.DragButton import DragButton


class ChatBox(DragButton):

    def __init__(self):
        left = int(Display.origWidth * 2 / 3)
        top = int(Display.origHeight * 3 / 5)
        right = int(Display.origWidth * 11 / 12)
        bottom = int(Display.origHeight * 17 / 20)
        width = right - left
        height = bottom - top
        super().__init__("Chat Box", left, top, w=width, h=height)
        self.messages = []
        self.messagePositions = []
        self.bottomMargins = []
        self.dy = 0

    def draw(self):
        Display.drawRect(Display.screen, SCREEN_COLOR, self.rect, adjust=False)
        Display.drawRect(Display.screen, BORDER_COLOR, self.rect, width=3, adjust=False)
        for i, message in enumerate(self.messages):
            if self.rect.top < self.messagePositions[i][1] < self.rect.bottom - Config.FONT_SIZE * 4:
                Display.write(Display.screen, message, Config.FONT_SIZE,
                              self.messagePositions[i][0], self.messagePositions[i][1])

    def update(self, pos):
        super().update(pos)
        if self.dragging:
            for i in range(len(self.messagePositions)):
                if i == 0:
                    self.messagePositions[i] = [self.rect.x + 10, self.rect.y + 10 + self.dy]
                else:
                    prevPos = self.messagePositions[i - 1]
                    self.messagePositions[i] = [prevPos[0], prevPos[1] + self.bottomMargins[i - 1]]

    def addMessage(self, sender, message):
        lines = [f"{sender}: {message}"]
        allLinesFit = False
        while not allLinesFit:
            img = self.font.render(lines[len(lines) - 1], True, self.color)
            nextLine = ""
            while img.get_width() > self.rect.w:
                nextLine = lines[len(lines) - 1][len(lines[len(lines) - 1]) - 1] + nextLine
                lines[len(lines) - 1] = lines[len(lines) - 1][:len(lines[len(lines) - 1]) - 1]
                img = self.font.render(lines[len(lines) - 1], True, self.color).convert_alpha()
            lines.append(nextLine)
            img = self.font.render(lines[len(lines) - 1], True, self.color)
            if img.get_width() <= self.rect.w:
                allLinesFit = True

        for i, line in enumerate(lines):
            self.messages.append(line)
            if i == len(lines) - 1:
                self.bottomMargins.append(Config.FONT_SIZE * 1.5)
            else:
                self.bottomMargins.append(Config.FONT_SIZE)
            if len(self.messagePositions) > 0:
                prevPos = self.messagePositions[len(self.messagePositions) - 1]
                self.messagePositions.append([prevPos[0], prevPos[1] + self.bottomMargins[len(self.bottomMargins) - 2]])
            else:
                self.messagePositions.append([self.rect.x + 10, self.rect.y + 10])

        while self.messagePositions[len(self.messagePositions) - 1][1] >= self.rect.bottom - Config.FONT_SIZE * 4:
            self.scrollDown()

    def scrollDown(self):
        self.messagePositions = [[pos[0], pos[1] - Config.FONT_SIZE] for pos in self.messagePositions]
        self.dy -= Config.FONT_SIZE

    def scrollUp(self):
        self.messagePositions = [[pos[0], pos[1] + Config.FONT_SIZE] for pos in self.messagePositions]
        self.dy += Config.FONT_SIZE
