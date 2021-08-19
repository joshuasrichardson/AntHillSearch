from Constants import *
from display import Display
from display.Graphs import SimulationGraphs
from interface.Simulation import Simulation
from ColonyExceptions import GameOver
from model.World import World


class RecordingPlayer(Simulation):
    """ Runs the colony interface for a previously recorded interface using the data stored in recording.txt """

    def __init__(self):
        self.hubAgentCounts = []
        super().__init__(shouldRecord=False)

    def initializeAgentList(self, hubAgentCounts=HUB_AGENT_COUNTS):
        super().initializeAgentList(self.hubAgentCounts)

    def initializeWorld(self, numHubs, numSites, hubLocations, hubRadii, hubAgentCounts, sitePositions, siteQualities,
                        siteRadii):
        self.recorder.read()
        self.initHubsAgentCounts()
        world = World(numHubs, numSites, hubLocations, hubRadii, self.hubAgentCounts, sitePositions,
                      siteQualities, siteRadii)

        return world

    def initHubsAgentCounts(self):
        assignmentIndices = self.recorder.getOriginalAssignments()
        for i in range(self.recorder.getNumHubs()):
            self.hubAgentCounts.append(0)
        for i in assignmentIndices:
            self.hubAgentCounts[i] = self.hubAgentCounts[i] + 1

    def runNextRound(self):
        self.userControls.handleEvents()
        Display.screen.fill(SCREEN_COLOR)
        super().runNextRound()
        self.draw()

    def update(self, agentRectList):
        self.graphs.setRemainingTime(self.timer.getRemainingTime())
        super().update(agentRectList)

    def setNextRound(self):
        if not self.recorder.setNextRound():
            raise GameOver("The recording has ended.")

    def updateSites(self):
        newPositions = []
        for i in range(0, self.recorder.getNumSites()):
            pos = self.recorder.getNextSitePosition()
            newPositions.append(pos)
            quality = self.recorder.getNextSiteQuality()
            rad = self.recorder.getNextSiteRadius()

            try:
                self.world.siteList[i].setPosition(pos)
                self.world.siteList[i].setQuality(quality)
                self.world.siteList[i].radius = rad
                self.world.siteList[i].setColor(quality)
                self.world.siteRectList[i] = self.world.siteList[i].getSiteRect()
            except IndexError:
                print("Creating site: " + str(pos))
                self.world.createSite(pos[0], pos[1], rad, quality, NUM_HUBS)
        for site in self.world.siteList:
            if not newPositions.__contains__(site.getPosition()):
                print("Removing site: " + str(site.getPosition()))
                self.world.removeSite(site)
        if len(self.world.siteList) > len(newPositions):
            self.world.removeSite(self.world.siteList[len(self.world.siteList) - 1])

    def updateAgent(self, agent, agentRectList):
        pos = self.recorder.getNextAgentPosition()
        agent.updatePosition(pos)
        angle = self.recorder.getNextAgentAngle()
        agent.setAngle(angle)

        agentRect = agent.getAgentRect()
        possibleNeighborList = agentRect.collidelistall(agentRectList)
        agentNeighbors = []
        for i in possibleNeighborList:
            agentNeighbors.append(self.world.agentList[i])
        agent.setState(self.recorder.getNextState(agent))
        agent.setPhase(self.recorder.getNextPhase())
        siteToAssign = agent.world.siteList[self.recorder.getNextAssignment()]
        agent.assignSite(siteToAssign)

    def getScreen(self):
        return Display.createScreen()

    def getShouldDraw(self):
        return True

    def getKnowSitePosAtStart(self):
        return True

    def getShouldDrawPaths(self):
        return True

    def getGraphs(self):
        return SimulationGraphs()
