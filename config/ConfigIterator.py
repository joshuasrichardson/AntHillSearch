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


class ConfigIterator:
    def __init__(self, simsPerSetting, simsPerPos, numAgentss, numSitess, distances, *qualitiess):
        self.settings = None
        self.simsPerSetting = simsPerSetting
        self.simsPerPos = simsPerPos
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
        self.posIndex = 1
        self.simIndex = 0
        self.numAgentsIndex = 0
        self.numSitesIndex = 0
        self.distanceIndex = 0
        self.qualitiesIndex = -1
        return self

    def __next__(self):
        if self.posIndex < self.simsPerPos and self.qualitiesIndex >= 0:
            self.posIndex += 1
            return self.settings
        self.posIndex = 1

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

        self.settings = [
            Setting("HUB_AGENT_COUNTS", [numAgents]),
            Setting("NUM_SITES", numSites),
            Setting("SITE_POSITIONS", generatePositions(numSites, distance)),
            Setting("SITE_QUALITIES", qualities)
        ]

        return self.settings


