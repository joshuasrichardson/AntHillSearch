from display.mainmenu.settings.StringSetting import StringSetting


class BooleanSetting(StringSetting):

    def __init__(self, key, name, categoryIndex, x, y, showUserInput, settingMenu):
        super().__init__(key, name, categoryIndex, x, y, showUserInput, settingMenu)

    def initUserInput(self):
        self.value = f"{not self.settingMenu.data[self.key]}"
        self.userInputString = f" -> {not self.settingMenu.data[self.key]}"
        return self.autofill == "True" or self.autofill == "T" or self.autofill == "true" or self.autofill == "t" \
            or self.autofill == "1"

    def getUserInput(self):
        boolString = super().getUserInput()
        self.value = boolString == "True" or boolString == "T" or boolString == "true" or boolString == "t" \
            or boolString == "1"
        return self.value
