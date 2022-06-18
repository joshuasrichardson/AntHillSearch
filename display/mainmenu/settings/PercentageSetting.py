from display.mainmenu.settings.Setting import Setting


class PercentageSetting(Setting):
    """ A setting button used to handle percentage configurations """

    def __init__(self, key, name, x, y, showUserInput, save):
        """ key - the name of the option in the Config.py file, also the key of the data written in config.json
         name - the name of the setting as displayed in the Settings tab of the simulation
         x - the horizontal position of the left side of the button
         y - the vertical position of the top side of the button
         showUserInput - a function used to display the effects of changing the value of this setting
         save - the method used to save this value when it is updated """
        super().__init__(key, name, x, y, showUserInput, save)

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
