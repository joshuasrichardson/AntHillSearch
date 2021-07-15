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
    # colony = ColonySimulation(SIM_DURATION, NUM_SITES, SHOULD_REPORT, SHOULD_RECORD, SHOULD_DRAW,
    #                           CONVERGENCE_FRACTION, HUB_LOCATION, SITE_RADIUS, NUM_AGENTS, SITE_POSITIONS,
    #                           SITE_QUALITIES, SITE_RADII, SITE_NO_CLOSER_THAN)
    colony = ColonySimulation(shouldReport=False, siteQualities=[0, 10, 20, 255], sitePositions=[[400, 400], [500, 500], [600, 600], [650, 400]])

    # recording default values are:        (see Constants.py to check constants' values)
    # colony = RecordingPlayer(SIM_DURATION, NUM_SITES, CONVERGENCE_FRACTION, HUB_LOCATION, SITE_RADIUS,
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
