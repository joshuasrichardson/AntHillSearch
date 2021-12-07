from display.mainmenu.Setting import Setting


class PercentageSetting(Setting):

    def __init__(self, key, name, value, rect, showUserInput, settingMenu):
        super().__init__(key, name, value, rect, showUserInput, settingMenu)

    def initUserInput(self):
        self.userInputValue = 0.00
        self.userInputString = ' -> 0%'

    def backspace(self):
        if self.userInputValue == 1.00:
            self.userInputValue = 0.00
        else:
            self.userInputValue = self.truncate(self.userInputValue, len(str(self.userInputValue)) - 3)
        self.userInputString = f' -> {int(self.userInputValue * 100)}%'

    @staticmethod
    def truncate(n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier

    def appendUserInput(self, number):
        try:
            if self.userInputValue == 0.00 or (self.userInputValue > 0.10 and number != 0):
                self.userInputValue = float(number) / 100.00
            else:
                self.userInputValue *= 10
                self.userInputValue = round(self.userInputValue + (float(number) / 100.00), 2)
            if self.userInputValue > 1.0:
                self.userInputValue = 1.00
        except ValueError:
            self.userInputValue = 0.00
        self.userInputString = f' -> {int(self.userInputValue * 100)}%'
