from Constants import *
from display import Display
from interface.LiveSimulation import LiveSimulation
from model.World import World


class UserInterface(LiveSimulation):
    """ A class to run the interface for ants finding their new home after the old one broke """

    def __init__(self, simulationDuration=SIM_DURATION, numSites=NUM_SITES, useRestAPI=USE_REST_API,
                 shouldRecord=SHOULD_RECORD, convergenceFraction=CONVERGENCE_FRACTION,
                 hubLocation=HUB_LOCATION, hubRadius=SITE_RADIUS, hubAgentCount=NUM_AGENTS,
                 sitePositions=SITE_POSITIONS, siteQualities=SITE_QUALITIES, siteRadii=SITE_RADII,
                 siteNoCloserThan=SITE_NO_CLOSER_THAN, siteNoFartherThan=SITE_NO_FARTHER_THAN,
                 hubCanMove=False):
        super().__init__(simulationDuration, numSites, useRestAPI, shouldRecord, convergenceFraction,
                         hubLocation, hubRadius, hubAgentCount, sitePositions, siteQualities, siteRadii,
                         siteNoCloserThan, siteNoFartherThan, hubCanMove)

    def initializeWorld(self, numSites, hubLocation, hubRadius, hubAgentCount, sitePositions,
                        siteQualities, siteRadii, siteNoCloserThan, siteNoFartherThan, shouldDraw=True,
                        knowSitePosAtStart=False, hubCanMove=False):
        world = World(numSites, hubLocation, hubRadius, hubAgentCount, sitePositions,
                      siteQualities, siteRadii, siteNoCloserThan, siteNoFartherThan,
                      shouldDraw, hubCanMove)
        return world

    def initializeAgentList(self, numAgents=NUM_AGENTS, homogenousAgents=HOMOGENOUS_AGENTS, minSpeed=MIN_AGENT_SPEED,
                            maxSpeed=MAX_AGENT_SPEED, minDecisiveness=MIN_DECISIVENESS, maxDecisiveness=MAX_DECISIVENESS,
                            minNavSkills=MIN_NAV_SKILLS, maxNavSkills=MAX_NAV_SKILLS, minEstAccuracy=MIN_QUALITY_MISJUDGMENT,
                            maxEstAccuracy=MAX_QUALITY_MISJUDGMENT, maxSearchDist=MAX_SEARCH_DIST,
                            findSitesEasily=FIND_SITES_EASILY, commitSpeedFactor=COMMIT_SPEED_FACTOR,
                            drawFarAgents=False):
        super().initializeAgentList(numAgents, homogenousAgents, minSpeed, maxSpeed, minDecisiveness, maxDecisiveness,
                                    minNavSkills, maxNavSkills, minEstAccuracy, maxEstAccuracy, maxSearchDist,
                                    findSitesEasily, commitSpeedFactor, drawFarAgents)

    def getScreen(self):
        return Display.createScreen()

    def getShouldDraw(self):
        return True

    def getKnowSitePosAtStart(self):
        return False

    def getShouldDrawPaths(self):
        return False
