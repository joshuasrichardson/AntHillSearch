""" Global constants used in swarm simulation program """
import numpy as np

NUM_AGENTS = 50    # Total number of agents in the simulation
SIM_DURATION = 300  # Time of the simulation in seconds
NUM_GOOD = 1        # Number of top sites
NUM_SITES = 3      # Number of total sites

MAX_AGENTS = 200    # Maximum allowed number of agents
MAX_STEPS = 5000    # Maximum allowed duration in seconds
TIME_STEP = 0.2     # Delta t
MAX_N = 30          # Maximum number of possible sites
MAX_M = 10          # Maximum number of "best" sites
MAX_FOLLOWERS = 2   # Maximum number of agents that can follow the same lead agent to a site

""" Define world size, hub location, and distribution parameters for sites """
WORLD_DIM = 1000    # Number of pixels in the square world
HUB_LOCATION = [500, 350]  # Location of the hub
HUB_SCALE = 0.01    # Percentage of world dimension that determines size of hub
SITE_SIZE = 20  # How big is the radius of a site?
SITE_OBSERVED_RANGE = int(round(1.25 * float(SITE_SIZE)))  # How close does and agent have to be to "see" a site
SITE_NO_CLOSER_THAN = 200  # How close to hub can a site be?
SITE_NO_FARTHER_THAN = 400  # How far away from hub can a site be?
QUALITY_STD = 255.0*.20  # Standard deviation of the quality of the site assessed by agent
                        # Set to 20% of maximum quality

STATE_GRAPH_LOCATION = [120, 40]  # The location of the graph that shows how many ants are in each state. The left number moves it right more, and the right number moves it down more
PHASE_GRAPH_LOCATION = [120, 150]  # The location of the graph that shows how many ants are in each phase. The left number moves it right more, and the right number moves it down more

# Agent parameters
AGENT_SPEED = 20  # Actual speed is AGENT_SPEED * TIME_STEP
# TODO: Agent speed doesn't make sense as speed times time.

""" Transition parameters for timed transitions """
AT_NEST_EXPONENTIAL = 50  # Average number of samples before change
AT_NEST_THRESHOLD = 7

SEARCH_EXPONENTIAL = 50  # Average number of samples before change
SEARCH_THRESHOLD = 4  # Higher number is less likely
SEARCH_FROM_HUB_THRESHOLD = 8  # Higher number is less likely

ASSESS_EXPONENTIAL = 50  # Average number of samples before change
ASSESS_THRESHOLD = 4  # Higher number is less likely

COMMIT_EXPONENTIAL = 50
COMMIT_THRESHOLD = 40

GET_LOST_EXPONENTIAL = 50  # TODO
GET_LOST_THRESHOLD = 5    # TODO

RECRUIT_EXPONENTIAL = 50  # TODO
RECRUIT_THRESHOLD = 20  # TODO

FOLLOW_EXPONENTIAL = 50  # TODO
FOLLOW_THRESHOLD = 3  # TODO

LEAD_EXPONENTIAL = 50  # TODO
LEAD_THRESHOLD = 3  # TODO

MIN_ACCEPT_VALUE = 255/2  # The minimum quality of a nest required for agents to accept it
QUORUM_SIZE = NUM_AGENTS / 2  # The minimum number of agents that need to be at a site before agents will commit to it

""" States and their colors """
SEARCH = 0         # Explore agent state
SEARCH_COLOR = 0, 0, 255  # Blue

AT_NEST = 1            # Rest agent state
AT_NEST_COLOR = 0, 0, 0  # Black

FOLLOW = 2          # Following another ant to a nest
FOLLOW_COLOR = 255, 165, 0  # Orange

LEAD_FORWARD = 3
LEAD_FORWARD_COLOR = 204, 204, 0  # Yellow

COMMIT = 4           # Commit agent state
COMMIT_COLOR = 0, 255, 0  # Green

NUM_POSSIBLE_STATES = COMMIT + 1  # Last state plus 1
COLORS = [AT_NEST_COLOR, SEARCH_COLOR, FOLLOW_COLOR, LEAD_FORWARD_COLOR, COMMIT_COLOR]
STATES_LIST = ['AT_NEST', 'SEARCH', 'FOLLOW', 'LEAD_FWD', 'COMMIT']

""" Phases and their colors """
EXPLORE_PHASE = 0
EXPLORE_PHASE_COLOR = 0, 0, 255  # Blue

ASSESS_PHASE = 1
ASSESS_PHASE_COLOR = 255, 0, 0   # Red

CANVAS_PHASE = 2
CANVAS_PHASE_COLOR = 204, 204, 0  # Yellow

COMMIT_PHASE = 3
COMMIT_PHASE_COLOR = 0, 255, 0  # Green

NUM_POSSIBLE_PHASES = 4
PHASE_COLORS = [EXPLORE_PHASE_COLOR, ASSESS_PHASE_COLOR, CANVAS_PHASE_COLOR, COMMIT_PHASE_COLOR]
PHASES_LIST = ['EXPLORE', 'ASSESS', 'CANVAS', 'COMMIT']
