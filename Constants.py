""" Global constants used in swarm simulation program """

# Having more agents slows down the simulation, but overall, the behavior is pretty similar.
# They can go to more various sites and things like that with lots of agents,
# but it doesn't have a great effect on where they end up.
NUM_AGENTS = 200    # Total number of agents in the simulation
# The lower the convergence fraction is, the faster the simulation goes because lower fractions require less agents to go to a site
CONVERGENCE_FRACTION = 1.00  # The fraction of the agents that need to be assigned to a site before they are considered converged to that site
# Not having a simulation duration leads to all agents eventually ending up at the same nest.
# Shorter durations increase the likeliness that the colony will be split.
SIM_DURATION = 300  # Time of the simulation in seconds
# More sites lead to longer simulations and higher likeliness of the colony splitting.
NUM_SITES = 4       # Number of total sites
# Setting these, especially the good ones, closer to the hub location makes the simulation end sooner
# [[200, 100], [200, 200], [200, 300], [200, 400], [200, 500], [200, 600], [300, 100], [400, 100], [500, 100], [600, 100], [700, 100], [800, 100], [900, 100], [1000, 100], [1100, 100]]
SITE_POSITIONS = []  # The quality of each site. If a site is not assigned a position here,
#                      it will be assigned a random position in the simulation.
# Setting these more spread apart makes the simulation end sooner and having them close together makes it take longer
#                      because the agents have a harder time deciding between more similar sites.
# [256, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 230, 240, 250, 255]
SITE_QUALITIES = []  # The quality of each site. If a site is not assigned a quality here,
#                      it will be assigned a random quality in the simulation. If quality is set outside the range,
#                      it will be set the the closest number in the range.
# Setting these, especially good ones, bigger makes the simulation end sooner
SITE_RADII = []  # The radius of each site. If a site is not assigned a radius here,
#                  it will be assigned to the SITE_SIZE.
# Does not affect the simulation, but the lower it is, the harder the computer will have to work to execute all the threads
SECONDS_BETWEEN_SENDING_REQUESTS = 5  # Number of seconds between sending information to the rest API and sending more information

# Having this set to False makes the simulation a little faster because it doesn't have to record all the time.
SHOULD_RECORD = True  # Whether the agents' positions, states, phases, and assigned sites will be recorded to be played again later.
# Having this set to False makes the simulation a little faster because it doesn't have to draw all the time.
SHOULD_DRAW = True  # Whether the simulation is drawn on the screen
# Having this false makes the simulation faster because the colors do not have to be drawn on the screen so much.
SHOW_AGENT_COLORS = True  # Whether or not the agents' phase and state colors are drawn on the simulation screen.
# Having this false makes the simulation faster because the numbers do not have to be drawn on the screen so much.
SHOW_ESTIMATED_QUALITY = False  # Whether or not the agents' estimated qualities are drawn on the simulation screen.

MAX_AGENTS = 200    # Maximum allowed number of agents
MAX_TIME = 5000     # Maximum allowed duration in seconds
MAX_NUM_SITES = 30  # Maximum number of possible sites
MAX_FOLLOWERS = 2   # Maximum number of agents that can follow the same lead agent to a site

""" Define colony size, hub location, and distribution parameters for sites """
# The closer it is to the center, the more likely the agents will go to various sites on their way to the site(s) they end up at
HUB_LOCATION = [600, 350]  # Location of the hub
# Bigger sites are easier to find, so bigger sites lead to shorter simulations.
SITES_RADII = 20  # How big is the radius of a site?
# Having closer sites makes everything go faster because they can find sites much sooner, and they can find sites from other sites easier.
SITE_NO_CLOSER_THAN = 100  # How close to hub can a default site be?
# Having closer sites makes everything go faster because they can find sites much sooner, and they can find sites from other sites easier.
SITE_NO_FARTHER_THAN = 400  # How far away from hub can a default site be?

# Does not affect simulation besides making it easier to see what's happening
STATE_GRAPH_LOCATION = [120, 40]  # The location of the graph that shows how many ants are in each state. The left number moves it right more, and the right number moves it down more
# Does not affect simulation besides making it easier to see what's happening
PHASE_GRAPH_LOCATION = [120, 150]  # The location of the graph that shows how many ants are in each phase. The left number moves it right more, and the right number moves it down more
# Does not affect simulation besides making it easier to see what's happening
AGENT_INFO_LOCATION = [120, 230]  # The location of the information about the selected agent
# Does not affect simulation besides making it easier to see what's happening
SITE_INFO_LOCATION = [120, 420]  # The location of the information about the selected site

