""" Method for simulating a Best of N colony
Michael Goodrich
February 2019
Joshua Richardson
Summer 2021 """
import gc
import sys

from config import Randomizer
from config.ConfigIterator import ConfigIterator
from model.phases.AssessPhase import AssessPhase
from model.states.AtNestState import AtNestState

sys.path.append("")

import pygame
import time

from display.mainmenu.MainMenu import MainMenu
from interface.EngineerInferface import EngineerInterface
from interface.LiveSimulation import *
from interface.UserInterface import UserInterface
from interface.RecordingPlayer import RecordingPlayer
from interface.EmpiricalTestingInterface import EmpiricalTestingInterface
from joblib import Parallel, delayed    # noqa : F401


def main():

    try:
        # startTime = time.perf_counter()

        # Use one of the following 2 lines to play the simulation with a game-like main menu
        # MainMenu(EngineerInterface).run()  # Start up display makes it look more like a game. Comes with a main menu.
        MainMenu(UserInterface).run()

        # Use one of the following 3 lines to run one simulation with the given interface
        # runSimWithInterface(EngineerInterface())  # The interface that shows lots of information about the interface and gives lots of control over what happens
        # runSimWithInterface(UserInterface())  # The interface that only shows what is known from the hub and has limited control
        # runSimWithInterface(RecordingPlayer())  # The interface with almost no control that simply plays a recording from the recording.json file

        # Use the next three lines for empirical testing (numSimulations doesn't do anything if the 3rd parameter is True)
        # numSimulations = 1
        # resultsFileName = "antPredictions_12_07"
        # runEmpiricalTestingInterface(numSimulations, resultsFileName, True)  # The interface that does not draw and is faster than the others.

        # endTime = time.perf_counter()
        # print(f"Total time: {int((endTime - startTime) / 60)}:{(endTime - startTime) % 60}")
        # print(f"Average time: {(endTime - startTime) / numSimulations} seconds")
    except GameOver:
        exit(0)


def runSimWithInterface(colony):
    # colony.addAgents(50, AtNestState, AssessPhase(), 1)  # You can optionally add agents with specified starting positions, states, phases, and assignments in some of the interfaces
    # colony.randomizeInitialState()  # You can optionally randomize which site each agent starts from in some of the interfaces
    colony.runSimulation()  # Starts the interface
    pygame.quit()  # Clean up pygame

    print("Success!")


def runEmpiricalTestingInterface(numSimulations=1, resultsFileName=None, useConfigIter=False):
    try:
        if useConfigIter:
            iterateConfigurations(resultsFileName)
            return

        iterations = []  # A list of the number of iterations taken to complete each simulation.
        convergenceTimes = []  # A list of how long it took each colony to converge in seconds.
        chosenHomesPositions = []  # A list of the positions of the homes the agents converged to.
        chosenHomesQualities = []  # A list of the qualities of the homes the agents converged to.
        deaths = []  # A list of the number of deaths in each colony.
        totals = []  # A list of the number of total agents in each colony.
        arrivals = []  # The number of agents that got assigned to the new sites.

        for i in range(numSimulations):  # Run the simulation as many times as you want
            print(f"Simulation {i + 1}:")
            # Randomizer.randomizeConfig()
            colony = EmpiricalTestingInterface(resultsFileName)  # The interface that does not draw on the screen but instead reports to a Rest API  # TODO: Make it so you don't have to start RestAPI separately from this program
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
        if colony is not None:
            colony.timer.cancel()
        raise GameOver("Simulations canceled by user")


def test_loop(i, resultsFileName, setting):
    print(f"Simulation {i + 1}:")
    colony = EmpiricalTestingInterface(resultsFileName,
                                       setting[0].value,
                                       setting[1].value,
                                       setting[2].value,
                                       setting[3].value)
    colony.runSimulation()


def test_test_loop(i, resultsFileName, setting):
    print(f"Simulation {i + 1}:")
    print(f"{setting[0].value}, {setting[1].value}, {setting[2].value}, {setting[3].value}")


def iterateConfigurations(resultsFileName):
    # 30 * 10 * 4 * 3 * 3 * 20 = 216,000 simulations
    simsPerSetting = 30
    simsPerPos = 10
    numAgentss = [50, 100, 150, 200]
    numSitess = [2, 3, 4]
    sitesDistances = [100, 200, 300]
    qualitiess2 = [[0, 128], [0, 255], [128, 255], [50, 160], [50, 250], [160, 250],
                   [129, 128], [10, 12], [255, 245], [180, 255], [190, 245], [70, 133],
                   [110, 128], [90, 248], [140, 228], [0, 0], [255, 255], [100, 175],
                   [255, 40], [240, 2]]
    qualitiess3 = [[0, 128, 255], [0, 245, 255], [0, 128, 130], [90, 128, 255], [200, 228, 255], [250, 253, 255],
                   [0, 12, 95], [0, 12, 129], [90, 128, 144], [0, 128, 200], [76, 109, 205], [127, 128, 120],
                   [0, 0, 0], [0, 12, 25], [47, 59, 135], [9, 122, 225], [254, 128, 255], [0, 8, 255],
                   [120, 128, 255], [0, 128, 195]]
    qualitiess4 = [[0, 128, 255, 254], [0, 245, 255, 235], [0, 128, 130, 134], [90, 128, 255, 34], [200, 228, 255, 188],
                   [250, 253, 255, 249], [0, 12, 95, 54], [0, 12, 129, 255], [90, 128, 144, 0], [0, 128, 200, 212],
                   [76, 109, 205, 150], [127, 128, 120, 129], [0, 0, 0, 0], [0, 12, 25, 36], [47, 59, 135, 155],
                   [9, 122, 225, 0], [254, 128, 255, 144], [0, 8, 255, 44], [120, 128, 255, 200], [0, 128, 195, 207]]

    configIter = iter(ConfigIterator(simsPerSetting, simsPerPos, numAgentss, numSitess, sitesDistances,
                                     qualitiess2, qualitiess3, qualitiess4))

    # for (i, c) in enumerate(configIter):
    #     test_test_loop(i, resultsFileName, c)
    Parallel(n_jobs=16)(delayed(test_loop)(i, resultsFileName, c) for (i, c) in enumerate(configIter))


main()
