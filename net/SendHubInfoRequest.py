import asyncio

import requests
import json

from Constants import *


class SendHubInfoRequest:

    def __init__(self, agentList):
        self.agentPhases = []
        self.agentStates = []
        for agent in agentList:
            self.agentPhases.append(agent.phase)
            self.agentStates.append(agent.getState())

        # Agent phases count estimates
        self.numExplore = NUM_AGENTS
        self.numAssess = 0
        self.numCanvas = 0
        self.numCommit = 0

        # Agent state count estimates
        self.numAtHub = NUM_AGENTS
        self.numSearch = 0
        self.numLeadForward = 0
        self.numFollow = 0
        self.numReverseTandem = 0
        self.numTransport = 0
        self.numCarried = 0

        # Estimates about site information
        self.sitesPositions = []
        self.sitesQualities = []
        self.numAgentsAtSites = []

    def addAgentToSendRequest(self, agent, agentIndex):
        self.decrementPhaseCount(agentIndex)
        self.agentPhases[agentIndex] = agent.phase

        self.decrementStateCount(agentIndex)
        self.agentStates[agentIndex] = agent.getState()

        self.incrementPhaseCount(agent)
        self.incrementStateCount(agent)

        self.updateSiteInfo(agent)

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
        elif self.agentStates[agentIndex] == LEAD_FORWARD:
            self.numLeadForward -= 1
        elif self.agentStates[agentIndex] == FOLLOW:
            self.numFollow -= 1
        elif self.agentStates[agentIndex] == REVERSE_TANDEM:
            self.numReverseTandem -= 1
        elif self.agentStates[agentIndex] == TRANSPORT:
            self.numTransport -= 1
        elif self.agentStates[agentIndex] == CARRIED:
            self.numCarried -= 1

    def incrementPhaseCount(self, agent):
        if agent.phase == EXPLORE:
            self.numExplore += 1
        elif agent.phase == ASSESS:
            self.numAssess += 1
        elif agent.phase == CANVAS:
            self.numCanvas += 1
        elif agent.phase == COMMIT:
            self.numCommit += 1

    def incrementStateCount(self, agent):
        if agent.state.state == AT_NEST:
            self.numAtHub += 1
        elif agent.state.state == SEARCH:
            self.numSearch += 1
        elif agent.state.state == LEAD_FORWARD:
            self.numLeadForward += 1
        elif agent.state.state == FOLLOW:
            self.numFollow += 1
        elif agent.state.state == REVERSE_TANDEM:
            self.numReverseTandem += 1
        elif agent.state.state == TRANSPORT:
            self.numTransport += 1
        elif agent.state.state == CARRIED:
            self.numCarried += 1

    def updateSiteInfo(self, agent):
        if self.siteIsNew(agent.assignedSite.pos):
            self.sitesPositions.append(agent.assignedSite.pos)
            self.sitesQualities.append(agent.estimatedQuality)
            self.numAgentsAtSites.append(agent.assignedSite.agentCount)
        else:
            siteIndex = 0
            for i in range(0, len(self.sitesPositions) - 1):
                if agent.assignedSite.pos is self.sitesPositions[i]:
                    siteIndex = i
                    break
            self.updateSiteQuality(siteIndex, agent.estimatedQuality)
            self.updateSiteNumAgents(siteIndex, agent.assignedSite.agentCount)

    def siteIsNew(self, sitePosition):
        for sitePos in self.sitesPositions:
            if sitePosition is sitePos:
                return False
        return True

    def updateSiteQuality(self, siteIndex, estimatedQuality):
        # TODO: Instead of just having the current estimated quality have a weight of 9, keep track of the previous 10
        #  and calculate new estimated quality using that.
        self.sitesQualities[siteIndex] = (self.sitesQualities[siteIndex] * 9 + estimatedQuality) / 10

    def updateSiteNumAgents(self, siteIndex, agentCount):
        # TODO: Instead of just having the current number of agents have a weight of 0, keep track of the previous 1
        #  and calculate new number of agents using that.
        self.numAgentsAtSites[siteIndex] = (self.numAgentsAtSites[siteIndex] * 0 + agentCount) / 1

    def sendHubInfo(self):
        response = requests.post('http://localhost:5000/addHubInfo', data=self.hubToJson())
        print("After: {}".format(response.text))

    def hubToJson(self):
        return {'numExplore': self.numExplore,
                'numAssess': self.numAssess,
                'numCanvas': self.numCanvas,
                'numCommit': self.numCommit,
                'numAtHub': self.numAtHub,
                'numSearch': self.numSearch,
                'numLeadForward': self.numLeadForward,
                'numFollow': self.numFollow,
                'numReverseTandem': self.numReverseTandem,
                'numTransport': self.numTransport,
                'numCarried': self.numCarried,
                'sitesPositions': self.sitesPositions,
                'sitesQualities': self.sitesQualities,
                'numAgentsAtSites': self.numAgentsAtSites}
