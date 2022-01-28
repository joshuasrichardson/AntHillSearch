from display.mainmenu.settings.Setting import Setting


class IntegerSetting(Setting):

    def __init__(self, key, name, x, y, showUserInput, settingMenu):
        super().__init__(key, name, x, y, showUserInput, settingMenu)

    def initUserInput(self):
        self.value = 0
        self.userInputString = ' -> 0'

    def backspace(self):
        self.value = int(self.value / 10)
        if len(self.userInputString) > 4:
            self.userInputString = f' -> {self.userInputString[4:len(self.userInputString) - 1]}'

    def appendUserInput(self, number):
        try:
            number = int(number)
            if self.value == 0 or self.value > 250:
                self.value = number
            else:
                self.value *= 10
                self.value += number
            self.userInputString = f' -> {self.value}'
        except ValueError:
            pass
