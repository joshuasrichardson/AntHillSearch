""" Global constants used in swarm simulation program """
import numpy as np

NUM_AGENTS = 100    # Total number of agents in the simulation
SIM_DURATION = 200  # Time of the simulation in seconds
NUM_GOOD = 5        # Number of top sites
NUM_SITES = 10      # Number of total sites

MAX_AGENTS = 200    # Maximum allowed number of agents
MAX_STEPS = 5000    # Maximum allowed duration in seconds
TIME_STEP = 0.2     # Delta t
MAX_N = 30          # Maximum number of possible sites
MAX_M = 10          # Maximum number of "best" sites

""" Define world size, hub location, and distribution parameters for sites """
WORLD_DIM = 700    # Number of pixels in the square world
HUB_LOCATION = [500, 350]  # Location of the hub
HUB_SCALE = 0.01    # Percentage of world dimension that determines size of hub
SITE_SIZE = 20  # How big is the radius of a site?
SITE_OBSERVED_RANGE = int(round(1.25 * float(SITE_SIZE)))  # How close does and agent have to be to "see" a site
SITE_NO_CLOSER_THAN = 200  # How close to hub can a site be?
SITE_NO_FARTHER_THAN = 350  # How far away from hub can a site be?
QUALITY_STD = 255.0*.20  # Standard deviation of the quality of the site assessed by agent
                        # Set to 20% of maximum quality

GRAPH_LOCATION = [120, 80]

# Agent parameters
AGENT_SPEED = 20  # Actual speed is AGENT_SPEED * TIME_STEP
# TODO: Agent speed doesn't make sense as speed times time.

""" Transition parameters for timed transitions """
# REST TO OBSERVE
MIN_REST = 0       # Must rest at least MIN_REST seconds
REST_EXPONENTIAL = 50  # Average number of samples before change
REST_THRESHOLD = 7  # TODO: Get some physics behind this. Magic
# OBSERVE TO EXPLORE
MIN_OBSERVE = 0       # Must rest at least MIN_REST seconds
OBSERVE_EXPONENTIAL = 50  # Average number of samples before change
OBSERVE_THRESHOLD = 7  # TODO: Get some physics behind this. Magic
# EXPLORE TO REST
MIN_EXPLORE = 0       # Must rest at least MIN_REST seconds
EXPLORE_EXPONENTIAL = 50  # Average number of samples before change
EXPLORE_THRESHOLD = 7  # TODO: Get some physics behind this. Magic
# ASSESS_SITE TO ASSES_HUB
MIN_ASSESS = 0       # Must rest at least MIN_REST seconds
ASSESS_EXPONENTIAL = 50  # Average number of samples before change
ASSESS_THRESHOLD = 4  # TODO: Get some physics behind this. Magic
# DANCE_SITE TO DANCE_HUB is same as ASSESS_SITE TO ASSESS_HUB
# DANCE_HUB is given by LingerTime,
# which is proportional to site quality,
# which decays each visit to the site
DANCE_EXPONENTIAL = 50  # Average number of samples before change
DANCE_THRESHOLD = 25  # TODO: Get some physics behind this. Magic
DANCE_DECAY = 0.7


# TODO

# TO_PIPE = 0
# TO_PIPE_THRESHOLD = 0

# TO_COMMIT = 0
# TO_COMMIT_THRESHOLD = 0

ADP_EXPONENTIAL = 50
ADP_THRESHOLD = 25

PIPE_EXPONENTIAL = 50
PIPE_THRESHOLD = 30

PIPE2REST_EXPONENTIAL = 50
PIPE2REST_THRESHOLD = 30

COMMIT_EXPONENTIAL = 50
COMMIT_THRESHOLD = 40

RTFX_EXPONENTIAL = 50
RTFX_THRESHOLD = 20

RTF2REST_EXPONENTIAL = 50
RTF2REST_THRESHOLD = 30


EXPLORE = 0         # Explore agent state
EXPLORE_COLOR = 255, 0, 0   # Red is color of Explorer

AT_NEST = 1            # Rest agent state
REST_COLOR = 0, 0, 0  # Blue

RTFX = 2  # Are we flying?
RTFX_COLOR = 0, 0, 0  # BLACK

ASSESS_HOME = 3     # Assess state where agent returns home to hub
ASSESS_SITE = 4     # Assess state where agent goes to site
ASSESS_COLOR = 204, 204, 0  # Yellow

OBSERVE_HUB = 5     # Observe agent state at hub or traveling to hub
OBSERVE_COLOR = 0, 0, 0  # BLACK

DANCE_HUB = 6       # Dance agent state where dancing is at hub or dancer is traveling to hub
DANCE_SITE = 7      # Dance state where dancer goes to site
DANCE_COLOR = 140, 140, 0  # Dark Yellow

PIPE = 8            # Pipe agent state
PIPE_COLOR = 0, 0, 255  # Blue

COMMIT = 9           # Commit agent state
COMMIT_COLOR = 0, 255, 0  # Green

"""Joshua Ant States"""
FOLLOW = 10          # Following another ant to a nest
FOLLOW_COLOR = 255, 165, 0  # Orange
"""End Joshua Ant States"""

# NUM_POSSIBLE_STATES = COMMIT + 1  # Last state plus 1
NUM_POSSIBLE_STATES = FOLLOW + 1  # Last state plus 1          # """JOSHUA"""
COLORS = [EXPLORE_COLOR, REST_COLOR, RTFX_COLOR, ASSESS_COLOR, ASSESS_COLOR, OBSERVE_COLOR, DANCE_COLOR, DANCE_COLOR, PIPE_COLOR, COMMIT_COLOR, FOLLOW_COLOR]
STATES_LIST = ['EXPLORE', 'REST', 'RTFX', 'ASSESS_HOME', 'ASSESS_SITE', 'OBSERVE', 'DANCE_HUB', 'DANCE_SITE', 'PIPE', 'COMMIT', 'FOLLOW']

"""Phases"""
EXPLORE_PHASE = 0
EXPLORE_PHASE_COLOR = 0, 0, 255  # Blue

ASSESS_PHASE = 1
ASSESS_PHASE_COLOR = 255, 0, 0   # Red

CANVAS_PHASE = 2
CANVAS_PHASE_COLOR = 204, 204, 0  # Yellow

COMMIT_PHASE = 3
COMMIT_PHASE_COLOR = 0, 255, 0  # Green
