""" Method for simulating a Best of N colony
Michael Goodrich
February 2019
Joshua Richardson
Summer 2021 """
import gc
import sys

from model.phases.AssessPhase import AssessPhase
from model.states.AtNestState import AtNestState

sys.path.append("")

import pygame

from display.mainmenu.MainMenu import MainMenu
from interface.EngineerInferface import EngineerInterface
from interface.LiveSimulation import *
from interface.UserInterface import UserInterface
from interface.RecordingPlayer import RecordingPlayer
from interface.EmpiricalTestingInterface import EmpiricalTestingInterface


def main():

    try:
        # StartUpDisplay(EngineerInterface).run()  # Start up display makes it look more like a game. Comes with a main menu.
        MainMenu(UserInterface).run()

        # runSimWithInterface(EngineerInterface())  # The interface that shows lots of information about the interface and gives lots of control over what happens
        # runSimWithInterface(UserInterface())  # The interface that only shows what is known from the hub and has limited control
        # runSimWithInterface(RecordingPlayer())  # The interface with almost no control that simply plays a recording from the recording.json file
        # runEmpiricalTestingInterface(15)  # The interface that does not draw and is faster than the others.
    except GameOver:
        exit(0)


def runSimWithInterface(colony):
    # colony.addAgents(50, AtNestState, AssessPhase(), 1)  # You can optionally add agents with specified starting positions, states, phases, and assignments in some of the interfaces
    # colony.randomizeInitialState()  # You can optionally randomize which site each agent starts from in some of the interfaces
    colony.runSimulation()  # Starts the interface
    pygame.quit()  # Clean up pygame

    print("Success!")


def runEmpiricalTestingInterface(numSimulations=1):
    try:
        iterations = []  # A list of the number of iterations taken to complete each simulation.
        convergenceTimes = []  # A list of how long it took each colony to converge in seconds.
        chosenHomesPositions = []  # A list of the positions of the homes the agents converged to.
        chosenHomesQualities = []  # A list of the qualities of the homes the agents converged to.
        deaths = []  # A list of the number of deaths in each colony.
        totals = []  # A list of the number of total agents in each colony.
        arrivals = []  # The number of agents that got assigned to the new sites.
        for i in range(numSimulations):  # Run the simulation as many times as you want
            print(f"Simulation {i + 1}:")
            colony = EmpiricalTestingInterface()  # The interface that does not draw on the screen but instead reports to a Rest API  # TODO: Make it so you don't have to start RestAPI separately from this program
            # colony.addAgents(50, AtNestState, AssessPhase(), 3)  # You can optionally add agents with specified starting positions, states, phases, and assignments in some of the interfaces
            results = colony.runSimulation()  # Starts the interface
            # Store results from each simulation so we can see a summary of all the simulations below.
            iterations.append(results[NUM_ROUNDS_NAME])
            convergenceTimes.append(results[SIM_TIMES_NAME])
            chosenHomesQualities.append(results[HOME_QUALITIES_NAME])
            chosenHomesPositions.append(results[HOME_POSITIONS_NAME])
            deaths.append(results[NUM_DEAD_NAME])
            totals.append(results[TOTAL_NAME])
            arrivals.append(results[NUM_ARRIVALS_NAME])
            del colony
            gc.collect()

        print(f"Iterations: {iterations}")
        print(f"Durations: {convergenceTimes}")
        print(f"Qualities: {chosenHomesQualities}")
        print(f"Positions: {chosenHomesPositions}")
        print(f"Arrivals: {arrivals}")
        print(f"Deaths: {deaths}")
        print(f"Total Agents: {totals}")
    except KeyboardInterrupt:
        colony.timer.cancel()
        raise GameOver("Simulations canceled by user")


main()
