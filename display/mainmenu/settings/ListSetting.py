from display.mainmenu.settings.ListStateMachine import ListStateMachine
from display.mainmenu.settings.Setting import Setting


class ListSetting(Setting):
    """ A setting button used to handle list configurations with depth of 1 """

    def __init__(self, key, name, x, y, showUserInput, save):
        """ key - the name of the option in the Config.py file, also the key of the data written in config.json
         name - the name of the setting as displayed in the Settings tab of the simulation
         x - the horizontal position of the left side of the button
         y - the vertical position of the top side of the button
         showUserInput - a function used to display the effects of changing the value of this setting
         save - the method used to save this value when it is updated """
        super().__init__(key, name, x, y, showUserInput, save)
        self.arrayStates = None

    def initUserInput(self):
        self.value = []
        self.userInputString = " -> "
        self.arrayStates = ListStateMachine(1)

    def backspace(self):
        self.userInputString = self.arrayStates.back()

    def appendUserInput(self, value):
        self.userInputString = self.arrayStates.state(value)
        if self.arrayStates.isComplete1:
            self.value = self.arrayStates.array
