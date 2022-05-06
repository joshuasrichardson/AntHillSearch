from display.buttons.Button import Button


class Page(Button):

    def __init__(self, fileName, y, number, caller):
        super().__init__(fileName, lambda: None, 0, y)
        self.fileName = fileName
        self.caller = caller
        self.number = number

    def draw(self):
        if self.caller.pageNumber == self.number:
            self.caller.drawPage()
