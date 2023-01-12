import json
import numbers
import os

from datetime import datetime

import Utils
from config import Config
from Constants import RESULTS_DIR, NUM_ROUNDS_NAME, CONFIG_FILE_NAME, FULL_CONTROL_NAME, DISTRACTED_NAME, \
    NUM_SITES_NAME, NUM_PREDATORS_NAME, MAX_NUM_RECORDINGS, RESULTS_FILE_ENDINGS
from display import Display
from model.phases.NumToPhaseConverter import numToPhase
from model.states.NumToStateConverter import numToState
from recording import XlsxWriter
from recording import CsvWriter


def getMostRecentRecording():
    with open(f'{RESULTS_DIR}most_recent.json', 'r') as file:
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
        self.agentEstimates = []
        self.predatorPositions = []
        self.predatorAngles = []
        self.ladybugPositions = []
        self.ladybugAngles = []
        self.obstaclePositions = []
        self.agentsToDelete = []
        self.sitePositions = []
        self.siteQualities = []
        self.siteRadii = []
        self.siteMarkerNames = []
        self.siteMarkerArgs = []
        self.siteMarkerNums = []
        self.time = 0
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
        self.currentLadybugPosIndex = -1
        self.currentLadybugAngleIndex = -1
        self.currentObstaclePosIndex = -1
        self.currentSitePosIndex = -1
        self.currentQualityIndex = -1
        self.currentRadiusIndex = -1
        self.currentMarkerIndex = -1

        self.dataIndex = -1

        self.timestampString = datetime.now().strftime('%b-%d-%Y-%H-%M-%S')
        self.outputFileBase = f'{RESULTS_DIR}{self.timestampString}'

    def record(self, simulation):
        if Config.SHOULD_RECORD:
            self.recordExecutedCommands(simulation.simDisp.commandHistBox.executedCommands)
            if Config.RECORD_ALL:
                self.recordAgentsToDelete(simulation.world.getDeletedAgentsIndexes())
                self.recordTime(simulation.timer.getRemainingTimeOrRounds())
                self.recordScreenBorder(Display.displacementX, Display.displacementY,
                                        Display.origWidth * Display.origWidth / Display.newWidth,
                                        Display.origHeight * Display.origHeight / Display.newHeight)

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

    def recordAgentEstimates(self, agent, agentId):
        self.agentEstimates.append({
            "agentId": agentId,
            "sitePosition:": [int(i) for i in agent.estimatedSitePosition],
            "quality": int(agent.estimatedQuality),
            # "agentCount": int(agent.estimatedAgentCount), # TODO: Actually estimate the count. It seems to be 100 always.
            "radius": int(agent.estimatedRadius),
        })

    def recordAgentsToDelete(self, agentIndex):
        self.agentsToDelete = agentIndex

    def recordPredatorPosition(self, pos):
        self.predatorPositions.append(pos)

    def recordPredatorAngle(self, angle):
        self.predatorAngles.append(angle)

    def recordLadybugPosition(self, pos):
        self.ladybugPositions.append(pos)

    def recordLadybugAngle(self, angle):
        self.ladybugAngles.append(angle)

    def recordObstaclePosition(self, pos):
        self.obstaclePositions.append(pos)

    def recordSiteInfo(self, site):
        self.recordSitePosition(site.getPosition())
        self.recordSiteQuality(site.getQuality())
        self.recordSiteRadius(site.getRadius())
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
                          'ladybugPositions': self.ladybugPositions,
                          'ladybugAngles': self.ladybugAngles,
                          'obstaclePositions': self.obstaclePositions,
                          'sitePositions': self.sitePositions,
                          'siteQualities': self.siteQualities,
                          'siteRadii': self.siteRadii,
                          'siteMarkerNames': self.siteMarkerNames,
                          'siteMarkerArgs': self.siteMarkerArgs,
                          'siteMarkerNums': self.siteMarkerNums,
                          'time': self.time,
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
        self.ladybugPositions = []
        self.ladybugAngles = []
        self.obstaclePositions = []
        self.sitePositions = []
        self.siteQualities = []
        self.siteRadii = []
        self.siteMarkerNames = []
        self.siteMarkerArgs = []
        self.siteMarkerNums = []

    def write(self):
        if Config.RECORD_ALL:
            # Create the folder with the results if it does not exist
            if not os.path.exists(RESULTS_DIR):
                os.makedirs(RESULTS_DIR)

            with open(f'{self.outputFileBase}_RECORDING.json', 'w') as file:
                json.dump(self.data, file)

            self.agentPositions.clear()
            self.agentAngles.clear()
            self.agentStates.clear()
            self.agentPhases.clear()
            self.agentAssignments.clear()
            self.agentsToDelete.clear()
            self.predatorPositions.clear()
            self.predatorAngles.clear()
            self.ladybugPositions.clear()
            self.ladybugAngles.clear()
            self.obstaclePositions.clear()
            self.sitePositions.clear()
            self.siteQualities.clear()
            self.siteRadii.clear()
            self.siteMarkerNames.clear()
            self.siteMarkerArgs.clear()
            self.siteMarkerNums.clear()

            self.data.clear()

        with open(f'{self.outputFileBase}_COMMANDS.json', 'w') as file:
            json.dump({'commands': self.executedCommands}, file)

        self.executedCommands.clear()

        with open(f'{self.outputFileBase}_ESTIMATES.json', 'w') as file:
            json.dump({'agentEstimates': self.agentEstimates}, file)

        self.agentEstimates.clear()

    @staticmethod
    def deleteExcessRecordings():
        # Delete old replays when there are too many, so they don't take up too much space on the computer.
        replays = [file for file in os.listdir('./recording/results/') if file.endswith(RESULTS_FILE_ENDINGS)]
        if len(replays) > MAX_NUM_RECORDINGS * len(RESULTS_FILE_ENDINGS):
            replays = sorted(replays, key=lambda t: -os.stat(f"./recording/results/{t}").st_mtime)  # Sort by date modified (recently modified first)
            replays = replays[MAX_NUM_RECORDINGS * len(RESULTS_FILE_ENDINGS):]  # Delete from the end of the list
            for replay in replays:
                try:
                    os.remove(f"./recording/results/{replay}")
                except FileNotFoundError:
                    pass

    def writeResults(self, results, world):
        CsvWriter.insert(results, world)
        if Config.ONLY_RECORD_LAST:
            return

        # Create the folder with the results if it does not exist
        if not os.path.exists(RESULTS_DIR):
            os.makedirs(RESULTS_DIR)
        with open(f'{self.outputFileBase}_RESULTS.json', 'w') as file:
            json.dump(results, file)
        with open(f'{RESULTS_DIR}/most_recent.json', 'w') as file:
            data = {'file_base': f'{self.outputFileBase}'}
            json.dump(data, file)
        configAbrv = self.recordConfig(world)
        XlsxWriter.jsonFileToXlsx(f'{getMostRecentRecording()}_COMMANDS.json', Config.INTERFACE_NAME,
                                  f"{configAbrv}Commands", "8FD3FE", "DAF0FF", "B5E2FF")

        with open(f'{getMostRecentRecording()}_RESULTS.json', 'r') as jsonFile:
            jsonResultsData = json.load(jsonFile)

        XlsxWriter.jsonToXlsx(jsonResultsData, Config.INTERFACE_NAME, f"{configAbrv}Results")

        ignore = ["SIM_END_TIME", "CHOSEN_HOME_POSITIONS"]
        self.createCharts(configAbrv)
        XlsxWriter.writeSummary(jsonResultsData, Config.INTERFACE_NAME, "Summary", f"{configAbrv}Results", ignore)

        chartsAxes = [["Settings", "Num Rounds"],
                      ["Settings", "Chosen Home Qualities"],
                      ["Settings", "Num Arrivals"],
                      ["Settings", "Num Dead Agents"]]
        colNames = [header.title().replace('_', ' ') for header in jsonResultsData.keys() if header not in ignore]
        stdErrs = XlsxWriter.getResultsStdErrs(Config.INTERFACE_NAME, colNames, 2)
        XlsxWriter.createBarCharts(Config.INTERFACE_NAME, "Summary", chartsAxes, 2, stdErrs)

        del results

    def read(self, selectedReplay=""):
        if selectedReplay == "":
            selectedReplay = f'{getMostRecentRecording()}_RECORDING.json'
        with open(selectedReplay, 'r') as file:
            self.data = json.load(file)
        Utils.setConfig(f'{selectedReplay[0:len(selectedReplay) - 15]}_CONFIG.json')
        Utils.copyJsonToConfig()

    @staticmethod
    def createCharts(configAbrv):
        chartsAxes = [["Num Rounds", "Chosen Home Qualities"],
                      ["Num Rounds", "Num Arrivals"],
                      ["Num Rounds", "Num Dead Agents"],
                      ["Chosen Home Qualities", "Num Arrivals"],
                      ["Chosen Home Qualities", "Num Dead Agents"]]
        XlsxWriter.createScatterPlots(Config.INTERFACE_NAME, f"{configAbrv}Results", chartsAxes, 2)

    def recordConfig(self, world):
        """ Record the actual configuration for the simulation (instead of just showing that certain variables
        were randomized) """
        with open(CONFIG_FILE_NAME, 'r') as configFile:
            configData = json.load(configFile)

        control = "Ful" if configData[FULL_CONTROL_NAME] else "Lim"  # Full control or limited control
        distractions = "Dis" if configData[DISTRACTED_NAME] else "Foc"  # Distracted or focused
        sites = f"S{configData[NUM_SITES_NAME]}"  # S (sites) + the number of sites
        preds = f"P{configData[NUM_PREDATORS_NAME]}"  # P (predators) + the number of predators
        positions = "Ran" if self.posAreRandom(configData) else "Con"  # Random or Constant

        # Get the actual values in simulations where these values were generated randomly
        configData['HUB_RADII'] = f"{list(map(lambda hub: hub.radius, world.hubs))}"
        configData['HUB_POSITIONS'] = f"{list(map(lambda hub: hub.pos, world.hubs))}"
        configData['SITE_RADII'] = f"{list(map(lambda site: site.radius, world.siteList[len(world.hubs):]))}"
        configData['SITE_POSITIONS'] = f"{list(map(lambda site: site.pos, world.siteList[len(world.hubs):]))}"
        configData['SITE_QUALITIES'] = f"{list(map(lambda site: site.quality, world.siteList[len(world.hubs):]))}"
        configData['PRED_POSITIONS'] = f"{list(map(lambda pred: pred.pos, world.predatorList))}"
        for corner in world.floodZone.corners:
            corner[0] += Display.worldLeft
            corner[1] += Display.worldTop
        configData['FLOOD_ZONE_CORNERS'] = f"{world.floodZone.corners}"

        # Record the configuration to a json file for the recording player to use
        with open(f'{self.outputFileBase}_CONFIG.json', 'w') as file:
            json.dump(configData, file)

        # The first part of the name of the sheets with these settings
        configAbrv = f"{control}{distractions}{sites}{preds}{positions}" if Config.RESULTS_FILE_NAME is None \
            else Config.RESULTS_FILE_NAME

        XlsxWriter.jsonToXlsx(configData, Config.INTERFACE_NAME, f"{configAbrv}Config",
                              "FFBE8C", "FFEAD9", "FFDBBF", sep=False)

        return configAbrv

    @staticmethod
    def posAreRandom(configData):
        return configData['SITE_RADII'] == [] and \
               configData['SITE_POSITIONS'] == [] and \
               configData['SITE_QUALITIES'] == [] and \
               configData['PRED_POSITIONS'] == []

    @staticmethod
    def readResults():
        mostRecent = getMostRecentRecording()
        try:
            with open(f'{mostRecent}_RESULTS.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File '{mostRecent}_RESULTS.json' not found.")
            file = open(f'{mostRecent}_RESULTS.json', 'w')
            file.close()
            print(f"Created Empty File: '{mostRecent}_RESULTS.json'.")
            return [[-1, -1]], [-1], -1
        except json.decoder.JSONDecodeError:
            print(f"File '{mostRecent}_RESULTS.json' is empty.")
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
        return numToState(self.agentStates[self.currentStateIndex], agent)

    def getNextPhase(self):
        self.currentPhaseIndex += 1
        return numToPhase(self.agentPhases[self.currentPhaseIndex])

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

    def getNextLadybugPosition(self):
        self.currentLadybugPosIndex += 1
        return self.ladybugPositions[self.currentLadybugPosIndex]

    def getNextLadybugAngle(self):
        self.currentLadybugAngleIndex += 1
        return self.ladybugAngles[self.currentLadybugAngleIndex]

    def getNextObstaclePosition(self):
        self.currentObstaclePosIndex += 1
        return self.obstaclePositions[self.currentObstaclePosIndex]

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

    def getNextExecutedCommands(self):
        return self.executedCommands

    def getNextScreenBorder(self):
        return self.screenBorder

    def getNumRounds(self):
        return self.readResults()[NUM_ROUNDS_NAME]

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

    def getNumLadybugs(self):
        if self.dataIndex >= 0:
            return len(self.ladybugPositions)
        else:
            return len(self.data[0]['ladybugPositions'])

    def getNumObstacles(self):
        if self.dataIndex >= 0:
            return len(self.obstaclePositions)
        else:
            return len(self.data[0]['obstaclePositions'])

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
        self.currentLadybugPosIndex = -1
        self.currentLadybugAngleIndex = -1
        self.currentObstaclePosIndex = -1
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
            self.ladybugPositions = self.data[self.dataIndex]['ladybugPositions']
            self.ladybugAngles = self.data[self.dataIndex]['ladybugAngles']
            self.obstaclePositions = self.data[self.dataIndex]['obstaclePositions']
            self.sitePositions = self.data[self.dataIndex]['sitePositions']
            self.siteQualities = self.data[self.dataIndex]['siteQualities']
            self.siteRadii = self.data[self.dataIndex]['siteRadii']
            self.siteMarkerNames = self.data[self.dataIndex]['siteMarkerNames']
            self.siteMarkerArgs = self.data[self.dataIndex]['siteMarkerArgs']
            self.siteMarkerNums = self.data[self.dataIndex]['siteMarkerNums']
            self.time = self.data[self.dataIndex]['time']
            self.executedCommands = self.data[self.dataIndex]['executedCommands']
            self.screenBorder = self.data[self.dataIndex]['screenBorder']
            return True
        return False
