from display.mainmenu.settings.StringSetting import StringSetting


class BooleanSetting(StringSetting):

    def __init__(self, key, name, x, y, showUserInput, settingMenu):
        super().__init__(key, name, x, y, showUserInput, settingMenu)

    def initUserInput(self):
        self.value = f"{not self.settingMenu.data[self.key]}"
        self.userInputString = f" -> {not self.settingMenu.data[self.key]}"
        return self.autofill == "True" or self.autofill == "T" or self.autofill == "true" or self.autofill == "t" \
            or self.autofill == "1"

    def saveValue(self):
        self.value = self.value == "True" or self.value == "T" or self.value == "true" or \
            self.value == "t" or self.value == "1"
        super().saveValue()
