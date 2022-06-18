from ColonyExceptions import BackException
from display.buttons.Button import Button


class SelectorButton(Button):
    """ A button used to select an option; particularly useful in the settings tab """

    def __init__(self, optionName, optionValue, x, y, selector, action=None):
        """ optionName - the name of the option to be selected
        optionValue - the initial value associated with the option
        x - the horizontal position of the left side of the button
        y - the vertical position of the top side of the button
        selector - the screen that owns this button; control will return to that screen when the new optionValue is set """
        if action is None:
            action = self.select
        super().__init__(optionName, action, x, y)
        self.optionValue = optionValue
        self.selector = selector

    def select(self):
        self.selector.option = self.optionValue
        raise BackException()
