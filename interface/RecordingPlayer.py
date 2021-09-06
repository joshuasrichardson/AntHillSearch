import time

from Constants import *
from display import Display
from display.Graphs import SimulationGraphs
from interface.Simulation import Simulation
from ColonyExceptions import GameOver
from model.World import World
from user.RecordingControls import RecordingControls


class RecordingPlayer(Simulation):
    """ Runs the colony interface for a previously recorded interface using the data stored in recording.txt """

    def __init__(self):
        self.hubAgentCounts = []
        self.delay = 0
        super().__init__(shouldRecord=False)

    def initializeAgentList(self):
        self.world.initialHubAgentCounts = self.hubAgentCounts
        super().initializeAgentList()

    def initializeWorld(self, numHubs, numSites, hubLocations, hubRadii, hubAgentCounts, sitePositions, siteQualities,
                        siteRadii):
        self.recorder.read()
        addAfter = self.initHubsAgentCounts()
        world = World(self.recorder.getNumHubs(), self.recorder.getNumSites(), hubLocations, hubRadii, self.hubAgentCounts, sitePositions,
                      siteQualities, siteRadii)
        self.addAddedAgents(world, addAfter)
        self.timer.simulationDuration = self.recorder.getNextTime()

        return world

    def initHubsAgentCounts(self):
        addAfter = []
        assignmentIndices = self.recorder.getOriginalAssignments()
        for i in range(self.recorder.getNumHubs()):
            self.hubAgentCounts.append(0)
        for i in assignmentIndices:
            if i < self.recorder.getNumHubs():
                self.hubAgentCounts[i] += 1
            else:
                addAfter.append(i)
        return addAfter

    def addAddedAgents(self, world, assignmentIndices):
        for i, site in enumerate(world.siteList):
            try:
                site.setPosition(self.recorder.data[0]['sitePositions'][i])
            except IndexError:
                world.removeSite(site)
        for i in assignmentIndices:
            hub = world.getClosestHub(world.siteList[i].getPosition())
            hubIndex = world.hubs.index(hub)
            hub.incrementCount(hubIndex)
            self.hubAgentCounts[hubIndex] += 1

    def runNextRound(self):
        self.userControls.handleEvents()
        Display.screen.fill(SCREEN_COLOR)
        super().runNextRound()
        self.draw()

    def update(self, agentRectList):
        self.slowDownOrSpeedUp()
        self.graphs.setRemainingTime(self.recorder.getNextTime())
        self.graphs.shouldDrawGraphs = self.recorder.getNextShouldDrawGraphs()
        self.graphs.executedCommands = self.recorder.getNextExecutedCommands()
        self.graphs.scrollIndex = len(self.recorder.executedCommands) - 1
        self.graphs.screenBorder = self.recorder.getNextScreenBorder()
        Display.addToDrawLast(self.graphs.drawScreenBorder)

        super().update(agentRectList)
        self.userControls.moveScreen()

    def slowDownOrSpeedUp(self):
        if self.delay > 0:  # Slow down
            time.sleep(self.delay)
        elif self.delay < 0:  # Speed up
            d = self.delay
            while d < 0:
                self.setNextRound()
                d += 0.025

    def setNextRound(self):
        if not self.recorder.setNextRound():
            raise GameOver("The recording has ended.")

    def checkIfSimulationEnded(self):
        pass

    def updateSites(self):
        newPositions = []
        for i in range(0, self.recorder.getNumSites()):
            pos = self.recorder.getNextSitePosition()
            newPositions.append(pos)
            quality = self.recorder.getNextSiteQuality()
            rad = self.recorder.getNextSiteRadius()
            marker = self.recorder.getNextSiteMarker()

            try:
                self.world.siteList[i].setPosition(pos)
                self.world.siteList[i].setQuality(quality)
                self.world.siteList[i].radius = rad
                self.world.siteList[i].setColor(quality)
                self.world.siteRectList[i] = self.world.siteList[i].getSiteRect()
                self.userControls.setSiteCommand(self.world.siteList[i], marker)
            except IndexError:
                print("Creating site: " + str(pos))
                self.world.createSite(pos[0], pos[1], rad, quality, len(self.world.getHubs()))
        for site in self.world.siteList:
            if not newPositions.__contains__(site.getPosition()):
                print("Removing site: " + str(site.getPosition()))
                self.world.removeSite(site)
        if len(self.world.siteList) > len(newPositions):
            self.world.removeSite(self.world.siteList[len(self.world.siteList) - 1])

    def updateAgents(self, agentRectList):
        self.deleteAgents(self.recorder.getNextAgentsToDelete(), agentRectList)
        super().updateAgents(agentRectList)

    def deleteAgents(self, agentIndexes, agentRectList):
        for agentIndex in reversed(agentIndexes):
            agentRectList.pop(agentIndex)
            self.world.removeAgent(self.world.agentList[agentIndex])

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

    def changeDelay(self, seconds):
        self.delay += seconds

    def getRemainingTime(self):
        return self.timer.simulationDuration - self.recorder.getNextTime()

    def getScreen(self):
        return Display.createScreen()

    def getShouldDraw(self):
        return True

    def getDrawFarAgents(self):
        return True

    def getKnowSitePosAtStart(self):
        return True

    def getShouldDrawPaths(self):
        return True

    def getGraphs(self, numAgents):
        return SimulationGraphs(numAgents)

    def calcNumAgents(self, hubAgentCounts):
        return self.recorder.getNumAgents()

    def getControls(self):
        return RecordingControls(self.timer, self.world.agentList, self.world, self.graphs, self.changeDelay)
