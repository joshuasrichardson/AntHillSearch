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
from model.phases.AssessPhase import AssessPhase
from model.states.AtNestState import AtNestState


# FIXME: Warning in Site.py
# TODO: Have ants avoid sites that have ants from other colonies or that have dead ants around it?
# TODO: Add rivers, cliffs, and stuff like that?
# TODO: Think about how to display predictions
# TODO: Add more comments to net, recording, states, and user packages
# TODO: Break Controls into multiple classes (such as AgentControls, SiteControls and Controls) to simplify it?

# TODO: Think about what kinds of things we want to study in the user studies.
# In empirical studies, test the difference between high urgency (low minimum acceptance quality, small quorum, and high recruitment probability) and low urgency (high minimum acceptance quality, large quorum, and low recruitment probability), and see how much faster high urgency is.


def main():
    try:
        runSimWithInterface(EngineerInterface(numSites=5, numHubs=2))  # The interface that shows lots of information about the interface and gives lots of control over what happens
        # runSimWithInterface(UserInterface(numSites=3))  # The interface that only shows what is known from the hub and has limited control
        # runSimWithInterface(RecordingPlayer())  # The interface with almost no control that simply plays a recording from the recording.json file
        # runEmpiricalTestingInterface(1)  # The interface that does not draw and is faster than the others.
    except GameOver:
        pass


def runSimWithInterface(colony):
    # colony.addAgents(50, AtNestState, AssessPhase(), 3)  # You can optionally add agents with specified starting positions, states, phases, and assignments in some of the interfaces

    # colony.randomizeInitialState()  # You can optionally randomize which site each agent starts from in some of the interfaces
    colony.runSimulation()  # Starts the interface

    print("Success!")


def runEmpiricalTestingInterface(numSimulations=1):
    chosenSiteQualities = []
    convergenceTimes = []
    for i in range(numSimulations):
        print("Simulation " + str(i + 1) + ":")
        colony = EmpiricalTestingInterface(hubAgentCounts=[50, 50, 50, 50], shouldRecord=True, useRestAPI=False)  # The interface that does not draw on the screen but instead reports to a Rest API  # TODO: Make it so you don't have to start RestAPI separately from this program
        # colony.addAgents(50, AtNestState, AssessPhase(), 3)  # You can optionally add agents with specified starting positions, states, phases, and assignments in some of the interfaces
        results = colony.runSimulation()  # Starts the interface
        chosenSiteQualities.append(results[0])
        convergenceTimes.append(results[1])
        print()
    print("Qualities: " + str(chosenSiteQualities))
    print("Durations: " + str(convergenceTimes))


main()
