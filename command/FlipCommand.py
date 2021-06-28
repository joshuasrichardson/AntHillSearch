import pygame

from command.DrawCommand import DrawCommand


class FlipCommand(DrawCommand):

    def __init__(self) -> None:
        pass

    def execute(self) -> None:
        pygame.display.flip()
