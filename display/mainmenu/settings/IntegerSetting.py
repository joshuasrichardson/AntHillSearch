from display.mainmenu.settings.Setting import Setting


class IntegerSetting(Setting):
    """ A setting button used to handle integer configurations """

    def __init__(self, key, name, x, y, showUserInput, save):
        """ key - the name of the option in the Config.py file, also the key of the data written in config.json
         name - the name of the setting as displayed in the Settings tab of the simulation
         x - the horizontal position of the left side of the button
         y - the vertical position of the top side of the button
         showUserInput - a function used to display the effects of changing the value of this setting
         save - the method used to save this value when it is updated """
        super().__init__(key, name, x, y, showUserInput, save)

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
