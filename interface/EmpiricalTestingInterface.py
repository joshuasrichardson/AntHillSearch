from Constants import *
from interface.LiveSimulation import LiveSimulation


class EmpiricalTestingInterface(LiveSimulation):
    """ A class to run the interface for ants finding their new home after the old one broke """

    def __init__(self, simulationDuration=SIM_DURATION, numHubs=NUM_HUBS, numSites=NUM_SITES, useRestAPI=True,
                 shouldRecord=SHOULD_RECORD, convergenceFraction=CONVERGENCE_FRACTION,
                 hubLocations=HUB_LOCATIONS, hubRadii=HUB_RADII, hubAgentCounts=HUB_AGENT_COUNTS,
                 sitePositions=SITE_POSITIONS, siteQualities=SITE_QUALITIES, siteRadii=SITE_RADII,
                 siteNoCloserThan=SITE_NO_CLOSER_THAN, siteNoFartherThan=SITE_NO_FARTHER_THAN, hubCanMove=False,
                 homogenousAgents=HOMOGENOUS_AGENTS, minSpeed=MIN_AGENT_SPEED,
                 maxSpeed=MAX_AGENT_SPEED, minDecisiveness=MIN_DECISIVENESS, maxDecisiveness=MAX_DECISIVENESS,
                 minNavSkills=MIN_NAV_SKILLS, maxNavSkills=MAX_NAV_SKILLS, minEstAccuracy=MIN_QUALITY_MISJUDGMENT,
                 maxEstAccuracy=MAX_QUALITY_MISJUDGMENT, maxSearchDist=MAX_SEARCH_DIST,
                 findSitesEasily=FIND_SITES_EASILY, commitSpeedFactor=COMMIT_SPEED_FACTOR, numPredators=NUM_PREDATORS,
                 useJson=True):
        super().__init__(simulationDuration, numHubs, numSites, useRestAPI, shouldRecord, convergenceFraction,
                         hubLocations, hubRadii, hubAgentCounts, sitePositions, siteQualities, siteRadii,
                         siteNoCloserThan, siteNoFartherThan, hubCanMove, homogenousAgents, minSpeed,
                         maxSpeed, minDecisiveness, maxDecisiveness, minNavSkills, maxNavSkills, minEstAccuracy,
                         maxEstAccuracy, maxSearchDist, findSitesEasily, commitSpeedFactor, numPredators=numPredators,
                         useJson=useJson)

    def recordDisplays(self):
        if self.shouldRecord:
            self.recorder.recordTime(self.timer.getRemainingTime())
            self.recorder.recordShouldDrawGraphs(True)
            self.recorder.recordExecutedCommands([])
            self.recorder.recordScreenBorder(None, None, None, None)

    def runNextRound(self):
        self.update(self.getAgentRectList())

    def getScreen(self):
        return None

    def getShouldDraw(self):
        return False

    def getDrawFarAgents(self):
        return False

    def getKnowSitePosAtStart(self):
        return False

    def getShouldDrawPaths(self):
        return False

    def getGraphs(self, numAgents, fontSize, largeFontSize):
        return None

    @staticmethod
    def drawBorder():
        pass
