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
# TODO: Add a setting where commands apply to agents when they arrive at the hub or a site instead of instantly.
# TODO: When new agents are created, make them the same speed as the others.
# TODO: Show site commands on the screen.
# TODO: Update the README.md file.
# TODO: Assign groups of agents with number keys like Star Craft.
# TODO: Fix recording agent numbers when additional agents are added with colony.addAgents(20, AtNestState, AssessPhase(), 2)
# TODO: Draw a line from the site to the agents' target
# TODO: Add an option to not draw the graphs as well as a way to turn them on and off during the simulation.


def main():
    # colony = ColonySimulation()
    colony = EngineerInterface()
    # colony = UserInterface()
    # colony = EmpiricalTestingInterface()  # TODO: Fix RestAPI and make it so you don't have to start it separately from this program

    # RecordingPlayer does not take any parameters, because all the positions, assignments, states, etc. are set by the recording.json file.
    # colony = RecordingPlayer()

    # (numAgents, state, phase, siteIndex)
    # colony.addAgents(20, AtNestState, AssessPhase(), 2)

    colony.initializeAgentList()

    # colony.randomizeInitialState()

    colony.runSimulation()
    print("Success!")


main()
