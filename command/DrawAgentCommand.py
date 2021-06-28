from command.DrawCommand import DrawCommand


class DrawAgentCommand(DrawCommand):

    def __init__(self, agent, recorder) -> None:
        self.agent = agent.copy()
        self.surface = recorder.getSurface()

    def execute(self) -> None:
        self.agent.drawAgent(self.surface)
