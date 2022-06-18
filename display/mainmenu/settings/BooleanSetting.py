from display.mainmenu.settings.StringSetting import StringSetting
from config import Config  # This is important for getAutofill.


class BooleanSetting(StringSetting):
    """ A setting button used to handle boolean configurations """

    def __init__(self, key, name, x, y, showUserInput, save):
        """ key - the name of the option in the Config.py file, also the key of the data written in config.json
         name - the name of the setting as displayed in the Settings tab of the simulation
         x - the horizontal position of the left side of the button
         y - the vertical position of the top side of the button
         showUserInput - a function used to display the effects of changing the value of this setting
         save - the method used to save this value when it is updated """
        super().__init__(key, name, x, y, showUserInput, save, self.getAutofill)

    def getAutofill(self):
        return str(not eval(f"Config.{self.key}"))

    def saveValue(self):
        self.value = self.value == "True" or self.value == "T" or self.value == "true" or \
            self.value == "t" or self.value == "1"
        super().saveValue()
