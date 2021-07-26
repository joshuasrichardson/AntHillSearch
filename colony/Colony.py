""" Method for simulating a Best of N colony
Michael Goodrich
February 2019
Joshua Richardson
Summer 2021 """

from ColonySimulation import *
from recording.RecordingPlayer import RecordingPlayer
from states.AtNestState import AtNestState


# TODO: only draw their estimated quality
# TODO: Make a display with less information that shows what we know from the hub
# TODO: Add some noise to the reports from the agents. This could be displayed as smear
# TODO: Make a path where the agents have been that evaporates over time
# TODO: Not erase the select agents sites etc.
# TODO: Add an option to make it so the hub cannot move.


def main():
    # simulation default values are:        (see Constants.py to check constants' values)
    # colony = ColonySimulation(SIM_DURATION, NUM_SITES, SHOULD_REPORT, SHOULD_RECORD, SHOULD_DRAW,
    #                           CONVERGENCE_FRACTION, HUB_LOCATION, SITE_RADIUS, NUM_AGENTS, SITE_POSITIONS,
    #                           SITE_QUALITIES, SITE_RADII, SITE_NO_CLOSER_THAN)
    colony = ColonySimulation()

    # RecordingPlayer does not take any parameters, because all the positions, assignments, states, etc. are set by the recording.json file.
    # colony = RecordingPlayer()

    # (numAgents, state, phase, siteIndex)
    # colony.addAgents(20, AtNestState, AssessPhase, 2)

    # initializeAgentList's default values are:        (see Constants.py to check constants' values)
    # colony.initializeAgentList(HOMOGENOUS_AGENTS, MIN_AGENT_SPEED, MAX_AGENT_SPEED, MIN_DECISIVENESS, MAX_DECISIVENESS,
    #                            MIN_NAV_SKILLS, MAX_NAV_SKILLS, MIN_QUALITY_MISJUDGMENT, MAX_QUALITY_MISJUDGMENT, MAX_SEARCH_DIST)
    colony.initializeAgentList()

    # colony.randomizeInitialState()

    colony.runSimulation()
    print("Success!")


main()
