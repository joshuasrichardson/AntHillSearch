from display import Display
from display.mainmenu.buttons.BackButton import BackButton
from display.mainmenu.MenuScreen import MenuScreen
from display.mainmenu.buttons.SelectorButton import SelectorButton
from display.mainmenu.buttons.Title import Title
from interface.EngineerInferface import EngineerInterface
from interface.UserInterface import UserInterface


class InterfaceSelector(MenuScreen):

    def __init__(self):
        self.uiButton = SelectorButton("User Interface: Practice like you will play", UserInterface, 100, Display.origHeight / 3, self)
        self.eiButton = SelectorButton("Engineer Interface: See everything that is happening", EngineerInterface, 100, Display.origHeight / 3 + 100, self)
        super().__init__([Title("Select an Interface", 200), BackButton(), self.uiButton, self.eiButton])
        self.option = None

    def chooseInterface(self):
        """ Let the user choose between the UserInterface and the EngineerInterface for the practice round """
        super().run()
        return self.option
