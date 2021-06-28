from command.DrawCommand import DrawCommand


class FillCommand(DrawCommand):

    def __init__(self, color, surface) -> None:
        self.color = color
        self.surface = surface

    def execute(self) -> None:
        self.surface.fill(self.color)
