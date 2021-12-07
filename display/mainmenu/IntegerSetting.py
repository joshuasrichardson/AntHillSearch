from display.mainmenu.Setting import Setting


class IntegerSetting(Setting):

    def __init__(self, key, name, value, rect, showUserInput, settingMenu):
        super().__init__(key, name, value, rect, showUserInput, settingMenu)

    def initUserInput(self):
        self.userInputValue = 0
        self.userInputString = ' -> 0'

    def backspace(self):
        self.userInputValue = int(self.userInputValue / 10)
        if len(self.userInputString) > 4:
            self.userInputString = f' -> {self.userInputString[4:len(self.userInputString) - 1]}'

    def appendUserInput(self, number):
        number = int(number)
        if self.userInputValue == 0 or self.userInputValue > 250:
            self.userInputValue = number
        else:
            self.userInputValue *= 10
            self.userInputValue += number
        self.userInputString = f' -> {self.userInputValue}'
