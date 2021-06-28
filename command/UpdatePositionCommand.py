from command.DrawCommand import DrawCommand


class UpdatePositionCommand(DrawCommand):

    def __init__(self, agent, pos) -> None:
        self.agent = agent
        self.pos = pos

    def execute(self) -> None:
        self.agent.updatePosition(self.pos)
