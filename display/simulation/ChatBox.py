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

    def draw(self):
        Display.drawRect(Display.screen, SCREEN_COLOR, self.rect, adjust=False)
        Display.drawRect(Display.screen, BORDER_COLOR, self.rect, width=3, adjust=False)
        for i, message in enumerate(self.messages):
            Display.write(Display.screen, message, Config.FONT_SIZE, self.messagePositions[i][0], self.messagePositions[i][1])

    def update(self, pos):
        super().update(pos)
        if self.dragging:
            for i in range(len(self.messagePositions)):
                if i == 0:
                    self.messagePositions[i] = [self.rect.x + 10, self.rect.y + 10]
                else:
                    prevPos = self.messagePositions[i - 1]
                    self.messagePositions[i] = [prevPos[0], prevPos[1] + Config.FONT_SIZE * 1.5]

    def addMessage(self, sender, message):
        self.messages.append(f"{sender}: {message}")
        if len(self.messagePositions) > 0:
            prevPos = self.messagePositions[len(self.messagePositions) - 1]
            self.messagePositions.append([prevPos[0], prevPos[1] + Config.FONT_SIZE * 1.5])
        else:
            self.messagePositions.append([self.rect.x + 10, self.rect.y + 10])
