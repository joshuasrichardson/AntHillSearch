""" Global constants used in swarm simulation program """

# Having more agents slows down the simulation, but overall, the behavior is pretty similar.
# They can go to more various sites and things like that with lots of agents,
# but it doesn't have a great effect on where they end up.

NUM_AGENTS = 90    # Total number of agents in the simulation
# Not having a simulation duration leads to all agents eventually ending up at the same nest.
# Shorter durations increase the likeliness that the colony will be split.
SIM_DURATION = 500  # Time of the simulation in seconds
# This doesn't actually do anything right now.
NUM_GOOD = 1        # Number of top sites
# More sites lead to longer simulations and higher likeliness of the colony splitting.
NUM_SITES = 5       # Number of total sites

MAX_AGENTS = 200    # Maximum allowed number of agents
MAX_STEPS = 5000    # Maximum allowed duration in seconds
TIME_STEP = 0.2     # Delta t
MAX_N = 30          # Maximum number of possible sites
MAX_M = 10          # Maximum number of "best" sites
MAX_FOLLOWERS = 2   # Maximum number of agents that can follow the same lead agent to a site

""" Define colony size, hub location, and distribution parameters for sites """
WORLD_DIM = 1000    # Number of pixels in the square colony
# The closer it is to the center, the more likely the agents will go to various sites on their way to the site(s) they end up at
HUB_LOCATION = [500, 350]  # Location of the hub
# Bigger sites are easier to find, so bigger sites lead to shorter simulations.
SITE_SIZE = 20  # How big is the radius of a site?
# Higher observe ranges make sites easier to find, speeding up the simulations.
SITE_OBSERVED_RANGE = int(round(1.25 * float(SITE_SIZE)))  # How close does and agent have to be to "see" a site
# Having closer sites makes everything go faster because they can find sites much sooner, and they can find sites from other sites easier.
SITE_NO_CLOSER_THAN = 100  # How close to hub can a site be?
# Having closer sites makes everything go faster because they can find sites much sooner, and they can find sites from other sites easier.
SITE_NO_FARTHER_THAN = 400  # How far away from hub can a site be?

# Does not affect simulation besides making it easier to see what's happening
STATE_GRAPH_LOCATION = [120, 40]  # The location of the graph that shows how many ants are in each state. The left number moves it right more, and the right number moves it down more
# Does not affect simulation besides making it easier to see what's happening
PHASE_GRAPH_LOCATION = [120, 150]  # The location of the graph that shows how many ants are in each phase. The left number moves it right more, and the right number moves it down more
# Does not affect simulation besides making it easier to see what's happening
AGENT_INFO_LOCATION = [120, 230]  # The location of the information about the selected agent
# Does not affect simulation besides making it easier to see what's happening
SITE_INFO_LOCATION = [120, 420]  # The location of the information about the selected site

# Agent parameters
AGENT_SPEED = 20  # Actual speed is AGENT_SPEED * TIME_STEP

""" Transition parameters for timed transitions """
# Threshold probability,
# 1 ==> 36%
# 2 ==> 13%
# 3 ==> 4.9%
# 4 ==> 1.8%
# 5 ==> 0.7%

# As far as I can tell, changing the exponential doesnt actually make a difference
AT_NEST_EXPONENTIAL = 50
# If this threshold is too high, then agents have to find better sites through SEARCH or CARRIED.
# If it's too low, then they have to find better sites through follow. A good medium lets them find both ways.
AT_NEST_THRESHOLD = 6  # Influences the likelihood that an agent will go back to their assigned site from searching.

# As far as I can tell, changing the exponential doesnt actually make a difference
SEARCH_EXPONENTIAL = 50
# Lower threshold makes agents more likely to start searching from AT_NEST(not hub)
SEARCH_THRESHOLD = 3  # Should go from AT_NEST to SEARCH
# With 100 agents, 8 ==> about 1 agent every second; if transitions from search are disabled,
# it takes about 45 seconds for half of the agents to go from AT_NEST to SEARCH
SEARCH_FROM_HUB_THRESHOLD = 8  # Should go from AT_NEST(hub) to SEARCH

