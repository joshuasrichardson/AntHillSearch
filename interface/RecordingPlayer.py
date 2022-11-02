import json
import time

from config import Config
from model.Timer import Timer
from Constants import *
from display.simulation import FogDisplay
from interface.Simulation import Simulation
from ColonyExceptions import GameOver
from model.World import World
from user.RecordingControls import RecordingControls


class RecordingPlayer(Simulation):
    """ Runs the colony simulation for a previously recorded simulation using the data stored in recording.txt """

    def __init__(self, selectedReplay):
        self.hubAgentCounts = []
        self.delay = 0
        self.selectedReplay = selectedReplay
        with open(CONFIG_FILE_NAME, 'r') as currentSettings:
            self.originalConfig = json.load(currentSettings)
        super().__init__()
        Config.SHOULD_RECORD = False
        self.realTimer = Timer(self.timeOut)

    def initializeAgentList(self):
        self.world.initialHubAgentCounts = self.hubAgentCounts
        for i in range(len(self.world.hubs)):
            self.world.hubs[i].agentCount = self.hubAgentCounts[i]
        super().initializeAgentList()

    def initializeWorld(self):
        self.recorder.read(self.selectedReplay)
        addAfter = self.initHubsAgentCounts()
        self.world = World(self.recorder.getNumHubs(), self.recorder.getNumSites(), Config.HUB_POSITIONS,
                           Config.HUB_RADII, Config.HUB_AGENT_COUNTS, Config.SITE_POSITIONS,
                           Config.SITE_QUALITIES, Config.SITE_RADII, Config.SITE_RADIUS,
                           numPredators=self.recorder.getNumPredators(), numLadybugs=self.recorder.getNumLadybugs())
        self.addAddedAgents(self.world, addAfter)
        self.initializeAgentList()
        FogDisplay.clearExplorableArea(self.world)

        return self.world

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

    def initChosenHomes(self):
        chosenHomes = []
        for i in range(self.recorder.getNumHubs()):
            chosenHomes.append(self.world.siteList[0])
        return chosenHomes

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

    def runSimulation(self):
        self.realTimer.start()
        results = super().runSimulation()
        return results

    def printNumRounds(self):
        roundCounts = self.recorder.getNumRounds()
        for i, roundCount in enumerate(roundCounts):
            print(f"Colony {i + 1} took {roundCount} rounds to finish.")
        return roundCounts

    def stopTimer(self):
        super().stopTimer()
        realTime = self.realTimer.getRemainingTime()
        self.realTimer.cancel()
        print(f"Real simulation time: {Config.SIM_DURATION - realTime}")

    def update(self, agentRectList):
        self.slowDownOrSpeedUp()
        self.simDisp.commandHistBox.executedCommands.clear()
        for command in self.recorder.getNextExecutedCommands():
            self.simDisp.commandHistBox.addMessage(command)
        self.simDisp.screenBorder = self.recorder.getNextScreenBorder()

        super().update(agentRectList)

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
                self.world.siteList[i].wasFound = True
                self.world.siteList[i].setPosition(pos)
                self.world.siteList[i].setQuality(quality)
                self.world.siteList[i].setRadius(rad)
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
        agent.setState(self.recorder.getNextState(agent))
        agent.setPhase(self.recorder.getNextPhase())
        pos = self.recorder.getNextAgentPosition()
        agent.setPosition(pos[0], pos[1])
        angle = self.recorder.getNextAgentAngle()
        agent.setAngle(angle)
        try:
            siteToAssign = agent.world.siteList[self.recorder.getNextAssignment()]
            agent.assignSite(siteToAssign)
        except TypeError:
            agent.die()

    def updatePredator(self, predator, agentRectList):
        pos = self.recorder.getNextPredatorPosition()
        predator.setPosition(pos[0], pos[1])
        predator.setAngle(self.recorder.getNextPredatorAngle())

    def updateLadybug(self, ladybug, agentRectList):
        pos = self.recorder.getNextLadybugPosition()
        ladybug.setPosition(pos[0], pos[1])
        ladybug.setAngle(self.recorder.getNextLadybugAngle())

    def updateObstacle(self, obstacle, agentRectList):
        pass

    def changeDelay(self, seconds):
        self.delay += seconds

    def printTimeResults(self):
        times = self.recorder.readResults()[SIM_TIMES_NAME]
        for i, duration in enumerate(times):
            print(f"Colony {i + 1} took {duration} seconds to finish.")
        return times

    def getNumDeadAgents(self):
        return self.recorder.readResults()[NUM_DEAD_NAME]

    def getControls(self):
        return RecordingControls(self.world.agentList, self.world, self.simDisp, self.changeDelay)

    def applyConfiguration(self, numAgents=None, numSites=None, sitePositions=None, siteQualities=None):
        super().applyConfiguration()
        Config.INTERFACE_NAME = "Recording"
        Config.DRAW_ESTIMATES = False
        Config.SHOULD_RECORD = False
        Config.DRAW_FAR_AGENTS = True

    def finish(self):
        results = super().finish()
        # Restore the original configuration that was overwritten when the recording was read.
        with open(CONFIG_FILE_NAME, 'w') as configFile:
            json.dump(self.originalConfig, configFile)
        return results
