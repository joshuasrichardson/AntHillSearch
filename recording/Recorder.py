import json


class Recorder:
    """ Records essential site information, agent positions, agent states, and agent phases
    in recording.txt so that the same simulation can be played over again """

    def __init__(self):
        self.agentPositions = []
        self.agentStates = []
        self.agentPhases = []
        self.agentAssignments = []
        self.sitePositions = []
        self.siteQualities = []
        self.siteRadii = []

        self.data = []

        self.currentAgentPosIndex = -1
        self.currentStateIndex = -1
        self.currentPhaseIndex = -1
        self.currentAssignmentIndex = -1
        self.currentSitePosIndex = -1
        self.currentQualityIndex = -1
        self.currentRadiusIndex = -1

        self.dataIndex = -1

    def recordAgentInfo(self, agent):
        self.recordAgentPosition(agent.getPosition())
        self.recordState(agent.getState())
        self.recordPhase(agent.phase)
        self.recordAssignment(agent.getAssignedSiteIndex())

    def recordAgentPosition(self, pos):
        self.agentPositions.append(pos)

    def recordState(self, state):
        self.agentStates.append(state)

    def recordPhase(self, phase):
        self.agentPhases.append(phase)

    def recordAssignment(self, siteIndex):
        self.agentAssignments.append(siteIndex)

    def recordSiteInfo(self, site):
        self.recordSitePosition(site.getPosition())
        self.recordSiteQuality(site.getQuality())
        self.recordSiteRadius(site.radius)

    def recordSitePosition(self, pos):
        self.sitePositions.append(pos)

    def recordSiteQuality(self, quality):
        self.siteQualities.append(quality)

    def recordSiteRadius(self, radius):
        self.siteRadii.append(radius)

    def save(self):
        self.data.append({'agentPositions': self.agentPositions,
                          'agentStates': self.agentStates,
                          'agentPhases': self.agentPhases,
                          'agentAssignments': self.agentAssignments,
                          'sitePositions': self.sitePositions,
                          'siteQualities': self.siteQualities,
                          'siteRadii': self.siteRadii})
        self.agentPositions = []
        self.agentStates = []
        self.agentPhases = []
        self.agentAssignments = []
        self.sitePositions = []
        self.siteQualities = []
        self.siteRadii = []

    def write(self):
        with open('../recording/recording.json', 'w') as file:
            json.dump(self.data, file)

    def read(self):
        with open('../recording/recording.json', 'r') as file:
            self.data = json.load(file)

    def getNextAgentPosition(self):
        self.currentAgentPosIndex += 1
        return self.agentPositions[self.currentAgentPosIndex]

    def getNextState(self):
        self.currentStateIndex += 1
        return self.agentStates[self.currentStateIndex]

    def getNextPhase(self):
        self.currentPhaseIndex += 1
        return self.agentPhases[self.currentPhaseIndex]

    def getNextAssignment(self):
        self.currentAssignmentIndex += 1
        return self.agentAssignments[self.currentAssignmentIndex]

    def getNextSitePosition(self):
        self.currentSitePosIndex += 1
        return self.sitePositions[self.currentSitePosIndex]

    def getNextSiteQuality(self):
        self.currentQualityIndex += 1
        return self.siteQualities[self.currentQualityIndex]

    def getNextSiteRadius(self):
        self.currentRadiusIndex += 1
        return self.siteRadii[self.currentRadiusIndex]

    def getNumSites(self):
        return len(self.sitePositions)

    def setNextRound(self):
        self.dataIndex += 1

        self.currentAgentPosIndex = -1
        self.currentStateIndex = -1
        self.currentPhaseIndex = -1
        self.currentAssignmentIndex = -1
        self.currentSitePosIndex = -1
        self.currentQualityIndex = -1
        self.currentRadiusIndex = -1

        if len(self.data) > self.dataIndex:
            self.agentPositions = self.data[self.dataIndex]['agentPositions']
            self.agentStates = self.data[self.dataIndex]['agentStates']
            self.agentPhases = self.data[self.dataIndex]['agentPhases']
            self.agentAssignments = self.data[self.dataIndex]['agentAssignments']
            self.sitePositions = self.data[self.dataIndex]['sitePositions']
            self.siteQualities = self.data[self.dataIndex]['siteQualities']
            self.siteRadii = self.data[self.dataIndex]['siteRadii']
            return True
        else:
            return False
