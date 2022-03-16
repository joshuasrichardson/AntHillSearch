from display.mainmenu.settings.ArrayStateMachine import ArrayStateMachine
from display.mainmenu.settings.Setting import Setting


class ListSetting(Setting):

    def __init__(self, key, name, categoryIndex, x, y, showUserInput, settingMenu):
        super().__init__(key, name, categoryIndex, x, y, showUserInput, settingMenu)
        self.arrayStates = None

    def initUserInput(self):
        self.value = []
        self.userInputString = " -> "
        self.arrayStates = ArrayStateMachine(1)

    def backspace(self):
        self.userInputString = self.arrayStates.back()

    def appendUserInput(self, value):
        self.userInputString = self.arrayStates.state(value)
        if self.arrayStates.isComplete1:
            self.value = self.arrayStates.array
