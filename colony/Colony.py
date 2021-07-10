""" Method for simulating a Best of N colony
Michael Goodrich
February 2019
Joshua Richardson
Summer 2021 """

from ColonySimulation import *
from recording.RecordingPlayer import RecordingPlayer


def main():
    # default is (see Constants.py):
    # colony = ColonySimulation(NUM_AGENTS, SIM_DURATION, NUM_SITES, SHOULD_RECORD, SHOULD_DRAW, CONVERGENCE_FRACTION,
    #                           HUB_LOCATION, DEFAULT_SITE_SIZE, NUM_AGENTS, SITE_POSITIONS, SITE_QUALITIES, SITE_RADII,
    #                           SITE_NO_CLOSER_THAN)
    colony = ColonySimulation()
    # default is (see Constants.py):
    # colony = RecordingPlayer(SIM_DURATION, NUM_SITES, CONVERGENCE_FRACTION, HUB_LOCATION, DEFAULT_SITE_SIZE,
    #                          NUM_AGENTS, SITE_POSITIONS, SITE_QUALITIES, SITE_RADII,
    #                          SITE_NO_CLOSER_THAN, SITE_NO_FARTHER_THAN)
    colony = RecordingPlayer()
    try:
        # default is (see Constants.py):
        # colony.initializeAgentList(HOMOGENOUS_AGENTS, MIN_AGENT_SPEED, MAX_AGENT_SPEED, MIN_DECISIVENESS, MAX_DECISIVENESS,
        #                                    MIN_NAV_SKILLS, MAX_NAV_SKILLS, MIN_QUALITY_MISJUDGMENT, MAX_QUALITY_MISJUDGMENT)
        colony.initializeAgentList()
        colony.runSimulation()
        print("Success!")
    except InputError:
        pass
        

main()
