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

# FIXME: Site position estimates (hub shouldn't move, and sites should not be drawn on top of the hub).

# Style changes
# TODO: Mark a site that has been converged to when there are multiple hubs.
# TODO: Make zoom better: zoom from middle of screen, prevent zooming or scrolling out of the initial fog's area, make initial fog the same shape as the screen, when there is more than 1 hub, make sure that the fog extends beyond the farthest sites/searchable area.
# TODO: Add table of contents to tutorial and make tutorial better.

# Additional features
# TODO: Set checkpoint
# TODO: Have ants avoid sites that have ants from other colonies?
# TODO: Set site positions in settings by clicking where you want it to go.
# TODO: Add an option to show all current settings in the settings tab.
# TODO: Be able to change things in settings without typing (dragging sites around, etc.).
# TODO: Think about how to display predictions.


def main():
    try:
        # StartUpDisplay(EngineerInterface).run()  # Start up display makes it look more like a game. Comes with a main menu.
        StartUpDisplay(UserInterface).run()

        # runSimWithInterface(EngineerInterface())  # The interface that shows lots of information about the interface and gives lots of control over what happens
        # runSimWithInterface(UserInterface())  # The interface that only shows what is known from the hub and has limited control
        # runSimWithInterface(RecordingPlayer())  # The interface with almost no control that simply plays a recording from the recording.json file
        # runEmpiricalTestingInterface()  # The interface that does not draw and is faster than the others.
    except GameOver:
        exit(0)


def runSimWithInterface(colony):
    # colony.addAgents(50, AtNestState, AssessPhase(), 3)  # You can optionally add agents with specified starting positions, states, phases, and assignments in some of the interfaces
    # colony.randomizeInitialState()  # You can optionally randomize which site each agent starts from in some of the interfaces
    colony.runSimulation()  # Starts the interface
    pygame.quit()  # Clean up pygame

    print("Success!")


def runEmpiricalTestingInterface(numSimulations=1):
    try:
        chosenSiteQualities = []  # A list of the qualities of the sites that the agents from each hub converged to.
        convergenceTimes = []  # A list of how long it took each colony to converge in seconds.
        chosenHomes = []  # A list of the homes the agents converged to.
        deaths = []  # A list of the number of deaths in each colony.
        totals = []  # A list of the number of total agents in each colony.
        for i in range(numSimulations):  # Run the simulation as many times as you want
            print(f"Simulation {i + 1}:")
            colony = EmpiricalTestingInterface(useRestAPI=False, useJson=True)  # The interface that does not draw on the screen but instead reports to a Rest API  # TODO: Make it so you don't have to start RestAPI separately from this program
            # colony.addAgents(50, AtNestState, AssessPhase(), 3)  # You can optionally add agents with specified starting positions, states, phases, and assignments in some of the interfaces
            results = colony.runSimulation()  # Starts the interface
            # Store results from each simulation so we can see a summary of all the simulations below.
            chosenSiteQualities.append(results["qualities"])
            convergenceTimes.append(results["simulationTime"])
            chosenHomes.append(results["chosenHomes"])
            deaths.append(results["deadAgents"])
            totals.append(results["initialHubAgentCounts"])
            del colony
            gc.collect()

        arrivals = []
        for i in range(len(chosenHomes)):
            for j, home in enumerate(chosenHomes[i]):
                arrivals.append(f"{home.agentCounts[j]}/{totals[i][j]}")

        print(f"Qualities: {chosenSiteQualities}")
        print(f"Durations: {convergenceTimes}")
        print(f"Arrivals: {arrivals}")
        print(f"Deaths: {deaths}")
        print(f"Total Agents: {totals}")
    except KeyboardInterrupt:
        colony.timer.cancel()
        raise GameOver("Simulations canceled by user")


main()
