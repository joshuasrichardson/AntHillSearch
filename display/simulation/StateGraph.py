from Constants import GRAPHS_TOP_LEFT, STATES_LIST, STATE_COLORS
from config import Config
from display.simulation.Graph import Graph


class StateGraph(Graph):
    def __init__(self, stateCounts):
        numAgents = 0
        for count in Config.HUB_AGENT_COUNTS:
            numAgents += count
        super().__init__("STATES", STATES_LIST, stateCounts, numAgents, STATE_COLORS, GRAPHS_TOP_LEFT[0],
                         GRAPHS_TOP_LEFT[1])
