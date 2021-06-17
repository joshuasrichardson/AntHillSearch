""" Method for simulating a Best of N colony
Michael Goodrich
February 2019 """

from ColonySimulation import *


def main():
    colony = ColonySimulation(NUM_AGENTS, SIM_DURATION, NUM_GOOD, NUM_SITES)
    
    try:
        colony.runSimulation()
        print("Success!")
    except InputError:
        pass
        

main()
