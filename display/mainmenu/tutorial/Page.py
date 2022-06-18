from display.buttons.Button import Button


class Page(Button):
    """ A page of the tutorial """

    def __init__(self, fileName, number, caller):
        """ fileName - the name of the file that has a picture of this page of the tutorial
        number - the order of the page (page 1, page 2, etc)
        caller - the menu screen that has control over the page """
        super().__init__(fileName, lambda: None, 0, 0)
        self.fileName = fileName
        self.caller = caller
        self.number = number

    def draw(self):
        if self.caller.pageNumber == self.number:
            self.caller.drawPage()