# As far as I can tell, changing the exponential doesnt actually make a difference
ASSESS_EXPONENTIAL = 50
# ASSESS_THRESHOLD = 4

# As far as I can tell, changing the exponential doesnt actually make a difference
GET_LOST_EXPONENTIAL = 50
GET_LOST_THRESHOLD = 5  # Influences the likelihood that an agent will get lost while following  TODO: see if they can get lost in other states

# As far as I can tell, changing the exponential doesnt actually make a difference
FOLLOW_EXPONENTIAL = 50
FOLLOW_THRESHOLD = 1  # Influences the likelihood that an agent will start following another agent

# As far as I can tell, changing the exponential doesnt actually make a difference
LEAD_EXPONENTIAL = 50
# If this is too low (like 3), then the canvasing and committed agents don't stay in the AT_NEST phase much
LEAD_THRESHOLD = 4  # Influences the likelihood that an agent will start recruiting (LEAD_FORWARD or REVERSE_TANDEM)

# The lower this value is, the lower the quality of nests that agents accept can be initially; however, it doesn't make much of a difference in the long run, because agents move from lower-ranked sites to higher-ranked sites either way.
MIN_ACCEPT_VALUE = 255 / 2  # The minimum quality of a nest required for agents to accept it
# The lower this size is, the earlier agents switch over to the committed phase, making other agents come to their site easier.
QUORUM_SIZE = NUM_AGENTS / 2  # The minimum number of agents that need to be at a site before agents will commit to it

""" States and their colors """
AT_NEST = 0            # Rest agent state
AT_NEST_COLOR = 0, 0, 0  # Black

SEARCH = 1                # Explore agent state
SEARCH_COLOR = 0, 0, 255  # Blue

CARRIED = 2
CARRIED_COLOR = 128, 0, 128  # Purple

FOLLOW = 3                # Following another ant to a nest
FOLLOW_COLOR = 255, 165, 0  # Orange

LEAD_FORWARD = 4          # After accepting a site, start to recruit other agents there
LEAD_FORWARD_COLOR = 204, 204, 0  # Yellow

REVERSE_TANDEM = 5        # Going back to the original nest or another known site with a follower to recruit more
REVERSE_TANDEM_COLOR = 0, 128, 128  # Teal

TRANSPORT = 6
TRANSPORT_COLOR = 0, 255, 0  # Green

GO = 7
GO_COLOR = 0, 255, 255  # Cyan

NUM_POSSIBLE_STATES = 8
COLORS = [AT_NEST_COLOR, SEARCH_COLOR, CARRIED_COLOR, FOLLOW_COLOR, LEAD_FORWARD_COLOR, REVERSE_TANDEM_COLOR, TRANSPORT_COLOR, GO_COLOR]
STATES_LIST = ['AT_NEST', 'SEARCH', 'CARRIED', 'FOLLOW', 'LEAD_FWD', 'RVRS_TNDM', 'TRANSPORT', 'GO']

""" Phases and their colors """
EXPLORE = 0
EXPLORE_COLOR = 0, 0, 255  # Blue

ASSESS = 1
ASSESS_COLOR = 255, 0, 0   # Red

CANVAS = 2
CANVAS_COLOR = 204, 204, 0  # Yellow

COMMIT = 3
COMMIT_COLOR = 0, 255, 0  # Green

NUM_POSSIBLE_PHASES = 4
PHASE_COLORS = [EXPLORE_COLOR, ASSESS_COLOR, CANVAS_COLOR, COMMIT_COLOR]
PHASES_LIST = ['EXPLORE', 'ASSESS', 'CANVAS', 'COMMIT']

""" Interaction """
SELECTED_COLOR = 0, 255, 244
