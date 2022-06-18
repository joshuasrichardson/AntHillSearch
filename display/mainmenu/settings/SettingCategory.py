from config import Config
from display import Display
from display.buttons.SelectorButton import SelectorButton


class SettingCategory(SelectorButton):
    """ A button that displays the category of the settings to follow it. If this button is expanded, the settings
    in its category will be displayed and changeable. If it is collapsed, they will not be visible or changeable """

    def __init__(self, name, x, y, settings, belowSettings, adjustCategoryPositions):
        """ name - the name of the category as displayed in the Settings tab of the simulation
         x - the horizontal position of the left side of the button
         y - the vertical position of the top side of the button
         belowSettings - the settings in this category that will be drawn below the name of the category
         adjustCategoryPositions - a function used to adjust the positions of the other categories """
        super().__init__(name, name, x, y, None, self.collapseOrExpand)
        self.name = name
        self.settings = settings
        self.belowSettings = belowSettings
        self.expanded = True
        self.adjustCategoryPositions = adjustCategoryPositions

    def draw(self):
        arrow = 'v' if self.expanded else '>'
        self.rect = Display.write(Display.screen, f"{arrow} {self.name}", int(Config.FONT_SIZE * 2),
                                  self.rect.left, self.rect.top, self.color)

    def collapseOrExpand(self):
        print(f"{self.name}, {len(self.belowSettings)}, {self.expanded}")
        self.expanded = not self.expanded
        for setting in self.settings:
            setting.shouldDraw = self.expanded
        adjustment = -len(self.settings * Config.FONT_SIZE * 2)
        if self.expanded:
            adjustment = len(self.settings * Config.FONT_SIZE * 2)
        for setting in self.belowSettings:
            setting.adjustY(adjustment)
        self.adjustCategoryPositions(self, adjustment)
