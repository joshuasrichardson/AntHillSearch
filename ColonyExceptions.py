class Error(Exception):
    """Base class for exceptions in the swarm simulator."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
        value -- the token that caused the error
    """

    def __init__(self, message, value):
        print(f"{message}:({value})")


class BackException(Error):
    def __init__(self, message=""):
        self.message = message
        print(f"{message}")


class GameOver(Error):
    """Exception raised to end the simulation.

    Attributes:
        message -- explanation of the error
        value -- the token that caused the error
    """

    def __init__(self, message):
        self.message = message
        print(f"{message}")
