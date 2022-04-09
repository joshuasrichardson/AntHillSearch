from display.mainmenu.settings.StringSetting import StringSetting
from config import Config  # This is important for initUserInput.


class BooleanSetting(StringSetting):

    def __init__(self, key, name, x, y, showUserInput, settingMenu):
        super().__init__(key, name, x, y, showUserInput, settingMenu, self.getAutofill)

    def getAutofill(self):
        return str(not eval(f"Config.{self.key}"))

    def saveValue(self):
        self.value = self.value == "True" or self.value == "T" or self.value == "true" or \
            self.value == "t" or self.value == "1"
        super().saveValue()
