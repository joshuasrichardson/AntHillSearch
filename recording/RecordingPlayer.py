from colony.AbstractColonySimulation import AbstractColonySimulation
from recording.Recorder import Recorder


class RecordingPlayer(AbstractColonySimulation):
    """ Runs the colony simulation for a previously recorded simulation using the data stored in recording.txt """

    def __init__(self, simulationDuration, numSites):
        super().__init__(simulationDuration, numSites)

    def getRecorder(self):
        self.recorder = Recorder(None, None)
        self.recorder.read()
        return self.recorder

    def getNumAgents(self):
        self.numAgents = self.recorder.numAgents
        for i in range(0, len(self.recorder.sites)):
            self.world.siteList[i].pos = self.recorder.sites[i].pos
            self.world.siteList[i].radius = self.recorder.sites[i].radius
            self.world.siteList[i].quality = self.recorder.sites[i].quality
            self.world.siteList[i].setPosition(self.recorder.sites[i].pos)
            self.world.siteList[i].setColor(self.world.siteList[i].quality)
        return self.numAgents

    def updateAgent(self, agent, agentRectList):
        pos = self.recorder.getNextPosition()
        if pos == -1:
            return False
        agent.updatePosition(pos)

        agentRect = agent.getAgentRect()
        possibleNeighborList = agentRect.collidelistall(agentRectList)
        agentNeighbors = []
        for i in possibleNeighborList:
            agentNeighbors.append(self.agentList[i])
        agent.state.state = self.recorder.getNextState()
        agent.state.color = agent.getStateColor(agent.state.state)
        agent.phase = self.recorder.getNextPhase()
        agent.phaseColor = agent.getPhaseColor(agent.phase)
        agent.tryAssigningSite()
