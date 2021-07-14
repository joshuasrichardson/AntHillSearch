""" Method for simulating a Best of N colony
Michael Goodrich
February 2019
Joshua Richardson
Summer 2021 """

from ColonySimulation import *
from recording.RecordingPlayer import RecordingPlayer
from states.AtNestState import AtNestState


def main():
    # simulation default values are:        (see Constants.py to check constants' values)
    # colony = ColonySimulation(NUM_AGENTS, SIM_DURATION, NUM_SITES, SHOULD_RECORD, SHOULD_DRAW, CONVERGENCE_FRACTION,
    #                           HUB_LOCATION, DEFAULT_SITE_SIZE, NUM_AGENTS, SITE_POSITIONS, SITE_QUALITIES, SITE_RADII,
    #                           SITE_NO_CLOSER_THAN)
    colony = ColonySimulation(sitePositions=[[500, 500], [600, 600], [550, 550], [650, 400]], siteQualities=[0, 100, 25, 255])

    # recording default values are:        (see Constants.py to check constants' values)
    # colony = RecordingPlayer(SIM_DURATION, NUM_SITES, CONVERGENCE_FRACTION, HUB_LOCATION, DEFAULT_SITE_SIZE,
    #                          NUM_AGENTS, SITE_POSITIONS, SITE_QUALITIES, SITE_RADII,
    #                          SITE_NO_CLOSER_THAN, SITE_NO_FARTHER_THAN)
    # colony = RecordingPlayer()
    try:
        # (numAgents, state, phase, siteIndex)
        # colony.addAgents(20, AtNestState, 1, 2)

        # initializeAgentList's default values are:        (see Constants.py to check constants' values)
        # colony.initializeAgentList(HOMOGENOUS_AGENTS, MIN_AGENT_SPEED, MAX_AGENT_SPEED, MIN_DECISIVENESS, MAX_DECISIVENESS,
        #                                    MIN_NAV_SKILLS, MAX_NAV_SKILLS, MIN_QUALITY_MISJUDGMENT, MAX_QUALITY_MISJUDGMENT)
        colony.initializeAgentList()

        # colony.randomizeInitialState()

        colony.runSimulation()
        print("Success!")
    except InputError:
        pass
        

main()
