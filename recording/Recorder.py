from colony.myPygameUtils import createScreen
from recording.CopySite import CopySite


class Recorder:

    def __init__(self, numAgents, sites):
        self.commands = []
        self.numAgents = numAgents
        if sites is not None:
            self.sites = sites
        else:
            self.sites = []
        self.positions = []
        self.result = None
        self.currentPosIndex = -1
        self.surface = None

    def record(self, command):
        self.commands.append(command)

    def recordPosition(self, pos):
        self.positions.append(pos)

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
            for i in range(2 + (numSites * 3), len(self.result) - 1):
                res = self.result[i][1:-1]
                position = [int(s) for s in res.split(',')]
                self.positions.append(position)

    def replay(self):
        for command in self.commands:
            command.execute()

    def getNextPosition(self):
        self.currentPosIndex += 1
        if len(self.positions) > self.currentPosIndex:
            return self.positions[self.currentPosIndex]
        else:
            return -1

    def getSurface(self):
        if self.surface is None:
            self.surface = createScreen()
        return self.surface
