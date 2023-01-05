from user.RecordingControls import RecordingControls


class NoControls(RecordingControls):

    def __init__(self, agentList, world, disp):
        """ agentList - a list of all the agents in the simulation
        world - the world with objects for the user to interact with
        selectRect - the rectangle used to select agents and sites
        disp - the display for the simulation that handles drawing things on the screen
        changeDelay - a function used to change how much time is added between each round of the simulation """
        super().__init__(agentList, world, disp, None)

    def speedUp(self, pos):
        pass

    def slowDown(self, pos):
        pass
