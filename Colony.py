""" Method for simulating a Best of N colony
Michael Goodrich
February 2019
Joshua Richardson
Summer 2021 """
import gc
import sys

sys.path.append("")

import pygame

from display.mainmenu.MainMenu import StartUpDisplay
from interface.EngineerInferface import EngineerInterface
from interface.LiveSimulation import *
from interface.UserInterface import UserInterface
from interface.RecordingPlayer import RecordingPlayer
from interface.EmpiricalTestingInterface import EmpiricalTestingInterface

# FIXME: Recording reports that all agents survived no matter how many died.

# Style changes
# TODO: Draw small lines around the hubs showing which directions ants left or came back
# TODO: Mark a site that has been converged to when there are multiple hubs
# TODO: Make zoom better: zoom from middle of screen, prevent zooming or scrolling out of the initial fog's area, make initial fog the same shape as the screen, when there is more than 1 hub, make sure that the fog extends beyond the farthest sites/searchable area.
# TODO: Add table of contents to tutorial and make tutorial better

# Additional features
# TODO: Have ants avoid sites that have ants from other colonies?
# TODO: Set site positions in settings by clicking where you want it to go.
# TODO: Add an option to show all current settings in the settings tab
# TODO: Think about how to display predictions


def main():
    try:
        # startUpScreen = StartUpDisplay(EngineerInterface)  # Start up display makes it look more like a game. Comes with a main menu.
        startUpScreen = StartUpDisplay(UserInterface)
        startUpScreen.run()

        # runSimWithInterface(EngineerInterface())  # The interface that shows lots of information about the interface and gives lots of control over what happens
        # runSimWithInterface(UserInterface())  # The interface that only shows what is known from the hub and has limited control
        # runSimWithInterface(RecordingPlayer())  # The interface with almost no control that simply plays a recording from the recording.json file
        # runEmpiricalTestingInterface(25)  # The interface that does not draw and is faster than the others.
    except GameOver:
        pass


def runSimWithInterface(colony):
    # colony.addAgents(50, AtNestState, AssessPhase(), 3)  # You can optionally add agents with specified starting positions, states, phases, and assignments in some of the interfaces
    # colony.randomizeInitialState()  # You can optionally randomize which site each agent starts from in some of the interfaces
    colony.runSimulation()  # Starts the interface
    pygame.quit()  # Clean up pygame

    print("Success!")


def runEmpiricalTestingInterface(numSimulations=1):
    chosenSiteQualities = []  # A list of the qualities of the sites that the agents from each hub converged to.
    convergenceTimes = []  # A list of how long it took each colony to converge in seconds.
    arrivals = []  # A list of the number of agents from each colony that arrived at their new site.
    deaths = []  # A list of the number of deaths in each colony.
    totals = []  # A list of the number of total agents in each colony.
    for i in range(numSimulations):  # Run the simulation as many times as you want
        print("Simulation " + str(i + 1) + ":")
        print()
        colony = EmpiricalTestingInterface(useRestAPI=False, useJson=True)  # The interface that does not draw on the screen but instead reports to a Rest API  # TODO: Make it so you don't have to start RestAPI separately from this program
        # colony.addAgents(50, AtNestState, AssessPhase(), 3)  # You can optionally add agents with specified starting positions, states, phases, and assignments in some of the interfaces
        results = colony.runSimulation()  # Starts the interface
        # Store results from each simulation so we can see a summary of all the simulations below.
        chosenSiteQualities.append(results[0])
        convergenceTimes.append(results[1])
        arrivals.append(results[2])
        deaths.append(results[3])
        totals.append(results[4])
        del colony
        gc.collect()

    print(f"Qualities: {chosenSiteQualities}")
    print(f"Durations: {convergenceTimes}")
    print(f"Arrivals: {arrivals}")
    print(f"Deaths: {deaths}")
    print(f"Total Agents: {totals}")


main()
