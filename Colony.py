""" Method for simulating a Best of N colony
Michael Goodrich
February 2019
Joshua Richardson
Summer 2021 """
import gc
import json
import random
import sys

import Utils
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


def main():

    try:
        # startTime = time.perf_counter()
        # MainMenu(EngineerInterface).run()  # Start up display makes it look more like a game. Comes with a main menu.
        # MainMenu(UserInterface).run()

        # runSimWithInterface(EngineerInterface())  # The interface that shows lots of information about the interface and gives lots of control over what happens
        # runSimWithInterface(UserInterface())  # The interface that only shows what is known from the hub and has limited control
        # runSimWithInterface(RecordingPlayer())  # The interface with almost no control that simply plays a recording from the recording.json file

        randomizeConfig()
        numSimulations = 1000
        resultsFileName = "antData"
        runEmpiricalTestingInterface(numSimulations, resultsFileName)  # The interface that does not draw and is faster than the others.

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


def runEmpiricalTestingInterface(numSimulations=1, resultsFileName=None):
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
            randomizeConfig()
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

        # print(f"Iterations: {iterations}")
        # print(f"Durations: {convergenceTimes}")
        # print(f"Qualities: {chosenHomesQualities}")
        # print(f"Positions: {chosenHomesPositions}")
        # print(f"Arrivals: {arrivals}")
        # print(f"Deaths: {deaths}")
        # print(f"Total Agents: {totals}")
    except KeyboardInterrupt:
        colony.timer.cancel()
        raise GameOver("Simulations canceled by user")


class Setting:
    def __init__(self, key, minimum, maximum, isFloat=False, isBool=False, isArray=False, isPos=False, numValues=1):
        self.key = key
        numberInRange = random.uniform if isFloat else random.randint
        if isArray:
            self.value = [numberInRange(minimum, maximum) for _ in range(numValues)]
        elif isPos:
            self.value = [[numberInRange(minimum, maximum), numberInRange(minimum, maximum)]
                          for _ in range(numValues)]
        elif isBool:
            self.value = numberInRange(0, 1) == 1
        else:
            self.value = numberInRange(minimum, maximum)


def randomizeConfig():
    numSitesSetting = Setting("NUM_SITES", 2, 8)
    sitePosSetting = Setting("SITE_POSITIONS", -1500, 1500, isPos=True, numValues=numSitesSetting.value)
    distances = [Utils.getDistance([0, 0], pos) for pos in sitePosSetting.value]
    maxDist = max(distances)

    settings = [
        numSitesSetting,
        Setting("SITE_RADII", 20, 60, isArray=True, numValues=numSitesSetting.value),
        Setting("SITE_QUALITIES", 0, 255, isArray=True, numValues=numSitesSetting.value),
        sitePosSetting,
        Setting("HUB_AGENT_COUNTS", 20, 200, isArray=True),
        Setting("MAX_SEARCH_DIST", maxDist, maxDist + 300, isFloat=True),
        Setting("HOMOGENOUS_AGENTS", 0, 1, isBool=True),
        Setting("MIN_AGENT_SPEED", 4, 10),
        Setting("MAX_AGENT_SPEED", 11, 15),
        Setting("COMMIT_SPEED_FACTOR", 1, 3),
        Setting("MAX_FOLLOWERS", 1, 4),
        Setting("MIN_DECISIVENESS", 0.2, 1.0, isFloat=True),
        Setting("MAX_DECISIVENESS", 1.0, 2.5, isFloat=True),
        Setting("MIN_NAV_SKILLS", 0.01, 0.3, isFloat=True),
        Setting("MAX_NAV_SKILLS", 1.0, 3.0, isFloat=True),
        Setting("MIN_QUALITY_MISJUDGMENT", 0, 30),
        Setting("MAX_QUALITY_MISJUDGMENT", 30, 100),
        Setting("AT_NEST_THRESHOLD", 4, 8),
        Setting("SEARCH_THRESHOLD", 3, 6),
        Setting("SEARCH_FROM_HUB_THRESHOLD", 6, 10),
        Setting("MAX_ASSESS_THRESHOLD", 7, 11),
        Setting("ASSESS_DIVIDEND", 40, 60),
        Setting("GET_LOST_THRESHOLD", 4, 6),
        Setting("FOLLOW_THRESHOLD", 1, 2),
        Setting("LEAD_THRESHOLD", 3, 5),
        Setting("MIN_ACCEPT_VALUE", 20, 200),
        Setting("QUORUM_DIVIDEND", 5, 9),
    ]

    # for setting in settings:
    #     print(f"{setting.key}: {setting.value}")
    setKeysValues(settings)


def setKeysValues(settings):
    with open(CONFIG_FILE_NAME, 'r') as file:
        data = json.load(file)
    for setting in settings:
        data[setting.key] = setting.value
    with open(CONFIG_FILE_NAME, 'w') as file:
        json.dump(data, file)
    Utils.copyJsonToConfig()


main()
