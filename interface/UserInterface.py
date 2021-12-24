from Constants import *
from display import Display
from display.Graphs import SimulationGraphs
from interface.LiveSimulation import LiveSimulation
from user.UIControls import UIControls


class UserInterface(LiveSimulation):
    """ A class to run the interface for ants finding their new home after the old one broke """

    def __init__(self, simulationDuration=SIM_DURATION, numHubs=NUM_HUBS, numSites=NUM_SITES, useRestAPI=USE_REST_API,
                 shouldRecord=SHOULD_RECORD, convergenceFraction=CONVERGENCE_FRACTION,
                 hubLocations=HUB_LOCATIONS, hubRadii=HUB_RADII, hubAgentCounts=HUB_AGENT_COUNTS,
                 sitePositions=SITE_POSITIONS, siteQualities=SITE_QUALITIES, siteRadii=SITE_RADII,
                 siteNoCloserThan=SITE_NO_CLOSER_THAN, siteNoFartherThan=SITE_NO_FARTHER_THAN,
                 hubCanMove=False, homogenousAgents=HOMOGENOUS_AGENTS, minSpeed=MIN_AGENT_SPEED,
                 maxSpeed=MAX_AGENT_SPEED, minDecisiveness=MIN_DECISIVENESS, maxDecisiveness=MAX_DECISIVENESS,
                 minNavSkills=MIN_NAV_SKILLS, maxNavSkills=MAX_NAV_SKILLS, minEstAccuracy=MIN_QUALITY_MISJUDGMENT,
                 maxEstAccuracy=MAX_QUALITY_MISJUDGMENT, maxSearchDist=MAX_SEARCH_DIST,
                 findSitesEasily=FIND_SITES_EASILY, commitSpeedFactor=COMMIT_SPEED_FACTOR, useJson=True):
        super().__init__(simulationDuration, numHubs, numSites, useRestAPI, shouldRecord, convergenceFraction,
                         hubLocations, hubRadii, hubAgentCounts, sitePositions, siteQualities, siteRadii,
                         siteNoCloserThan, siteNoFartherThan, hubCanMove, homogenousAgents, minSpeed,
                         maxSpeed, minDecisiveness, maxDecisiveness, minNavSkills, maxNavSkills, minEstAccuracy,
                         maxEstAccuracy, maxSearchDist, findSitesEasily, commitSpeedFactor, useJson=useJson)

    def runNextRound(self):
        self.userControls.handleEvents()
        Display.screen.fill(SCREEN_COLOR)
        self.draw()
        super().runNextRound()

    def update(self, agentRectList):
        self.graphs.setRemainingTime(self.timer.getRemainingTime())
        super().update(agentRectList)
        self.userControls.moveScreen()

    def getScreen(self):
        return Display.createScreen()

    def getShouldDraw(self):
        return True

    def getDrawFarAgents(self):
        return False

    def getKnowSitePosAtStart(self):
        return False

    def getShouldDrawPaths(self):
        return False

    def getGraphs(self, numAgents, fontSize, largeFontSize):
        return SimulationGraphs(numAgents, fontSize, largeFontSize, UI_CONTROL_OPTIONS)

    def getControls(self):
        return UIControls(self.timer, self.world.agentList, self.world, self.graphs)
