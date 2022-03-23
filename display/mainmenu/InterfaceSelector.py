from display import Display
from display.mainmenu.buttons.BackButton import BackButton
from display.mainmenu.MenuScreen import MenuScreen
from display.mainmenu.buttons.SelectorButton import SelectorButton
from display.mainmenu.buttons.Title import Title
from interface.EngineerInferface import EngineerInterface
from interface.UserInterface import UserInterface


class InterfaceSelector(MenuScreen):

    def __init__(self):
        title = Title("Select an Interface", 200)
        uiButton = SelectorButton("User Interface: Practice like you will play", UserInterface,
                                  Display.origWidth * 1 / 3, Display.origHeight / 3, self)
        eiButton = SelectorButton("Engineer Interface: See everything that is happening", EngineerInterface,
                                  Display.origWidth * 1 / 3, Display.origHeight / 3 + 100, self)
        super().__init__([title, BackButton(), uiButton, eiButton])
        self.option = None

    def setDataUsingConfig(self):
        """ Set the values on the screen to match the values in settings.json """
        try:
            with open(CONFIG_FILE_NAME, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print(f"File '{CONFIG_FILE_NAME}' was not found")
        except json.decoder.JSONDecodeError:
            print(f"File '{CONFIG_FILE_NAME}' is empty")

    def chooseInterface(self):
        """ Let the user choose between the UserInterface and the EngineerInterface for the practice round """
        super().run()
        return self.option
