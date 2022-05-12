from Constants import GRAPHS_TOP_LEFT, PHASES_LIST, PHASE_COLORS
from config import Config
from display.simulation.Graph import Graph


class PhaseGraph(Graph):
    def __init__(self, phaseCounts):
        numAgents = 0
        for count in Config.HUB_AGENT_COUNTS:
            numAgents += count
        super().__init__("PHASES", PHASES_LIST, phaseCounts, numAgents, PHASE_COLORS, GRAPHS_TOP_LEFT[0],
                         GRAPHS_TOP_LEFT[1] + 200)
