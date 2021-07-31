""" Method for simulating a Best of N colony
Michael Goodrich
February 2019
Joshua Richardson
Summer 2021 """

from ColonySimulation import *
from colony.EmpiricalTestingInterface import EmpiricalTestingInterface
from colony.EngineerInferface import EngineerInterface
from colony.UserInterface import UserInterface
from recording.RecordingPlayer import RecordingPlayer
from states.AtNestState import AtNestState


# TODO: Estimate site radii
# TODO: Display the estimated position of sites as a smear that grow more clear as it is visited more
# TODO: Make a path where the agents have been that evaporates over time
# TODO: Update the README.md file.


def main():
    try:
        # colony = ColonySimulation()
        colony = EngineerInterface()
        # colony = UserInterface()
        # colony = EmpiricalTestingInterface()  # TODO: Make it so you don't have to start RestAPI separately from this program

        # RecordingPlayer does not take any parameters, because all the positions, assignments, states, etc. are set by the recording.json file.
        # colony = RecordingPlayer()

        # (numAgents, state, phase, siteIndex)
        # colony.addAgents(20, AtNestState, AssessPhase(), 2)

        colony.initializeAgentList()

        # colony.randomizeInitialState()

        colony.runSimulation()
        print("Success!")
    except GameOver:
        pass


main()
