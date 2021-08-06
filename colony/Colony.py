""" Method for simulating a Best of N colony
Michael Goodrich
February 2019
Joshua Richardson
Summer 2021 """

import sys
sys.path.append("")

from colony.simulation.ColonySimulation import *
from colony.simulation.EngineerInferface import EngineerInterface
from colony.simulation.UserInterface import UserInterface
from colony.simulation.EmpiricalTestingInterface import EmpiricalTestingInterface
from recording.RecordingPlayer import RecordingPlayer


# TODO: Update the README.md file, add more comments throughout the code, and refactor.
# TODO: separate agent colors
# TODO: Find a format to show the information on the left without having the users need to read it.
# TODO: Save a list of the commands the user executed, and show that on the screen. How can we differentiate between the permanent and temporary commands and show them differently?
# TODO: Show where agents have explored
# TODO: Make the path drawing in UI look better


def main():
    try:
        # colony = ColonySimulation()
        # colony = EngineerInterface()
        colony = UserInterface()
        # colony = EmpiricalTestingInterface()  # TODO: Make it so you don't have to start RestAPI separately from this program

        # RecordingPlayer does not take any parameters, because all the positions, assignments, states, etc. are set by the recording.json file.
        # colony = RecordingPlayer()

        # (numAgents, state, phase, siteIndex)
        # colony.addAgents(20, AtNestState, AssessPhase(), 1)

        colony.initializeAgentList()

        # colony.randomizeInitialState()

        colony.runSimulation()
        print("Success!")
    except GameOver:
        pass


main()
