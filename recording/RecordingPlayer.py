from Constants import *
from colony.simulation.AbstractColonySimulation import AbstractColonySimulation
from colony.ColonyExceptions import GameOver
from colony.World import World


class RecordingPlayer(AbstractColonySimulation):
    """ Runs the colony simulation for a previously recorded simulation using the data stored in recording.txt """

    def __init__(self):
        super().__init__(useRestAPI=False, shouldRecord=False, shouldDraw=True, knowSitePosAtStart=True)

    def initializeAgentList(self, numAgents=NUM_AGENTS, homogenousAgents=HOMOGENOUS_AGENTS, minSpeed=MIN_AGENT_SPEED,
                            maxSpeed=MAX_AGENT_SPEED, minDecisiveness=MIN_DECISIVENESS, maxDecisiveness=MAX_DECISIVENESS,
                            minNavSkills=MIN_NAV_SKILLS, maxNavSkills=MAX_NAV_SKILLS, minEstAccuracy=MIN_QUALITY_MISJUDGMENT,
                            maxEstAccuracy=MAX_QUALITY_MISJUDGMENT, maxSearchDist=MAX_SEARCH_DIST,
                            findSitesEasily=FIND_SITES_EASILY, commitSpeedFactor=COMMIT_SPEED_FACTOR,
                            drawFarAgents=DRAW_FAR_AGENTS, showAgentColors=SHOW_AGENT_COLORS):
        numAgents = self.recorder.getNumAgents()
        super().initializeAgentList(numAgents=numAgents)

    def initializeWorld(self, numSites, hubLocation, hubRadius, hubAgentCount, sitePositions, siteQualities,
                        siteRadii, siteNoCloserThan, siteNoFartherThan, shouldDraw=True, knowSitePosAtStart=True,
                        hubCanMove=True):
        self.recorder.read()

        return World(numSites, self.screen, hubLocation, hubRadius, self.recorder.getNumAgents(), sitePositions,
                     siteQualities, siteRadii, siteNoCloserThan, siteNoFartherThan, shouldDraw, knowSitePosAtStart, False)

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
                self.world.siteList[i].quality = quality
                self.world.siteList[i].radius = rad
                self.world.siteList[i].setColor(quality)
                self.world.siteRectList[i] = self.world.siteList[i].getSiteRect()
            except IndexError:
                print("Creating site: " + str(pos))
                self.world.createSite(pos[0], pos[1], rad, quality, self.shouldDraw)
        for site in self.world.siteList:
            if not newPositions.__contains__(site.getPosition()):
                print("Removing site: " + str(site.getPosition()))
                self.world.removeSite(site)
        if len(self.world.siteList) > len(newPositions):
            self.world.removeSite(self.world.siteList[len(self.world.siteList) - 1])

    def updateAgent(self, agent, agentRectList):
        pos = self.recorder.getNextAgentPosition()
        agent.updatePosition(pos)

        agentRect = agent.getAgentRect()
        possibleNeighborList = agentRect.collidelistall(agentRectList)
        agentNeighbors = []
        for i in possibleNeighborList:
            agentNeighbors.append(self.world.agentList[i])
        agent.setState(self.recorder.getNextState(agent))
        agent.setPhase(self.recorder.getNextPhase())
        siteToAssign = agent.world.siteList[self.recorder.getNextAssignment()]
        agent.assignSite(siteToAssign)
