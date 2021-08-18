""" Method for simulating a Best of N colony
Michael Goodrich
February 2019
Joshua Richardson
Summer 2021 """

import sys
sys.path.append("")

from interface.LiveSimulation import *
from interface.UserInterface import UserInterface
from interface.EngineerInferface import EngineerInterface
from interface.RecordingPlayer import RecordingPlayer
from interface.EmpiricalTestingInterface import EmpiricalTestingInterface


# TODO: How can we differentiate between the permanent and temporary commands and show them differently?
# TODO: Make boundary around agents round instead of square
# TODO: Make the orange circle disappear when the agents are sent to a site's old position
# TODO: Think about how to display predictions
# TODO: Make font flexible
# TODO: Make laziness and trust parameters
# TODO: Ensure that each hub has a site to move to
# Numba

# TODO: Read articles about ants, especially how they find homes
# TODO: Make more realistic
# TODO: Limit control in the User interface more (get rid of ability to set quality of hub and command agents who are selected and have moved away from the hub
# TODO: Unselect agents that go out of the range of the hub in UI
# TODO: Add more comments to net, recording, states, and user packages
# TODO: Break Controls into multiple classes (such as AgentControls, SiteControls and Controls)?
# TODO: Combine agent.assignedSiteLastKnownPos and agent.estimatedSitePosition into one variable?
# TODO: Make faster, especially the fog when it extends beyond the screen


def main():
    try:
        # runSimWithInterface(EngineerInterface())  # The interface that shows lots of information about the interface and gives lots of control over what happens
        # runSimWithInterface(UserInterface())  # The interface that only shows what is known from the hub and has limited control
        # runSimWithInterface(RecordingPlayer())  # The interface with almost no control that simply plays a recording from the recording.json file
        runEmpiricalTestingInterface(1)  # The interface that does not draw and is faster than the others.
    except GameOver:
        pass


def runSimWithInterface(colony):
    # (numAgents, state, phase, siteIndex)
    # colony.addAgents(20, AtNestState, AssessPhase(), 1)  # You can optionally add agents with specified starting positions, states, phases, and assignments in some of the interfaces
    colony.initializeAgentList()  # Create the agents that will be used in the interface
    # colony.randomizeInitialState()  # You can optionally randomize which site each agent starts from in some of the interfaces
    colony.runSimulation()  # Starts the interface

    print("Success!")


def runEmpiricalTestingInterface(numSimulations=1):
    chosenSiteQualities = []
    convergenceTimes = []
    for i in range(numSimulations):
        print("Simulation " + str(i + 1) + ":")
        colony = EmpiricalTestingInterface(shouldRecord=True, useRestAPI=False)  # The interface that does not draw on the screen but instead reports to a Rest API  # TODO: Make it so you don't have to start RestAPI separately from this program
        colony.initializeAgentList()  # Create the agents that will be used in the interface
        results = colony.runSimulation()  # Starts the interface
        chosenSiteQualities.append(results[0])
        convergenceTimes.append(results[1])
        print()
    print("Qualities: " + str(chosenSiteQualities))
    print("Durations: " + str(convergenceTimes))


main()
