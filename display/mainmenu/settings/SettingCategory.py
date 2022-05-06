from config import Config
from display import Display
from display.buttons.SelectorButton import SelectorButton


class SettingCategory(SelectorButton):

    def draw(self):
        arrow = 'v' if self.expanded else '>'
        self.rect = Display.write(Display.screen, f"{arrow} {self.name}", int(Config.FONT_SIZE * 2),
                                  self.rect.left, self.rect.top, self.color)

    def __init__(self, name, x, y, settings, belowSettings, adjustCategoryPositions):
        super().__init__(name, name, x, y, None, self.collapseOrExpand)
        self.name = name
        self.settings = settings
        self.belowSettings = belowSettings
        self.expanded = True
        self.adjustCategoryPositions = adjustCategoryPositions

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
