import requests

from Constants import *


class HubInfoRequest:
    """ A Request object holding information that is known from the hub. """

    def __init__(self, agentList, stateCounts, phaseCounts):
        """ agentList - a list of all the agents in the colony
        stateCounts - a list of the number of agents in each state
        phaseCounts - a list of the number of agents in each phase """
        # Agent state and phase count estimates
        self.stateCounts = stateCounts  # List of the number of agents assigned to each state
        self.phaseCounts = phaseCounts  # List of the number of agents assigned to each phase

        self.agentPhases = []
        self.agentStates = []
        for agent in agentList:
            self.agentPhases.append(agent.getPhaseNumber())
            self.incrementPhaseCount(agent)
            self.agentStates.append(agent.getStateNumber())
            self.incrementStateCount(agent)

        # Estimates about site information
        self.sitesPositions = []
        self.sitesEstimatedPositions = []
        self.sitesPreviousNPositions = []
        self.sitesQualities = []
        self.sitesPreviousNQualities = []
        self.numAgentsAtSites = []
        self.sitesRadii = []
        self.sitesPreviousNRadii = []

    def addAgent(self, agent):
        self.agentPhases.append(agent.getPhaseNumber())
        self.agentStates.append(agent.getStateNumber())
        self.incrementPhaseCount(agent)
        self.incrementStateCount(agent)

    def removeAgent(self, agentIndex):
        self.decrementPhaseCount(agentIndex)
        self.decrementStateCount(agentIndex)
        self.agentPhases.pop(agentIndex)
        self.agentStates.pop(agentIndex)

    def addAgentToHubInfo(self, agent, agentIndex):
        self.decrementPhaseCount(agentIndex)
        self.agentPhases[agentIndex] = agent.getPhaseNumber()

        self.decrementStateCount(agentIndex)
        self.agentStates[agentIndex] = agent.getStateNumber()

        self.incrementPhaseCount(agent)
        self.incrementStateCount(agent)

        return self.updateSiteInfo(agent)

    def decrementPhaseCount(self, agentIndex):
        phaseNumber = self.agentPhases[agentIndex]
        self.phaseCounts[phaseNumber] -= 1

    def decrementStateCount(self, agentIndex):
        stateNumber = self.agentStates[agentIndex]
        self.stateCounts[stateNumber] -= 1

    def incrementPhaseCount(self, agent):
        self.phaseCounts[agent.getPhaseNumber()] += 1

    def incrementStateCount(self, agent):
        self.stateCounts[agent.getStateNumber()] += 1

    def updateSiteInfo(self, agent):
        if self.siteIsNew(agent.assignedSite.pos):  # The first time a site is found, just add the current agent's estimated values
            self.sitesPositions.append(agent.assignedSite.pos)
            self.sitesEstimatedPositions.append(agent.estimatedSitePosition)
            self.sitesPreviousNPositions.append([agent.estimatedSitePosition])
            self.sitesQualities.append(agent.estimatedQuality)
            self.sitesPreviousNQualities.append([agent.estimatedQuality])
            self.numAgentsAtSites.append(agent.assignedSite.estimatedAgentCount)
            self.sitesRadii.append(agent.estimatedRadius)
            self.sitesPreviousNRadii.append([agent.estimatedRadius])

            return self.sitesEstimatedPositions[len(self.sitesEstimatedPositions) - 1], \
                self.sitesQualities[len(self.sitesQualities) - 1], \
                self.numAgentsAtSites[len(self.numAgentsAtSites) - 1], \
                self.sitesRadii[len(self.sitesRadii) - 1]
        else:  # If it's not the first time encountering a site, the estimated values need to be averaged out
            siteIndex = 0
            for i in range(len(self.sitesPositions)):
                if agent.assignedSite.pos[0] == self.sitesPositions[i][0] \
                        and agent.assignedSite.pos[1] == self.sitesPositions[i][1]:
                    siteIndex = i
                    break
            self.updateSitePosition(siteIndex, agent.estimatedSitePosition)
            self.updateSiteQuality(siteIndex, agent.estimatedQuality)
            self.numAgentsAtSites[siteIndex] = agent.assignedSite.estimatedAgentCount
            self.updateSiteRadius(siteIndex, agent.estimatedRadius)

            return self.sitesEstimatedPositions[siteIndex], \
                self.sitesQualities[siteIndex], \
                self.numAgentsAtSites[siteIndex], \
                self.sitesRadii[siteIndex]

    def siteIsNew(self, sitePosition):
        """ Determines whether the site is new or not based on its position """
        return not self.sitesPositions.__contains__(sitePosition)

    def updateSitePosition(self, siteIndex, estimatedPosition):
        self.sitesPreviousNPositions[siteIndex].append(estimatedPosition)
        n = 100
        average = self.getAverageOfLastNPos(n, siteIndex, self.sitesPreviousNPositions)
        self.sitesEstimatedPositions[siteIndex][0] = average[0]
        self.sitesEstimatedPositions[siteIndex][1] = average[1]

    def updateSiteQuality(self, siteIndex, estimatedQuality):
        self.sitesPreviousNQualities[siteIndex].append(estimatedQuality)
        n = 50
        self.sitesQualities[siteIndex] = self.getAverageOfLastNQualities(n, siteIndex)

    def getAverageOfLastNQualities(self, n, siteIndex):
        return self.getAverageOfLastN(n, siteIndex, self.sitesPreviousNQualities)

    def updateSiteRadius(self, siteIndex, estimatedRadius):
        self.sitesPreviousNRadii[siteIndex].append(estimatedRadius)
        n = 80
        self.sitesRadii[siteIndex] = self.getAverageOfLastNRadii(n, siteIndex)

    def getAverageOfLastNRadii(self, n, siteIndex):
        return self.getAverageOfLastN(n, siteIndex, self.sitesPreviousNRadii)

    @staticmethod
    def getAverageOfLastN(n, arrayIndex, array2D):
        if n < 1:
            return 0
        total = 0
        length = len(array2D[arrayIndex])
        if length < n:
            n = length
        for i in range(length - 1, length - n - 1, -1):
            total += array2D[arrayIndex][i]
        return total / n

    @staticmethod
    def getAverageOfLastNPos(n, arrayIndex, array2D):
        totalX = 0
        totalY = 0
        length = len(array2D[arrayIndex])
        if length < n:
            n = length
        for i in range(length - 1, length - n - 1, -1):
            totalX += array2D[arrayIndex][i][0]
            totalY += array2D[arrayIndex][i][1]
        x = totalX / n
        y = totalY / n
        return [x, y]

    def sendHubInfo(self):
        response = requests.post('http://localhost:5000/addHubInfo', data=self.hubToJson())
        print("Simulation Status: {}".format(response.text))

    def hubToJson(self):
        return {'numExplore': self.phaseCounts[EXPLORE],
                'numAssess': self.phaseCounts[ASSESS],
                'numCanvas': self.phaseCounts[CANVAS],
                'numCommit': self.phaseCounts[COMMIT],
                'numConverged': self.phaseCounts[CONVERGED],

                'numAtNest': self.stateCounts[AT_NEST],
                'numSearch': self.stateCounts[SEARCH],
                'numCarried': self.stateCounts[CARRIED],
                'numLeadForward': self.stateCounts[LEAD_FORWARD],
                'numFollow': self.stateCounts[FOLLOW],
                'numReverseTandem': self.stateCounts[REVERSE_TANDEM],
                'numTransport': self.stateCounts[TRANSPORT],
                'numGo': self.stateCounts[GO],
                'numDead': self.stateCounts[DEAD],

                'sitesPositions': self.sitesPositions,
                'sitesQualities': self.sitesQualities,
                'numAgentsAtSites': self.numAgentsAtSites,
                'sitesRadii': self.sitesRadii}

    @staticmethod
    def sendResultsToAPI(results):
        response = requests.post('http://localhost:5000/sendResults', data=results)
        print("Simulation Results: {}".format(response.text))
