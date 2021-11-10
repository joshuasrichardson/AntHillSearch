""" Method for simulating a Best of N colony
Michael Goodrich
February 2019
Joshua Richardson
Summer 2021 """

import sys

sys.path.append("")

import pygame

from display.mainmenu.MainMenu import StartUpDisplay
from interface.EngineerInferface import EngineerInterface
from interface.LiveSimulation import *
from interface.UserInterface import UserInterface
from interface.RecordingPlayer import RecordingPlayer
from interface.EmpiricalTestingInterface import EmpiricalTestingInterface

# Style changes
# TODO: Report how many made it to the new home.
# TODO: Set site positions in settings by clicking where you want it to go.
# TODO: Show how many ants are currently at a site next to how many are assigned there: "currentlyPresent/assigned"
# TODO: Draw small lines around the hubs showing which directions ants left or came back
# TODO: Mark a site that has been converged to when there are multiple hubs
# TODO: Make zoom better: zoom from middle of screen, prevent zooming or scrolling out of the initial fog's area, make initial fog the same shape as the screen, when there is more than 1 hub, make sure that the fog extends beyond the farthest sites/searchable area.
# TODO: Add more comments to the code and refactor
# TODO: Add table of contents to tutorial and make tutorial better

# Additional features
# TODO: Have ants avoid harmful places https://www.pbs.org/wgbh/nova/article/how-ants-respond-to-predators-suggests-superorganism-capabilities/
# TODO: Add predators, and have ants report when they see a dead ant or a predator. Be able to enable/disable them
# TODO: Record the commands executed by the user
# TODO: Add an option to set how many recordings you want to store, and store the previous n recordings.
# TODO: Earthquakes?
# TODO: Add traps and have ants avoid sites that have ants from other colonies or that have dead ants around them?
# TODO: Add an option to show all current settings in the settings tab
# TODO: Think about how to display predictions


# TODO: Read other studies to know what kinds of things they are testing and what metrics they are using.
# TODO: Think about what kinds of things we want to study in the user studies.
# In empirical studies, test the difference between high urgency (low minimum acceptance quality, small quorum, and high recruitment probability) and low urgency (high minimum acceptance quality, large quorum, and low recruitment probability), and see how much faster high urgency is.
# The relationship between the time of their first control and the time of the simulation
# Try limiting the number of times they can execute commands.
# Give 3 different tutorials - Thorough, surface level, and just play around.
# Test earthquake recovery skills
# Test how well they do with different numbers of hubs.
# Test different maxSearchDists
# Set predators next to best site and have the user get the second best site, or the best one that is safe. Keep track of number of survivors.


def main():
    try:
        # startUpScreen = StartUpDisplay(EngineerInterface)
        startUpScreen = StartUpDisplay(UserInterface)
        startUpScreen.run()

        # runSimWithInterface(EngineerInterface())  # The interface that shows lots of information about the interface and gives lots of control over what happens
        # runSimWithInterface(UserInterface(numSites=10, numHubs=2))  # The interface that only shows what is known from the hub and has limited control
        # runSimWithInterface(RecordingPlayer())  # The interface with almost no control that simply plays a recording from the recording.json file
        # runEmpiricalTestingInterface(1)  # The interface that does not draw and is faster than the others.
    except GameOver:
        pass


def runSimWithInterface(colony):
    # colony.addAgents(50, AtNestState, AssessPhase(), 3)  # You can optionally add agents with specified starting positions, states, phases, and assignments in some of the interfaces

    # colony.randomizeInitialState()  # You can optionally randomize which site each agent starts from in some of the interfaces
    colony.runSimulation()  # Starts the interface
    pygame.quit()

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
