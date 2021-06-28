from command.DrawCommand import DrawCommand


class DrawPhaseGraphCommand(DrawCommand):

    def __init__(self, world, phases) -> None:
        self.world = world
        self.phases = phases

    def execute(self) -> None:
        self.world.drawPhaseGraph(self.phases)
