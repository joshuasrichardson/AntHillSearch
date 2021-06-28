import asyncio

import requests
import json

from Constants import *


class SendRequest:

    def __init__(self):
        self.agentList = []

        self.numExplore = 0
        self.numAssess = 0
        self.numCanvas = 0
        self.numCommit = 0

        self.numAtHub = 0
        self.numSearch = 0
        self.numLeadForward = 0
        self.numFollow = 0
        self.numReverseTandem = 0
        self.numTransport = 0
        self.numCarried = 0

        self.sites = set()
        self.bestSitePosition = None
        self.bestSiteQuality = -1
        self.mostAssignedSitePosition = None
        self.mostAssignedSiteQuality = -1

    def addAgentToSendRequest(self, agent):
        if agent.phase == EXPLORE:
            self.numExplore += 1
        if agent.phase == ASSESS:
            self.numAssess += 1
        if agent.phase == CANVAS:
            self.numCanvas += 1
        if agent.phase == COMMIT:
            self.numCommit += 1

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

        self.sites.add(agent.assignedSite)

        # self.agentList.append(self.agentToJson(agent))

    def calculateBestSites(self):
        maxAssigned = 0
        maxQuality = 0
        for site in self.sites:
            if site.agentCount > maxAssigned:
                maxAssigned = site.agentCount
                self.mostAssignedSitePosition = site.getPosition()
                self.mostAssignedSiteQuality = site.getQuality()
            if site.getQuality() > maxQuality:
                maxQuality = site.getQuality()
                self.bestSitePosition = site.getPosition()
                self.bestSiteQuality = site.getQuality()

    def sendHubInfo(self):
        response = requests.get('http://localhost:5000/getHubInfo')
        print("Before: {}".format(response.text))

        hubJson = {'numExplore': self.numExplore,
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
                   'SitePosition': self.sitePosition,  # [1,2,3,4,5,6,7]
                   # Average quality from the last 10 agents for each site
                   'SiteQuality': self.siteQuality, # [0.9,0.2,0.3,0.4,0.5,0.6,0.7]
                   # TODO: numAgents at each site. When agents come back, they report how many agents are at the site they came from
                   #  Keep the latest number for this ^. Do Moving average and set to one

                   # TODO: Don't need these v
                   'bestSitePosition': self.bestSitePosition,
                   'bestSiteQuality': self.bestSiteQuality,
                   'mostAssignedSitePosition': self.mostAssignedSitePosition,
                   'mostAssignedSiteQuality': self.mostAssignedSiteQuality}

        response = requests.post('http://localhost:5000/addHubInfo', data=hubJson)
        print("After: {}".format(response.text))

    def agentToJson(self, agent):
        knownSitePositions = []
        for site in agent.knownSites:
            knownSitePositions.append(site.pos)
        return {'pos': agent.pos,
                'state': agent.state.state,
                'phase': agent.phase,
                'assignedSitePosition': agent.assignedSite.pos,
                'assignedSiteQuality': agent.assignedSite.quality,
                'estimatedQuality': agent.estimatedQuality,
                'speed': agent.speed,
                'decisiveness': agent.decisiveness,
                'navigationSkills': agent.navigationSkills,
                'target': agent.target,
                'angle': agent.angle,
                'knownSites': knownSitePositions,
                'leadAgent': agent.leadAgent}

    def sendAgentInfo(self):
        response = requests.get('http://localhost:5000/getAgents')
        print("Before: {}".format(response.text))

        print("Agent list: " + str(self.agentList))

        for agent in self.agentList:
            response = requests.post('http://localhost:5000/addAgent', data=agent)
        print("After: {}".format(response.text))

    @staticmethod
    def addAgent(agent):
        # if __name__ == "__main__":
        # Call REST API
        response = requests.get('http://localhost:5000/getAgents')
        print("Before: {}".format(response.text))

        newAgent = {'pos': agent.pos,
                    'state': agent.state.state,
                    'assignedSite': agent.assignedSite.pos}

        response = requests.post('http://localhost:5000/addAgent', data=newAgent)
        print("After: {}".format(response.text))
