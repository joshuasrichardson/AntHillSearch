from command.DrawCommand import DrawCommand


class DrawStateGraphCommand(DrawCommand):

    def __init__(self, world, states) -> None:
        self.world = world
        self.states = states

    def execute(self) -> None:
        self.world.drawStateGraph(self.states)
