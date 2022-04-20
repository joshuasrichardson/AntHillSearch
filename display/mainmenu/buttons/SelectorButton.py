from ColonyExceptions import BackException
from display.mainmenu.buttons.Button import Button


class SelectorButton(Button):

    def __init__(self, optionName, optionValue, x, y, selector, action=None, screen=None):
        if action is None:
            action = self.select
        super().__init__(optionName, action, x, y, screen=screen)
        self.optionValue = optionValue
        self.selector = selector

    def select(self):
        self.selector.option = self.optionValue
        raise BackException()
