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
# TODO: Think about how to display predictions
# TODO: Make laziness and trust parameters
# TODO: Read articles about ants, especially how they find homes and make more realistic
# TODO: Update the ant movements to be more ant-like instead of random (if there is a cool way to do that).
# TODO: Limit control in the User interface more (get rid of ability to command agents who are selected and have moved away from the hub and dont move or select sites anywhere)
# TODO: Add more comments to net, recording, states, and user packages
# TODO: Break Controls into multiple classes (such as AgentControls, SiteControls and Controls) to simplify it?
# TODO: Add commands to change the state of agents (not just to GO but to AT_NEST or whatever).

# TODO: Update README


def main():
    try:
        # runSimWithInterface(EngineerInterface())  # The interface that shows lots of information about the interface and gives lots of control over what happens
        # runSimWithInterface(UserInterface())  # The interface that only shows what is known from the hub and has limited control
        runSimWithInterface(RecordingPlayer())  # The interface with almost no control that simply plays a recording from the recording.json file
        # runEmpiricalTestingInterface(1)  # The interface that does not draw and is faster than the others.
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
        colony = EmpiricalTestingInterface(hubAgentCounts=[20, 20, 20, 20], shouldRecord=True, useRestAPI=False)  # The interface that does not draw on the screen but instead reports to a Rest API  # TODO: Make it so you don't have to start RestAPI separately from this program
        colony.initializeAgentList(hubAgentCounts=[20, 20, 20, 20])  # Create the agents that will be used in the interface
        results = colony.runSimulation()  # Starts the interface
        chosenSiteQualities.append(results[0])
        convergenceTimes.append(results[1])
        print()
    print("Qualities: " + str(chosenSiteQualities))
    print("Durations: " + str(convergenceTimes))


main()
