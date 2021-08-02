from Constants import *
from colony.simulation.ColonySimulation import ColonySimulation
from colony.World import World


class UserInterface(ColonySimulation):
    """ A class to run the simulation for ants finding their new home after the old one broke """

    def __init__(self, simulationDuration=SIM_DURATION, numSites=NUM_SITES, useRestAPI=USE_REST_API,
                 shouldRecord=SHOULD_RECORD, shouldDraw=True, convergenceFraction=CONVERGENCE_FRACTION,
                 hubLocation=HUB_LOCATION, hubRadius=SITE_RADIUS, hubAgentCount=NUM_AGENTS,
                 sitePositions=SITE_POSITIONS, siteQualities=SITE_QUALITIES, siteRadii=SITE_RADII,
                 siteNoCloserThan=SITE_NO_CLOSER_THAN, siteNoFartherThan=SITE_NO_FARTHER_THAN,
                 knowSitePosAtStart=False, canSelectAnywhere=False, hubCanMove=False):
        super().__init__(simulationDuration, numSites, useRestAPI, shouldRecord, shouldDraw, convergenceFraction,
                         hubLocation, hubRadius, hubAgentCount, sitePositions, siteQualities, siteRadii,
                         siteNoCloserThan, siteNoFartherThan, knowSitePosAtStart, canSelectAnywhere, hubCanMove)

    def initializeWorld(self, numSites, hubLocation, hubRadius, hubAgentCount, sitePositions,
                        siteQualities, siteRadii, siteNoCloserThan, siteNoFartherThan, shouldDraw=True,
                        knowSitePosAtStart=False, hubCanMove=False, shouldDrawPaths=False):
        world = World(numSites, self.screen, hubLocation, hubRadius, hubAgentCount, sitePositions,
                      siteQualities, siteRadii, siteNoCloserThan, siteNoFartherThan, shouldDraw, False,
                      True, False, shouldDrawPaths)
        return world

    def initializeAgentList(self, numAgents=NUM_AGENTS, homogenousAgents=HOMOGENOUS_AGENTS, minSpeed=MIN_AGENT_SPEED,
                            maxSpeed=MAX_AGENT_SPEED, minDecisiveness=MIN_DECISIVENESS, maxDecisiveness=MAX_DECISIVENESS,
                            minNavSkills=MIN_NAV_SKILLS, maxNavSkills=MAX_NAV_SKILLS, minEstAccuracy=MIN_QUALITY_MISJUDGMENT,
                            maxEstAccuracy=MAX_QUALITY_MISJUDGMENT, maxSearchDist=MAX_SEARCH_DIST,
                            findSitesEasily=FIND_SITES_EASILY, commitSpeedFactor=COMMIT_SPEED_FACTOR,
                            drawFarAgents=False, showAgentColors=False):
        super().initializeAgentList(numAgents, homogenousAgents, minSpeed, maxSpeed, minDecisiveness, maxDecisiveness,
                                    minNavSkills, maxNavSkills, minEstAccuracy, maxEstAccuracy, maxSearchDist,
                                    findSitesEasily, commitSpeedFactor, drawFarAgents, showAgentColors)
