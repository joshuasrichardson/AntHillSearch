""" Functions used to generate a new agent with randomized attributes that fall within the ranges specified in
 Config.py """
import random

from config import Config
from model.Agent import Agent


def getNewAgent(world, startingAssignment, startingPosition=None):
    if startingPosition is None:
        startingPosition = startingAssignment.getPosition()
    speed = initializeAttribute(Config.HOMOGENOUS_AGENTS, Config.MIN_AGENT_SPEED, Config.MAX_AGENT_SPEED)  # Speed the agent moves on the screen
    decisiveness = initializeAttribute(Config.HOMOGENOUS_AGENTS, Config.MIN_DECISIVENESS, Config.MAX_DECISIVENESS)  # Influences how quickly an agent can assess
    navSkills = initializeAttribute(Config.HOMOGENOUS_AGENTS, Config.MIN_NAV_SKILLS, Config.MAX_NAV_SKILLS)  # Influences how likely an agent is to get lost
    estAccuracy = initializeAttribute(Config.HOMOGENOUS_AGENTS, Config.MIN_QUALITY_MISJUDGMENT, Config.MAX_QUALITY_MISJUDGMENT)  # How far off an agent's estimate of the quality of a site will be on average.
    return Agent(world, startingAssignment, startingPosition, speed, decisiveness, navSkills, estAccuracy)


def initializeAttribute(homogenousAgents, minimum, maximum):
    """ Sets all the attribute value to maximum if agents are all the same or a random number in the
    range if agents are different """
    if homogenousAgents:
        return maximum
    else:
        return random.uniform(minimum, maximum)
