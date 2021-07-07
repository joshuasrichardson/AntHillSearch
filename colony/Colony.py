""" Method for simulating a Best of N colony
Michael Goodrich
February 2019
Joshua Richardson
Summer 2021 """

from ColonySimulation import *
from recording.RecordingPlayer import RecordingPlayer


def main():
    colony = ColonySimulation(NUM_AGENTS, SIM_DURATION, NUM_GOOD, NUM_SITES)
    # RecordingPlayer(SIM_DURATION, NUM_GOOD, NUM_SITES)  #
    try:
        colony.runSimulation()
        print("Success!")
    except InputError:
        pass
        

main()
