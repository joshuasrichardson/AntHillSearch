from Constants import *
from colony.ColonySimulation import ColonySimulation


class EmpiricalTestingInterface(ColonySimulation):
    """ A class to run the simulation for ants finding their new home after the old one broke """

    def __init__(self, simulationDuration=SIM_DURATION, numSites=NUM_SITES, useRestAPI=True,
                 shouldRecord=SHOULD_RECORD, shouldDraw=False, convergenceFraction=CONVERGENCE_FRACTION,
                 hubLocation=HUB_LOCATION, hubRadius=SITE_RADIUS, hubAgentCount=NUM_AGENTS,
                 sitePositions=SITE_POSITIONS, siteQualities=SITE_QUALITIES, siteRadii=SITE_RADII,
                 siteNoCloserThan=SITE_NO_CLOSER_THAN, siteNoFartherThan=SITE_NO_FARTHER_THAN,
                 knowSitePosAtStart=False, canSelectAnywhere=False, hubCanMove=False):
        super().__init__(simulationDuration, numSites, useRestAPI, shouldRecord, shouldDraw, convergenceFraction,
                         hubLocation, hubRadius, hubAgentCount, sitePositions, siteQualities, siteRadii,
                         siteNoCloserThan, siteNoFartherThan, knowSitePosAtStart, canSelectAnywhere, hubCanMove)
