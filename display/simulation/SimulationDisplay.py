from display.mainmenu.MenuScreen import MenuScreen
from display.simulation.ChatBox import ChatBox


class SimulationDisplay(MenuScreen):

    def __init__(self):
        self.chatBox = ChatBox()
        super().__init__([self.chatBox])
        self.screens = [self.chatBox]

    def handleEvents(self):
        super().handleEvents()
        for screen in self.screens:
            screen.handleEvents()

    def displayScreen(self):
        for button in self.buttons:
            button.draw()

    def escape(self):
        pass

    def scrollUp(self, times=1):
        pass

    def scrollDown(self, times=1):
        pass
