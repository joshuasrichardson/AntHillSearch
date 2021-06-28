from command.DrawCommand import DrawCommand


class DrawWorldObjectsCommand(DrawCommand):

    def __init__(self, world) -> None:
        self.world = world

    def execute(self) -> None:
        self.world.drawWorldObjects()
