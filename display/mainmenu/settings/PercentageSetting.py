from display.mainmenu.settings.Setting import Setting


class PercentageSetting(Setting):

    def __init__(self, key, name, x, y, showUserInput, settingMenu):
        super().__init__(key, name, x, y, showUserInput, settingMenu)

    def initUserInput(self):
        self.value = 0.00
        self.userInputString = ' -> 0%'

    def backspace(self):
        if self.value == 1.00:
            self.value = 0.00
        else:
            self.value = self.truncate(self.value, len(str(self.value)) - 3)
        self.userInputString = f' -> {int(self.value * 100)}%'

    @staticmethod
    def truncate(n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier

    def appendUserInput(self, number):
        try:
            if self.value == 0.00 or (self.value > 0.10 and number != 0):
                self.value = float(number) / 100.00
            else:
                self.value *= 10
                self.value = round(self.value + (float(number) / 100.00), 2)
            if self.value > 1.0:
                self.value = 1.00
        except ValueError:
            self.value = 0.00
        self.userInputString = f' -> {int(self.value * 100)}%'
