from display import Display
from display.mainmenu.MenuScreen import MenuScreen
from display.buttons.Title import Title
from display.buttons.BackButton import BackButton
from display.buttons.SelectorButton import SelectorButton
from interface.EngineerInferface import EngineerInterface
from interface.UserInterface import UserInterface


class InterfaceSelector(MenuScreen):
    """ The screen where the user chooses which interface to run for their practice simulation """

    def __init__(self):
        title = Title("Select an Interface", 200)
        uiButton = SelectorButton("User Interface: Practice like you will play", UserInterface,
                                  Display.origWidth * 1 / 3, Display.origHeight / 3, self)
        eiButton = SelectorButton("Engineer Interface: See everything that is happening", EngineerInterface,
                                  Display.origWidth * 1 / 3, Display.origHeight / 3 + 100, self)
        super().__init__([title, BackButton(), uiButton, eiButton])
        self.option = None

    def chooseInterface(self):
        """ Let the user choose between the UserInterface and the EngineerInterface for the practice round """
        super().run()
        return self.option
