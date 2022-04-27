from display.mainmenu.buttons.Button import Button


class DragButton(Button):

    def __init__(self, name, x, y, w, h, action=lambda: None):
        super().__init__(name, action, x, y, w, h)
        self.dragging = False

    def mouseButtonDown(self, pos):
        if self.collides(pos):
            self.dragging = True

    def mouseButtonUp(self, pos):
        self.dragging = False

    def update(self, pos):
        super().update(pos)
        if self.dragging:
            self.rect.center = pos
