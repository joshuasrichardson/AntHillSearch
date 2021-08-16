# import threading

# import psutil

from Constants import *
from interface.LiveSimulation import LiveSimulation


class EmpiricalTestingInterface(LiveSimulation):
    """ A class to run the interface for ants finding their new home after the old one broke """

    def __init__(self, simulationDuration=SIM_DURATION, numHubs=NUM_HUBS, numSites=NUM_SITES, useRestAPI=True,
                 shouldRecord=SHOULD_RECORD, convergenceFraction=CONVERGENCE_FRACTION,
                 hubLocations=HUB_LOCATIONS, hubRadii=HUB_RADII, hubAgentCounts=HUB_AGENT_COUNTS,
                 sitePositions=SITE_POSITIONS, siteQualities=SITE_QUALITIES, siteRadii=SITE_RADII,
                 siteNoCloserThan=SITE_NO_CLOSER_THAN, siteNoFartherThan=SITE_NO_FARTHER_THAN, hubCanMove=False):
        super().__init__(simulationDuration, numHubs, numSites, useRestAPI, shouldRecord, convergenceFraction,
                         hubLocations, hubRadii, hubAgentCounts, sitePositions, siteQualities, siteRadii,
                         siteNoCloserThan, siteNoFartherThan, hubCanMove)

    def getScreen(self):
        return None

    def getShouldDraw(self):
        return False

    def getKnowSitePosAtStart(self):
        return False

    def getShouldDrawPaths(self):
        return False

    def getGraphs(self):
        return None

    # def runSimulation(self):
    #     print("1")
    #
    #     from net import RestAPI
    #     thread = threading.Thread(target=RestAPI.app.run)
    #     thread.start()
    #     print("2")
    #     super().runSimulation()
    #     print("3")
    #     try:
    #         from psutil import process_iter
    #         from signal import SIGTERM
    #
    #         for proc in process_iter():
    #             for conns in proc.connections(kind='inet'):
    #                 if conns.laddr.port == 5000:
    #                     proc.send_signal(SIGTERM) # or SIGKILL
    #     except (PermissionError, psutil.AccessDenied):
    #         pass
    #     print("4")

