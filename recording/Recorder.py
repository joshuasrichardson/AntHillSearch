import json
import numbers

from datetime import datetime

from Constants import RESULTS_DIR
from model.phases import Phase
from model.states import State


def getMostRecentRecording():
    with open(f'{RESULTS_DIR}/most_recent.json', 'r') as file:
        data = json.load(file)
        return data['file_base']


class Recorder:
    """ Records essential site information, agent positions, agent states, and agent phases
    in recording.txt so that the same interface can be played over again """

    def __init__(self):
        self.agentPositions = []
        self.agentAngles = []
        self.agentStates = []
        self.agentPhases = []
        self.agentAssignments = []
        self.predatorPositions = []
        self.predatorAngles = []
        self.agentsToDelete = []
        self.sitePositions = []
        self.siteQualities = []
        self.siteRadii = []
        self.siteMarkerNames = []
        self.siteMarkerArgs = []
        self.siteMarkerNums = []
        self.time = 0
        self.shouldDrawGraphs = False
        self.executedCommands = []
        self.screenBorder = []

        self.data = []

        self.currentAgentPosIndex = -1
        self.currentAgentAngleIndex = -1
        self.currentStateIndex = -1
        self.currentPhaseIndex = -1
        self.currentAssignmentIndex = -1
        self.currentPredatorPosIndex = -1
        self.currentPredatorAngleIndex = -1
        self.currentSitePosIndex = -1
        self.currentQualityIndex = -1
        self.currentRadiusIndex = -1
        self.currentMarkerIndex = -1

        self.dataIndex = -1

        self.timestampString = datetime.now().strftime('%b-%d-%Y--%H:%M:%S')
        self.outputFileBase = f'{RESULTS_DIR}{self.timestampString}'

    def recordAgentInfo(self, agent):
        self.recordAgentPosition(agent.getPosition())
        self.recordAgentAngle(agent.getAngle())
        self.recordState(agent.getStateNumber())
        self.recordPhase(agent.getPhaseNumber())
        self.recordAssignment(agent.getAssignedSiteIndex())

    def recordAgentPosition(self, pos):
        self.agentPositions.append(pos)

    def recordAgentAngle(self, angle):
        self.agentAngles.append(float(angle))

    def recordState(self, state):
        self.agentStates.append(state)

    def recordPhase(self, phase):
        self.agentPhases.append(phase)

    def recordAssignment(self, siteIndex):
        self.agentAssignments.append(siteIndex)

    def recordAgentsToDelete(self, agentIndex):
        self.agentsToDelete = agentIndex

    def recordPredatorPosition(self, pos):
        self.predatorPositions.append(pos)

    def recordPredatorAngle(self, angle):
        self.predatorAngles.append(angle)

    def recordSiteInfo(self, site):
        self.recordSitePosition(site.getPosition())
        self.recordSiteQuality(site.getQuality())
        self.recordSiteRadius(site.radius)
        self.recordSiteMarker(site.markerName, site.commandArg, site.marker)

    def recordSitePosition(self, pos):
        self.sitePositions.append(pos)

    def recordSiteQuality(self, quality):
        self.siteQualities.append(quality)

    def recordSiteRadius(self, radius):
        self.siteRadii.append(radius)

    def recordSiteMarker(self, markerName, arg, num):
        self.siteMarkerNames.append(markerName)
        self.siteMarkerArgs.append(arg)
        if isinstance(num, numbers.Number):
            self.siteMarkerNums.append(num)
        else:
            self.siteMarkerNums.append(-1)

    def recordTime(self, time):
        self.time = time

    def recordShouldDrawGraphs(self, draw):
        self.shouldDrawGraphs = draw

    def recordExecutedCommands(self, commands):
        self.executedCommands = commands

    def recordScreenBorder(self, x, y, w, h):
        if x is None:
            self.screenBorder = None
        else:
            self.screenBorder = [-x, -y, w, h]

    def save(self):
        self.data.append({'agentPositions': self.agentPositions,
                          'agentAngles': self.agentAngles,
                          'agentStates': self.agentStates,
                          'agentPhases': self.agentPhases,
                          'agentAssignments': self.agentAssignments,
                          'agentsToDelete': self.agentsToDelete,
                          'predatorPositions': self.predatorPositions,
                          'predatorAngles': self.predatorAngles,
                          'sitePositions': self.sitePositions,
                          'siteQualities': self.siteQualities,
                          'siteRadii': self.siteRadii,
                          'siteMarkerNames': self.siteMarkerNames,
                          'siteMarkerArgs': self.siteMarkerArgs,
                          'siteMarkerNums': self.siteMarkerNums,
                          'time': self.time,
                          'shouldDrawGraphs': self.shouldDrawGraphs,
                          'executedCommands': self.executedCommands,
                          'screenBorder': self.screenBorder})
        self.agentPositions = []
        self.agentAngles = []
        self.agentStates = []
        self.agentPhases = []
        self.agentAssignments = []
        self.agentsToDelete = []
        self.predatorPositions = []
        self.predatorAngles = []
        self.sitePositions = []
        self.siteQualities = []
        self.siteRadii = []
        self.siteMarkerNames = []
        self.siteMarkerArgs = []
        self.siteMarkerNums = []

    def write(self):
        with open(f'{self.outputFileBase}_RECORDING.json', 'w') as file:
            json.dump(self.data, file)
        with open(f'{self.outputFileBase}_COMMANDS.json', 'w') as file:
            json.dump(self.executedCommands, file)

        self.agentPositions.clear()
        self.agentAngles.clear()
        self.agentStates.clear()
        self.agentPhases.clear()
        self.agentAssignments.clear()
        self.agentsToDelete.clear()
        self.predatorPositions.clear()
        self.predatorAngles.clear()
        self.sitePositions.clear()
        self.siteQualities.clear()
        self.siteRadii.clear()
        self.siteMarkerNames.clear()
        self.siteMarkerArgs.clear()
        self.siteMarkerNums.clear()

    def writeResults(self, positions, qualities, simulationTime, deadAgents):
        results = {'positions': positions,
                   'qualities': qualities,
                   'simulationTime': simulationTime,
                   'deadAgents': deadAgents}

        with open(f'{self.outputFileBase}_RESULTS.json', 'w') as file:
            json.dump(results, file)
        with open(f'{RESULTS_DIR}/most_recent.json', 'w') as file:
            data = {'file_base': f'{self.outputFileBase}'}
            json.dump(data, file)

    def read(self):
        with open(f'{getMostRecentRecording()}_RECORDING.json', 'r') as file:
            self.data = json.load(file)
            self.time = self.data[0]['time']

    @staticmethod
    def readResults():
        try:
            with open(f'{getMostRecentRecording()}_RESULTS.json', 'r') as file:
                results = json.load(file)
                return results['positions'], results['qualities'], results['simulationTime'], results['deadAgents']
        except FileNotFoundError:
            print(f"File '{getMostRecentRecording()}_RESULTS.json' not found.")
            open(f'{getMostRecentRecording()}_RESULTS.json', 'w')
            print(f"Created Empty File: '{getMostRecentRecording()}_RESULTS.json'.")
            return [[-1, -1]], [-1], -1
        except json.decoder.JSONDecodeError:
            print(f"File '{getMostRecentRecording()}_RESULTS.json' is empty.")
            print("Returning arbitrary results")
            return [[-1, -1]], [-1], -1

    def getNextAgentPosition(self):
        self.currentAgentPosIndex += 1
        return self.agentPositions[self.currentAgentPosIndex]

    def getNextAgentAngle(self):
        self.currentAgentAngleIndex += 1
        return self.agentAngles[self.currentAgentAngleIndex]

    def getNextState(self, agent):
        self.currentStateIndex += 1
        return State.numToState(self.agentStates[self.currentStateIndex], agent)

    def getNextPhase(self):
        self.currentPhaseIndex += 1
        return Phase.numToPhase(self.agentPhases[self.currentPhaseIndex])

    def getOriginalAssignments(self):
        return self.data[0]['agentAssignments']

    def getNextAssignment(self):
        self.currentAssignmentIndex += 1
        return self.agentAssignments[self.currentAssignmentIndex]

    def getNextAgentsToDelete(self):
        return self.agentsToDelete

    def getNextPredatorPosition(self):
        self.currentPredatorPosIndex += 1
        return self.predatorPositions[self.currentPredatorPosIndex]

    def getNextPredatorAngle(self):
        self.currentPredatorAngleIndex += 1
        return self.predatorAngles[self.currentPredatorAngleIndex]

    def getNumHubs(self):
        numHubs = 0
        for quality in self.data[0]['siteQualities']:
            if quality == -1:
                numHubs += 1
        return numHubs

    def getNextSitePosition(self):
        self.currentSitePosIndex += 1
        return self.sitePositions[self.currentSitePosIndex]

    def getNextSiteQuality(self):
        self.currentQualityIndex += 1
        return self.siteQualities[self.currentQualityIndex]

    def getNextSiteRadius(self):
        self.currentRadiusIndex += 1
        return self.siteRadii[self.currentRadiusIndex]

    def getNextSiteMarker(self):
        self.currentMarkerIndex += 1
        return [self.siteMarkerNames[self.currentMarkerIndex], self.siteMarkerArgs[self.currentMarkerIndex],
                self.siteMarkerNums[self.currentMarkerIndex]]

    def getNextTime(self):
        return self.time

    def getNextShouldDrawGraphs(self):
        return self.shouldDrawGraphs

    def getNextExecutedCommands(self):
        return self.executedCommands

    def getNextScreenBorder(self):
        return self.screenBorder

    def getNumAgents(self):
        if self.dataIndex >= 0:
            return len(self.agentPositions)
        else:
            return len(self.data[0]['agentPositions'])

    def getNumPredators(self):
        if self.dataIndex >= 0:
            return len(self.predatorPositions)
        else:
            return len(self.data[0]['predatorPositions'])

    def getNumSites(self):
        if self.dataIndex >= 0:
            return len(self.sitePositions)
        else:
            return len(self.data[0]['sitePositions'])

    def setNextRound(self):
        self.dataIndex += 1

        self.currentAgentPosIndex = -1
        self.currentAgentAngleIndex = -1
        self.currentStateIndex = -1
        self.currentPhaseIndex = -1
        self.currentAssignmentIndex = -1
        self.currentPredatorPosIndex = -1
        self.currentPredatorAngleIndex = -1
        self.currentSitePosIndex = -1
        self.currentQualityIndex = -1
        self.currentRadiusIndex = -1
        self.currentMarkerIndex = -1

        if len(self.data) > self.dataIndex:
            self.agentPositions = self.data[self.dataIndex]['agentPositions']
            self.agentAngles = self.data[self.dataIndex]['agentAngles']
            self.agentStates = self.data[self.dataIndex]['agentStates']
            self.agentPhases = self.data[self.dataIndex]['agentPhases']
            self.agentAssignments = self.data[self.dataIndex]['agentAssignments']
            self.agentsToDelete = self.data[self.dataIndex]['agentsToDelete']
            self.predatorPositions = self.data[self.dataIndex]['predatorPositions']
            self.predatorAngles = self.data[self.dataIndex]['predatorAngles']
            self.sitePositions = self.data[self.dataIndex]['sitePositions']
            self.siteQualities = self.data[self.dataIndex]['siteQualities']
            self.siteRadii = self.data[self.dataIndex]['siteRadii']
            self.siteMarkerNames = self.data[self.dataIndex]['siteMarkerNames']
            self.siteMarkerArgs = self.data[self.dataIndex]['siteMarkerArgs']
            self.siteMarkerNums = self.data[self.dataIndex]['siteMarkerNums']
            self.time = self.data[self.dataIndex]['time']
            self.shouldDrawGraphs = self.data[self.dataIndex]['shouldDrawGraphs']
            self.executedCommands = self.data[self.dataIndex]['executedCommands']
            self.screenBorder = self.data[self.dataIndex]['screenBorder']
            return True
        return False
