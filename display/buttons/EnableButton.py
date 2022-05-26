import pygame.mouse

from Constants import SCREEN_COLOR, WORDS_COLOR, BLUE
from config import Config
from display import Display
from display.buttons.Box import Box


class EnableButton(Box):
    def __init__(self, name, action, activated, visible, x, y, w=0, h=0, recenter=False, canActivate=True,
                 fontSize=Config.FONT_SIZE):
        self.childAction = action
        super().__init__(name, self.enableOrDisable, x, y, w, h, bgColor=WORDS_COLOR if activated else SCREEN_COLOR,
                         fontSize=fontSize)
        self.canActivate = canActivate
        self.activated = activated
        self.visible = visible
        if recenter:
            self.rect.left = self.rect.left - self.rect.width / 2

    def draw(self):
        """ Draw a box that is either selected or not """
        if self.visible:
            super().draw()
            Display.blitImage(Display.screen, self.image,
                              [self.rect.left + self.rect.width / 2 - self.image.get_width() / 2,
                               self.rect.top + self.rect.height / 2 - self.image.get_height() / 2], False)

    def collides(self, pos):
        if self.visible:
            return super().collides(pos)

    def enableOrDisable(self):
        if self.canActivate:
            self.activated = not self.activated
            self.update(pygame.mouse.get_pos())
        self.childAction()

    def update(self, pos):
        if self.collides(pos):
            self.changeColor(BLUE)
        elif self.activated:
            self.changeColor(SCREEN_COLOR)
        else:
            self.changeColor(WORDS_COLOR)
        self.bgColor = WORDS_COLOR if self.activated else SCREEN_COLOR
