from display.mainmenu.settings.Setting import Setting


def DEFAULT_AUTOFILL(self):
    return ""


class StringSetting(Setting):

    def __init__(self, key, name, categoryIndex, x, y, showUserInput, settingMenu, autofill=DEFAULT_AUTOFILL):
        super().__init__(key, name, categoryIndex, x, y, showUserInput, settingMenu)
        self.autofill = autofill

    def initUserInput(self):
        self.value = self.autofill(self)
        self.userInputString = " -> " + self.autofill(self)

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
