from display.mainmenu.settings.Setting import Setting


def DEFAULT_AUTOFILL():
    return ""


class StringSetting(Setting):
    """ A setting button used to handle string configurations """

    def __init__(self, key, name, x, y, showUserInput, save, autofill=DEFAULT_AUTOFILL):
        """ key - the name of the option in the Config.py file, also the key of the data written in config.json
         name - the name of the setting as displayed in the Settings tab of the simulation
         x - the horizontal position of the left side of the button
         y - the vertical position of the top side of the button
         showUserInput - a function used to display the effects of changing the value of this setting
         save - the method used to save this value when it is updated
         autofill - the value the option is most likely to be set to next """
        super().__init__(key, name, x, y, showUserInput, save)
        self.autofill = autofill

    def initUserInput(self):
        self.value = self.autofill()
        self.userInputString = " -> " + self.autofill()

    def backspace(self):
        if len(self.value) > 0:
            self.value = self.value[0:len(self.value) - 1]
            self.userInputString = f" -> {self.value}"

    def appendUserInput(self, letter):
        if len(self.value) == 0 or len(self.value) > 100:
            self.value = letter
        else:
            self.value += letter
        self.userInputString = f" -> {self.value}"
