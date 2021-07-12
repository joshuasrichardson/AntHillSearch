from Constants import *
from colony.AbstractColonySimulation import AbstractColonySimulation
from colony.World import World
from recording.Recorder import Recorder


class RecordingPlayer(AbstractColonySimulation):
    """ Runs the colony simulation for a previously recorded simulation using the data stored in recording.txt """

    # TODO: Get the hub to stop showing up twice in recordings where sites were deleted.

    def __init__(self, simulationDuration=SIM_DURATION, numSites=NUM_SITES, convergenceFraction=CONVERGENCE_FRACTION,
                 hubLocation=HUB_LOCATION, hubRadius=DEFAULT_SITE_SIZE, hubAgentCount=NUM_AGENTS,
                 sitePositions=SITE_POSITIONS, siteQualities=SITE_QUALITIES, siteRadii=SITE_RADII,
                 siteNoCloserThan=SITE_NO_CLOSER_THAN, siteNoFartherThan=SITE_NO_FARTHER_THAN):
        super().__init__(simulationDuration, numSites, False, True, convergenceFraction, hubLocation, hubRadius,
                         hubAgentCount, sitePositions, siteQualities, siteRadii, siteNoCloserThan, siteNoFartherThan)

    def initializeWorldAndRecorder(self, numSites, hubLocation, hubRadius, hubAgentCount, sitePositions, siteQualities,
                                   siteRadii, siteNoCloserThan, siteNoFartherThan):
        recorder = Recorder(None, None)
        recorder.read()

        # numAgents = recorder.numAgents

        world = World(numSites, self.screen, hubLocation, hubRadius, hubAgentCount, sitePositions,
                      siteQualities, siteRadii, siteNoCloserThan, siteNoFartherThan)

        for i in range(0, len(recorder.sites)):
            world.siteList[i].pos = recorder.sites[i].pos
            world.siteList[i].radius = recorder.sites[i].radius
            world.siteList[i].quality = recorder.sites[i].quality
            world.siteList[i].setPosition(recorder.sites[i].pos)
            world.siteList[i].setColor(world.siteList[i].quality)

        return world, recorder

    def updateAgent(self, agent, agentRectList):
        pos = self.recorder.getNextPosition()
        if pos == -1:
            return False
        agent.updatePosition(pos)

        agentRect = agent.getAgentRect()
        possibleNeighborList = agentRect.collidelistall(agentRectList)
        agentNeighbors = []
        for i in possibleNeighborList:
            agentNeighbors.append(self.world.agentList[i])
        agent.state.state = self.recorder.getNextState()
        agent.state.color = agent.getStateColor(agent.state.state)
        agent.phase = self.recorder.getNextPhase()
        agent.phaseColor = agent.getPhaseColor(agent.phase)
        siteToAssign = agent.siteList[self.recorder.getNextAssignment()]
        agent.assignSite(siteToAssign)
