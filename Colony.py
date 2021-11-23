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
# TODO: Set site positions in settings by clicking where you want it to go.
# TODO: Draw small lines around the hubs showing which directions ants left or came back
# TODO: Mark a site that has been converged to when there are multiple hubs
# TODO: Make zoom better: zoom from middle of screen, prevent zooming or scrolling out of the initial fog's area, make initial fog the same shape as the screen, when there is more than 1 hub, make sure that the fog extends beyond the farthest sites/searchable area.
# TODO: Add table of contents to tutorial and make tutorial better

# Additional features
# TODO: Add ability to remove an avoid place
# TODO: Have ants avoid harmful places https://www.pbs.org/wgbh/nova/article/how-ants-respond-to-predators-suggests-superorganism-capabilities/
# TODO: Have ants report when they see a dead ant or a predator.
# TODO: Earthquakes?
# TODO: Have ants avoid sites that have ants from other colonies?
# TODO: Add an option to show all current settings in the settings tab
# TODO: Think about how to display predictions


def main():
    try:
        # startUpScreen = StartUpDisplay(EngineerInterface)
        startUpScreen = StartUpDisplay(UserInterface)
        startUpScreen.run()

        # runSimWithInterface(EngineerInterface())  # The interface that shows lots of information about the interface and gives lots of control over what happens
        # runSimWithInterface(UserInterface(numSites=10, numHubs=2))  # The interface that only shows what is known from the hub and has limited control
        # runSimWithInterface(RecordingPlayer())  # The interface with almost no control that simply plays a recording from the recording.json file
        # runEmpiricalTestingInterface(5)  # The interface that does not draw and is faster than the others.
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
    arrivals = []
    deaths = []
    totals = []
    for i in range(numSimulations):
        print("Simulation " + str(i + 1) + ":")
        colony = EmpiricalTestingInterface(numHubs=1, shouldRecord=False, useRestAPI=False, useJson=False,
                                           numPredators=1, simulationDuration=60)  # The interface that does not draw on the screen but instead reports to a Rest API  # TODO: Make it so you don't have to start RestAPI separately from this program
        # colony.addAgents(50, AtNestState, AssessPhase(), 3)  # You can optionally add agents with specified starting positions, states, phases, and assignments in some of the interfaces
        results = colony.runSimulation()  # Starts the interface
        chosenSiteQualities.append(results[0])
        convergenceTimes.append(results[1])
        arrivals.append(results[2])
        deaths.append(results[3])
        totals.append(results[4])
        print()
    print(f"Qualities: {chosenSiteQualities}")
    print(f"Durations: {convergenceTimes}")
    print(f"Arrivals: {arrivals}")
    print(f"Deaths: {deaths}")
    print(f"Total Agents: {totals}")


main()
