from colony.AbstractColonySimulation import AbstractColonySimulation
from recording.Recorder import Recorder


class RecordingPlayer(AbstractColonySimulation):

    def __init__(self, simulationDuration, numGoodSites, numSites):
        super().__init__(simulationDuration, numGoodSites, numSites)

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
            if self.world.siteList[i].quality != -1:
                self.world.siteList[i].color = (255 - self.world.siteList[i].quality, self.world.siteList[i].quality, 0)
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
