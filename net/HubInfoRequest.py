import requests

from Constants import *


class HubInfoRequest:
    """ A Request object holding information that is known from the hub.
    This request can be send to a rest API. """

    def __init__(self, agentList):
        # Agent phases count estimates
        self.numExplore = 0
        self.numAssess = 0
        self.numCanvas = 0
        self.numCommit = 0

        # Agent state count estimates
        self.numAtHub = 0
        self.numSearch = 0
        self.numCarried = 0
        self.numLeadForward = 0
        self.numFollow = 0
        self.numReverseTandem = 0
        self.numTransport = 0
        self.numGo = 0
        self.numConverged = 0
        self.numDead = 0

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
        if self.agentPhases[agentIndex] == EXPLORE:
            self.numExplore -= 1
        elif self.agentPhases[agentIndex] == ASSESS:
            self.numAssess -= 1
        elif self.agentPhases[agentIndex] == CANVAS:
            self.numCanvas -= 1
        elif self.agentPhases[agentIndex] == COMMIT:
            self.numCommit -= 1

    def decrementStateCount(self, agentIndex):
        if self.agentStates[agentIndex] == SEARCH:
            self.numSearch -= 1
        elif self.agentStates[agentIndex] == CARRIED:
            self.numCarried -= 1
        elif self.agentStates[agentIndex] == LEAD_FORWARD:
            self.numLeadForward -= 1
        elif self.agentStates[agentIndex] == FOLLOW:
            self.numFollow -= 1
        elif self.agentStates[agentIndex] == REVERSE_TANDEM:
            self.numReverseTandem -= 1
        elif self.agentStates[agentIndex] == TRANSPORT:
            self.numTransport -= 1
        elif self.agentStates[agentIndex] == GO:
            self.numGo -= 1
        elif self.agentStates[agentIndex] == CONVERGED:
            self.numConverged -= 1
        elif self.agentStates[agentIndex] == DEAD:
            self.numDead -= 1

    def incrementPhaseCount(self, agent):
        if agent.getPhaseNumber() == EXPLORE:
            self.numExplore += 1
        elif agent.getPhaseNumber() == ASSESS:
            self.numAssess += 1
        elif agent.getPhaseNumber() == CANVAS:
            self.numCanvas += 1
        elif agent.getPhaseNumber() == COMMIT:
            self.numCommit += 1

    def incrementStateCount(self, agent):
        stateNum = agent.getStateNumber()
        if stateNum == AT_NEST:
            self.numAtHub += 1
        elif stateNum == SEARCH:
            self.numSearch += 1
        elif stateNum == CARRIED:
            self.numCarried += 1
        elif stateNum == LEAD_FORWARD:
            self.numLeadForward += 1
        elif stateNum == FOLLOW:
            self.numFollow += 1
        elif stateNum == REVERSE_TANDEM:
            self.numReverseTandem += 1
        elif stateNum == TRANSPORT:
            self.numTransport += 1
        elif stateNum == GO:
            self.numGo += 1
        elif stateNum == CONVERGED:
            self.numConverged += 1
        elif stateNum == DEAD:
            self.numDead += 1

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
        return {'numExplore': self.numExplore,
                'numAssess': self.numAssess,
                'numCanvas': self.numCanvas,
                'numCommit': self.numCommit,

                'numAtHub': self.numAtHub,
                'numSearch': self.numSearch,
                'numCarried': self.numCarried,
                'numLeadForward': self.numLeadForward,
                'numFollow': self.numFollow,
                'numReverseTandem': self.numReverseTandem,
                'numTransport': self.numTransport,
                'numGo': self.numGo,
                'numConverged': self.numConverged,
                'numDead': self.numDead,

                'sitesPositions': self.sitesPositions,
                'sitesQualities': self.sitesQualities,
                'numAgentsAtSites': self.numAgentsAtSites,
                'sitesRadii': self.sitesRadii}

    @staticmethod
    def sendResultsToAPI(results):
        response = requests.post('http://localhost:5000/sendResults', data=results)
        print("Simulation Results: {}".format(response.text))
