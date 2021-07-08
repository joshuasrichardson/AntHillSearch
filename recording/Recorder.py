from recording.CopySite import CopySite


class Recorder:
    """ Records essential site information, agent positions, agent states, and agent phases
    in recording.txt so that the same simulation can be played over again """

    def __init__(self, numAgents, sites):
        self.numAgents = numAgents
        if sites is not None:
            self.sites = sites
        else:
            self.sites = []
        self.positions = []
        self.states = []
        self.phases = []
        self.assignments = []
        self.result = None
        self.currentPosIndex = -1
        self.currentStateIndex = -1
        self.currentPhaseIndex = -1
        self.currentAssignmentIndex = -1

    def recordAgentInfo(self, agent):
        self.recordPosition(agent.getPosition())
        self.recordState(agent.getState())
        self.recordPhase(agent.phase)
        self.recordAssignment(agent.getAssignedSiteIndex())

    def recordPosition(self, pos):
        self.positions.append(pos)

    def recordState(self, state):
        self.states.append(state)

    def recordPhase(self, phase):
        self.phases.append(phase)

    def recordAssignment(self, siteIndex):
        self.assignments.append(siteIndex)

    def save(self):
        with open('../recording/recording.txt', 'w') as file:
            file.write(str(self.numAgents) + "\n")
            file.write(str(len(self.sites)) + "\n")
            for site in self.sites:
                file.write(str(site.pos) + "\n")
                file.write(str(site.radius) + "\n")
                file.write(str(site.quality) + "\n")
            for pos in self.positions:
                file.write(str(pos) + "\n")
            for state in self.states:
                file.write(str(state) + "\n")
            file.write("Phases:\n")
            for phase in self.phases:
                file.write(str(phase) + "\n")
            file.write("Assignments:\n")
            for assignment in self.assignments:
                file.write(str(assignment) + "\n")

    def read(self):
        with open('../recording/recording.txt', 'r') as file:
            text = file.read()
            self.result = text.split('\n')
            self.numAgents = int(self.result[0])
            numSites = int(self.result[1])
            for i in range(2, (numSites * 3) + 2, 3):
                res = self.result[i][1:-1]
                pos = [int(s) for s in res.split(',')]
                radius = int(self.result[i + 1])
                quality = int(self.result[i + 2])
                site = CopySite(pos, radius, quality)
                self.sites.append(site)
            index = 0
            for i in range(2 + (numSites * 3), len(self.result) - 1):
                if self.result[i][0] is not '[':
                    index = i
                    break
                res = self.result[i][1:-1]
                position = [int(s) for s in res.split(',')]
                self.positions.append(position)
            for i in range(index, len(self.result) - 1):
                if self.result[i].__contains__("Phases:"):
                    index = i + 1
                    break
                self.states.append(int(self.result[i]))
            for i in range(index, len(self.result) - 1):
                if self.result[i].__contains__("Assignments:"):
                    index = i + 1
                    break
                self.phases.append(int(self.result[i]))
            for i in range(index, len(self.result) - 1):
                self.assignments.append(int(self.result[i]))
                # self.assignments.append(int(self.result[i]))

    def getNextPosition(self):
        self.currentPosIndex += 1
        if len(self.positions) > self.currentPosIndex:
            return self.positions[self.currentPosIndex]
        else:
            return -1

    def getNextState(self):
        self.currentStateIndex += 1
        if len(self.states) > self.currentStateIndex:
            return self.states[self.currentStateIndex]
        else:
            return -1

    def getNextPhase(self):
        self.currentPhaseIndex += 1
        if len(self.phases) > self.currentPhaseIndex:
            return self.phases[self.currentPhaseIndex]
        else:
            return -1

    def getNextAssignment(self):
        self.currentAssignmentIndex += 1
        if len(self.assignments) > self.currentAssignmentIndex:
            return self.assignments[self.currentAssignmentIndex]
        else:
            return -1
