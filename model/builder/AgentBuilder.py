import random
from model.Agent import Agent
from model.builder import AgentSettings


def getNewAgent(world, startingAssignment, startingPosition=None):
    if startingPosition is None:
        startingPosition = startingAssignment.getPosition()
    speed = initializeAttribute(AgentSettings.homogenousAgents, AgentSettings.minSpeed, AgentSettings.maxSpeed)  # Speed the agent moves on the screen
    decisiveness = initializeAttribute(AgentSettings.homogenousAgents, AgentSettings.minDecisiveness, AgentSettings.maxDecisiveness)  # Influences how quickly an agent can assess
    navSkills = initializeAttribute(AgentSettings.homogenousAgents, AgentSettings.minNavSkills, AgentSettings.maxNavSkills)  # Influences how likely an agent is to get lost
    estAccuracy = initializeAttribute(AgentSettings.homogenousAgents, AgentSettings.minEstAccuracy, AgentSettings.maxEstAccuracy)  # How far off an agent's estimate of the quality of a site will be on average.
    return Agent(world, startingAssignment, startingPosition, speed, decisiveness, navSkills, estAccuracy)


def initializeAttribute(homogenousAgents, minimum, maximum):
    """ Sets all the attribute value to maximum if agents are all the same or a random number in the
    range if agents are different """
    if homogenousAgents:
        return maximum
    else:
        return random.uniform(minimum, maximum)
