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
from states.AtNestState import AtNestState


# TODO: Add more comments to net, recording, states, and user packages
# TODO: How can we differentiate between the permanent and temporary commands and show them differently?
# TODO: Display remaining time
# TODO: Add Pause button
# TODO: Break Agents, Site, and World, into themselves and AgentBuilder, SiteBuilder, and WorldBuilder classes?
# TODO: Break Controls into multiple classes (such as AgentControls, SiteControls and Controls)?
# TODO: Combine agent.assignedSiteLastKnownPos and agent.estimatedSitePosition into one variable?


def main():
    try:
        # colony = ColonySimulation()  # The general interface where all parameters can be set how the programmer wants
        # colony = EngineerInterface()  # The interface that shows lots of information about the simulation and gives lots of control over what happens
        # colony = UserInterface()  # The interface that only shows what is known from the hub and has limited control
        # colony = EmpiricalTestingInterface()  # The interface that does not draw on the screen but instead reports to a Rest API  # TODO: Make it so you don't have to start RestAPI separately from this program

        # RecordingPlayer does not take any parameters, because all the positions, assignments, states, etc. are set by the recording.json file.
        colony = RecordingPlayer()  # The interface with almost no control that simply plays a recording from the recording.json file

        # (numAgents, state, phase, siteIndex)
        # colony.addAgents(20, AtNestState, AssessPhase(), 1)  # You can optionally add agents with specified starting positions, states, phases, and assignments in some of the interfaces

        colony.initializeAgentList()  # Create the agents that will be used in the simulation

        # colony.randomizeInitialState()  # You can optionally randomize which site each agent starts from in some of the interfaces

        colony.runSimulation()  # Starts the simulation
        print("Success!")
    except GameOver:
        pass


main()
