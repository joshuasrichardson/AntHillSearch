from Constants import *
from display import Display
from display.Graphs import SimulationGraphs
from interface.LiveSimulation import LiveSimulation


class EngineerInterface(LiveSimulation):
    """ A class to run the simulation for ants finding their new home after the old one broke """

    def __init__(self, simulationDuration=SIM_DURATION, numHubs=NUM_HUBS, numSites=NUM_SITES, useRestAPI=USE_REST_API,
                 shouldRecord=SHOULD_RECORD, convergenceFraction=CONVERGENCE_FRACTION,
                 hubLocations=HUB_LOCATIONS, hubRadii=HUB_RADII, hubAgentCounts=HUB_AGENT_COUNTS,
                 sitePositions=SITE_POSITIONS, siteQualities=SITE_QUALITIES, siteRadii=SITE_RADII,
                 siteNoCloserThan=SITE_NO_CLOSER_THAN, siteNoFartherThan=SITE_NO_FARTHER_THAN,
                 hubCanMove=True):
        Display.drawFarAgents = True
        super().__init__(simulationDuration, numHubs, numSites, useRestAPI, shouldRecord, convergenceFraction,
                         hubLocations, hubRadii, hubAgentCounts, sitePositions, siteQualities, siteRadii,
                         siteNoCloserThan, siteNoFartherThan, hubCanMove)

    def runNextRound(self):
        self.userControls.handleEvents()
        Display.screen.fill(SCREEN_COLOR)
        super().runNextRound()
        self.draw()

    def update(self, agentRectList):
        self.graphs.setRemainingTime(self.timer.getRemainingTime())
        super().update(agentRectList)

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
