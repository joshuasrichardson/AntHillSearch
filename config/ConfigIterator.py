import json
import random

import numpy as np

import Utils
from Constants import CONFIG_FILE_NAME


class Setting:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        print(f"{self.key}: {self.value}")
        return f"{self.key}: {self.value}"


def generatePositions(numSites, distance):
    angle = random.uniform(0, np.pi)
    angleDiff = (np.pi * 2) / numSites
    positions = []

    for i in range(numSites):
        positions.append(Utils.getNextPosition([0, 0], distance, angle))
        angle += angleDiff

    return positions


def setKeysValues(settings):
    with open(CONFIG_FILE_NAME, 'r') as file:
        data = json.load(file)
    for setting in settings:
        data[setting.key] = setting.value
    with open(CONFIG_FILE_NAME, 'w') as file:
        json.dump(data, file)
    Utils.copyJsonToConfig()


class ConfigIterator:
    def __init__(self, simsPerSetting, numAgentss, numSitess, distances, *qualitiess):
        self.simsPerSetting = simsPerSetting
        self.numAgentss = numAgentss
        self.numSitess = numSitess
        self.distances = distances
        self.qualitiess = qualitiess
        self.maxNumAgentsIndex = len(numAgentss)
        self.maxNumSitesIndex = len(numSitess)
        self.maxDistanceIndex = len(distances)
        self.maxQualitiesIndex = len(qualitiess[0])
        if self.maxNumSitesIndex != len(qualitiess):
            raise Exception(f"Length of qualitiess ({len(qualitiess)}) must match the length of the number of sites ({self.maxNumSitesIndex})")
        for i, numSites in enumerate(self.numSitess):
            if numSites != len(qualitiess[i][0]):
                raise Exception(f"Length of qualities ({len(qualitiess[i][0])}) must match the number of sites ({numSites})")

    def __iter__(self):
        self.simIndex = 0
        self.numAgentsIndex = 0
        self.numSitesIndex = 0
        self.distanceIndex = 0
        self.qualitiesIndex = -1
        return self

    def __next__(self):
        self.qualitiesIndex += 1
        if self.qualitiesIndex == self.maxQualitiesIndex:
            self.qualitiesIndex = 0
            self.distanceIndex += 1
            if self.distanceIndex == self.maxDistanceIndex:
                self.distanceIndex = 0
                self.numSitesIndex += 1
                if self.numSitesIndex == self.maxNumSitesIndex:
                    self.numSitesIndex = 0
                    self.numAgentsIndex += 1
                    if self.numAgentsIndex == self.maxNumAgentsIndex:
                        self.numAgentsIndex = 0
                        self.simIndex += 1
                        if self.simIndex == self.simsPerSetting:
                            raise StopIteration

        print(f"{self.numAgentsIndex} {self.numSitesIndex} {self.distanceIndex} {self.qualitiesIndex}")

        numAgents = self.numAgentss[self.numAgentsIndex]
        numSites = self.numSitess[self.numSitesIndex]
        distance = self.distances[self.distanceIndex]
        qualities = self.qualitiess[self.numSitesIndex][self.qualitiesIndex]

        settings = [
            Setting("HUB_AGENT_COUNTS", [numAgents]),
            Setting("NUM_SITES", numSites),
            Setting("SITE_POSITIONS", generatePositions(numSites, distance)),
            Setting("SITE_QUALITIES", qualities)
        ]

        setKeysValues(settings)

        return settings


# simsPerSetting = 30
# numAgentss = [50, 100, 200]
# numSitess = [2, 3, 4]
# sitesDistances = [50, 100, 200, 300]
# qualitiess2 = [[0, 128], [0, 128], [0, 128], [0, 128], [0, 128], [0, 128],
#                [0, 128], [0, 128], [0, 128], [0, 128], [0, 128], [0, 128],
#                [0, 128], [0, 128], [0, 128], [0, 128], [0, 128], [0, 128],
#                [0, 128], [0, 128]]
# qualitiess3 = [[0, 128, 255], [0, 128, 255], [0, 128, 255], [0, 128, 255], [0, 128, 255], [0, 128, 255],
#                [0, 128, 255], [0, 128, 255], [0, 128, 255], [0, 128, 255], [0, 128, 255], [0, 128, 255],
#                [0, 128, 255], [0, 128, 255], [0, 128, 255], [0, 128, 255], [0, 128, 255], [0, 128, 255],
#                [0, 128, 255], [0, 128, 255]]
# qualitiess4 = [[0, 128, 255, 255], [0, 128, 255, 255], [0, 128, 255, 255], [0, 128, 255, 255], [0, 128, 255, 255], [0, 128, 255, 255],
#                [0, 128, 255, 255], [0, 128, 255, 255], [0, 128, 255, 255], [0, 128, 255, 255], [0, 128, 255, 255], [0, 128, 255, 255],
#                [0, 128, 255, 255], [0, 128, 255, 255], [0, 128, 255, 255], [0, 128, 255, 255], [0, 128, 255, 255], [0, 128, 255, 255],
#                [0, 128, 255, 255], [0, 128, 255, 255]]
#
# configIter = iter(ConfigIterator(simsPerSetting, numAgentss, numSitess, sitesDistances, qualitiess2, qualitiess3, qualitiess4))
#
# for ind, conf in enumerate(configIter):
#     print(ind + 1)
#     # print(conf)