""" Agent parameters """
HOMOGENOUS_AGENTS = False  # Determines whether the agents have all the same attributes (speed, decisiveness, etc.)
#                            If set to true, they will all have the MAX number as their attribute.
# Setting the speed too high actually makes the simulation take longer because the agents don't turn as
# sharp and find sites as easily.
# Setting it low makes the simulation take longer just because the agents aren't moving as fast.
# Somewhere in the middle (about 4 ~ 25 when DEFAULT_SITE_SIZE is 20) leads to faster simulations.
MIN_AGENT_SPEED = 10  # The slowest possible agent's initial speed
# Each agent's speed will be between these two numbers v^
# 0.8 is the slowest they can go without getting stuck. 25 is about the fastest before it gets too hard to notice sites.
# Above 12, they start to appear on the side of the sites they are at, which is fine if its not too much (like over 25).
MAX_AGENT_SPEED = 12  # The fastest possible agent's initial speed  # Actual speed is AGENT_SPEED * TIME_STEP
# The higher this is, the more their speeds increase when they commit
COMMIT_SPEED_FACTOR = 3  # The number to multiply the agents' speed by when they commit to a site.

# This being lower makes agents take longer to assess, and thus makes the simulation longer
MIN_DECISIVENESS = 0.5  # The factor of the least decisive agent possible (slowest assesser)
# This being lower makes agents take longer to assess, and thus makes the simulation longer
MAX_DECISIVENESS = 2.0  # The factor of the most decisive agent possible (fastest assesser)

# The lower these numbers are, the more likely agents are to get lost while following, making the simulation take longer.
MIN_NAV_SKILLS = 0.1  # The factor of the least skilled navigator possible (most likely to get lost)
MAX_NAV_SKILLS = 2.0  # The factor of the most skilled navigator possible (least likely to get lost)

# The higher this number is, the less accurate the agents' initial judgment about their site is.
# If it really far off, sometimes agents can be taken to a lower quality site than the one they were at.
MIN_QUALITY_MISJUDGMENT = 0  # How close agents' estimatedQuality can be from a site's actual quality.
# The higher this number is, the less accurate the agents' initial judgment about their site is.
# If it really far off, sometimes agents can be taken to a lower quality site than the one they were at.
MAX_QUALITY_MISJUDGMENT = 50  # How far off agents' estimatedQuality can be from a site's actual quality.

""" Transition parameters for timed transitions """
# Threshold probability,
# 1 ==> 36%
# 2 ==> 13%
# 3 ==> 4.9%
# 4 ==> 1.8%
# 5 ==> 0.7%

# If this threshold is too high, then agents have to find better sites through SEARCH or CARRIED.
# If it's too low, then they have to find better sites through follow. A good medium lets them find both ways.
AT_NEST_THRESHOLD = 6  # Influences the likelihood that an agent will go back to their assigned site from searching.

# Lower threshold makes agents more likely to start searching from AT_NEST(not hub)
SEARCH_THRESHOLD = 3  # Should go from AT_NEST to SEARCH
# With 100 agents, 8 ==> about 1 agent every second; if transitions from search are disabled,
# it takes about 45 seconds for half of the agents to go from AT_NEST to SEARCH
SEARCH_FROM_HUB_THRESHOLD = 8  # Should go from AT_NEST(hub) to SEARCH

# This being higher makes agents take longer to assess, and thus makes the simulation longer
MAX_ASSESS_THRESHOLD = 9.0  # The assessment threshold of a site with quality 0
# This being higher makes agents take longer to assess, and thus makes the simulation longer
ASSESS_DIVIDEND = 50.0  # The number the site quality is divided by before being subtracted from the threshold.

GET_LOST_THRESHOLD = 5  # Influences the likelihood that an agent will get lost while following

FOLLOW_THRESHOLD = 1  # Influences the likelihood that an agent will start following another agent

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
THE_SELECTED_COLOR = 255, 0, 0   # Red
SELECTED_COLOR = 0, 255, 244  # Cyan
