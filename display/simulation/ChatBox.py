import pygame

from Constants import BORDER_COLOR
from config import Config
from display.mainmenu.MenuScreen import MenuScreen
from display import Display
from display.mainmenu.buttons.Button import Button
from display.mainmenu.buttons.SelectorButton import SelectorButton


class ChatBox(Button, MenuScreen):

    def __init__(self):
        self.left = int(Display.origWidth * 2 / 3)
        self.top = int(Display.origHeight * 3 / 5)
        self.right = int(Display.origWidth * 11 / 12)
        self.bottom = int(Display.origHeight * 17 / 20)
        self.width = self.right - self.left
        self.height = self.bottom - self.top
        super().__init__("Chat Box", self.drag, self.left, self.top)
        self.screen = pygame.Surface((self.width, self.height))
        self.buttons = [SelectorButton("chat", "a", 10, self.height - Config.FONT_SIZE * 2, self, action=self.type, screen=self.screen)]

    def draw(self):
        self.displayScreen()

    def type(self):
        Display.write(Display.screen, "BUHHHHH", 20, 500, 500)

    def displayScreen(self):
        super().displayScreen()
        print(str(self.rect))
        Display.drawRect(self.screen, BORDER_COLOR, pygame.Rect(0, 0, self.right - self.left,
                                                                self.bottom - self.top), width=3, adjust=False)
        Display.blitImage(Display.screen, self.screen, [self.left, self.top], False)

    def drag(self):
        print("drag")
        pos = pygame.mouse.get_pos()
        self.rect.center = pos
        self.left = pos[0]
        self.top = pos[0]
