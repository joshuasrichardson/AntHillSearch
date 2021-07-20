from Constants import *
from colony.AbstractColonySimulation import AbstractColonySimulation
from colony.ColonyExceptions import GameOver
from colony.World import World


class RecordingPlayer(AbstractColonySimulation):
    """ Runs the colony simulation for a previously recorded simulation using the data stored in recording.txt """

    def __init__(self):
        # , simulationDuration=SIM_DURATION, numSites=NUM_SITES, convergenceFraction=CONVERGENCE_FRACTION,
        #          hubLocation=HUB_LOCATION, hubRadius=SITE_RADIUS, hubAgentCount=NUM_AGENTS,
        #          sitePositions=SITE_POSITIONS, siteQualities=SITE_QUALITIES, siteRadii=SITE_RADII,
        #          siteNoCloserThan=SITE_NO_CLOSER_THAN, siteNoFartherThan=SITE_NO_FARTHER_THAN
        super().__init__(shouldReport=False, shouldRecord=False, shouldDraw=True)

    def initializeWorld(self, numSites, hubLocation, hubRadius, hubAgentCount, sitePositions, siteQualities,
                        siteRadii, siteNoCloserThan, siteNoFartherThan, shouldDraw=True):
        self.recorder.read()

        return World(numSites, self.screen, hubLocation, hubRadius, hubAgentCount, sitePositions,
                     siteQualities, siteRadii, siteNoCloserThan, siteNoFartherThan, shouldDraw)

    def setNextRound(self):
        if not self.recorder.setNextRound():
            raise GameOver("The recording has ended.")

    def updateSites(self):
        newPositions = []
        newQualities = []
        for i in range(0, self.recorder.getNumSites()):
            pos = self.recorder.getNextSitePosition()
            newPositions.append(pos)
            quality = self.recorder.getNextSiteQuality()
            newQualities.append(quality)
            rad = self.recorder.getNextSiteRadius()

            try:
                self.world.siteList[i].setPosition(pos)
                self.world.siteList[i].quality = quality
                self.world.siteList[i].radius = rad
                self.world.siteList[i].setColor(quality)
                self.world.siteRectList[i] = self.world.siteList[i].getSiteRect()
            except IndexError:
                print("Creating site: " + str(pos))
                self.world.createSite(pos[0], pos[1], rad, quality)
        for site in self.world.siteList:
            if not newPositions.__contains__(site.getPosition()):
                print("Removing site: " + str(site.getPosition()))
                self.world.removeSite(site)

    def updateAgent(self, agent, agentRectList):
        pos = self.recorder.getNextAgentPosition()
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
        siteToAssign = agent.world.siteList[self.recorder.getNextAssignment()]
        agent.assignSite(siteToAssign)
