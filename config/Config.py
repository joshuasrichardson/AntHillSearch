""" The default values for configurations. Many of these values can be overridden
 by the config.json file, by selecting a certain interface, or by changing the
 configuration in the Settings tab while the program is running. """

from numpy import sin, pi

RESULTS_FILE_NAME = None
ONLY_RECORD_LAST = True
INTERFACE_NAME = "Engineering"
FULL_CONTROL = True  # Whether the user can access all the controls in the interface.
DISTRACTED = False  # Whether the user is distracted
# The lower the convergence fraction is, the faster the interface goes because lower fractions require fewer agents to go to a site
CONVERGENCE_FRACTION = 0.80  # The fraction of the agents that need to be assigned to a site before they are considered converged to that site
# Not having an interface duration leads to all agents eventually ending up at the same nest.
# Shorter durations increase the likeliness that the colony will be split.

USE_ROUNDS_AS_DURATION = True
SIM_DURATION = 25000  # Time of the interface in seconds or rounds

FONT_SIZE = 13  # The font size of most words in the simulation
LARGE_FONT_SIZE = 40  # The font size for titles and such
INITIAL_ZOOM = -6  # How far in or out the zoom is at the beginning

FLOOD_ZONE_SHAPE = "Any"  # The shape of the flood zone if the FLOOD_ZONE_CORNERS are not set.
FLOOD_ZONE_COVERAGE = 0  # The percentage of the world within MAX_SEARCH_DISTANCE of the hub that the flood zone covers
# if the FLOOD_ZONE_CORNERS are not set.
FLOOD_ZONE_CORNERS = []  # The positions of corners of the flood zone. If this list has more than 2 values,
# the FLOOD_ZONE_COVERAGE variable will be ignored to have the flood zone line up with these corners.

NUM_HUBS = 1  # The number of starting homes or the number of colonies
HUB_POSITIONS = []  # A list of positions of where the original homes are located
HUB_RADII = []  # A list of the radius of the hubs
# Having more agents slows down the interface, but overall, the behavior is pretty similar.
# They can go to more various sites and things like that with lots of agents,
# but it usually doesn't have a great effect on where they end up.
HUB_AGENT_COUNTS = [100]  # Number of agents starting out at each hub

# More sites lead to longer simulations and higher likeliness of the colony splitting.
NUM_SITES = 5  # Number of total sites
# Setting these, especially the good ones, closer to the hub location makes the interface end sooner
# [[200, 100], [200, 200], [200, 300], [200, 400], [200, 500], [200, 600], [300, 100], [400, 100], [500, 100], [600, 100], [700, 100], [800, 100], [900, 100], [1000, 100], [1100, 100]]
SITE_POSITIONS = []  # The quality of each site. If a site is not assigned a position here,
#                      it will be assigned a random position in the interface.
# Setting these more spread apart makes the interface end sooner and having them close together makes it take longer
#                      because the agents have a harder time deciding between more similar sites.
# [256, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 230, 240, 250, 255]
SITE_QUALITIES = []  # The quality of each site. If a site is not assigned a quality here,
#                      it will be assigned a random quality in the interface. If quality is set outside the range,
#                      it will be set the the closest number in the range.
# Setting these, especially good ones, bigger makes the interface end sooner
SITE_RADII = []  # The radius of each site. If a site is not assigned a radius here,
#                  it will be assigned to the SITE_SIZE.
# Does not affect the interface, but the lower it is, the harder the computer will have to work to execute all the threads
SECONDS_BETWEEN_SENDING_REQUESTS = 5  # Number of seconds between sending information to the rest API and sending more information
# Having this set to False makes the interface a little faster, but not much. However, it does prevent errors from not having the API running.
USE_REST_API = False  # Whether the interface sends information about the hub to the rest API
# Having this set to False makes the interface a little faster because it doesn't have to record all the time.
SHOULD_RECORD = True  # Whether the agents' positions, states, phases, and assigned sites will be recorded to be played again later.
# Having this set to False makes the interface a little faster because it doesn't have to record all movements etc.
RECORD_ALL = False
# Having this set to False makes the interface a little faster because it doesn't have to draw all the time.
SHOULD_DRAW = True  # Whether the interface is drawn on the screen
# Having this false makes the interface faster because the paths do not have to be drawn on the screen so much.
SHOULD_DRAW_PATHS = False

DRAW_ESTIMATES = False  # If True, only estimates of sites' qualities, positions, sizes, etc. will be drawn. If False, exact values will be drawn.

HUB_CAN_MOVE = True  # Whether the hub can be moved

DRAW_FAR_AGENTS = True  # Whether agents that aren't right by the hub are drawn

""" Define colony size, hub location, and distribution parameters for sites """
HUB_OBSERVE_DIST = 80  # The farthest distance agents can be seen from the center of the hub
# Bigger sites are easier to find, so bigger sites lead to shorter simulations.
SITE_RADIUS = 30  # The default radius of the sites.
# Having closer sites makes everything go faster because they can find sites much sooner, and they can find sites from other sites easier.
SITE_NO_CLOSER_THAN = 300  # How close to hub can a default site be?
# Having closer sites makes everything go faster because they can find sites much sooner, and they can find sites from other sites easier.
SITE_NO_FARTHER_THAN = 400  # How far away from hub can a default site be?
INITIAL_BLUR = 8  # How blurry the sites are when they are found

""" Agent parameters """
AGENT_IMAGE = "resources/ant.png"  # The image that is displayed on the screen to represent an agent
AGENT_IMAGES = ["resources/copter.png",
                "resources/ant.png"]  # A list of names of files that users can set their agent image to
HOMOGENOUS_AGENTS = False  # Determines whether the agents have all the same attributes (speed, decisiveness, etc.)
#                            If set to true, they will all have the MAX number as their attribute.
# Having this set to True helps the interface go faster if user controls are used. If they are not used, it makes no difference.
FIND_SITES_EASILY = False  # If True, agents will be able to go directly to their assigned site when it is moved.
#                                    If False, agents will have to search for their site again when it moves.
# The smaller the max distance is, the faster the interface ends because agents never get too far away from the sites
# (unless it is set too small, and they cannot get to sites other than the hub without being forced to turn around).
MAX_SEARCH_DIST = SITE_NO_FARTHER_THAN  # The farthest an agent can get away from the hub while searching.
HUB_MIN_X = 0 - MAX_SEARCH_DIST  # The farthest left a hub can randomly be placed.
HUB_MIN_Y = 0 - MAX_SEARCH_DIST  # The farthest left a hub can randomly be placed.
HUB_MAX_X = 1250 + MAX_SEARCH_DIST  # The farthest right a hub can randomly be placed.
HUB_MAX_Y = 650 + MAX_SEARCH_DIST  # The farthest right a hub can randomly be placed.
MIN_AVOID_DIST = 100  # The closest an ant can get to a point the it is avoiding.
AVOID_MARKER_XY = MIN_AVOID_DIST * sin(pi / 4)  # x and y distances to corners of circle.
MAX_NUM_AVOIDS = 4  # The max number of areas an agent or site can avoid.
# Setting the speed too high actually makes the interface take longer because the agents don't turn as
# sharp and find sites as easily.
# Setting it low makes the interface take longer just because the agents aren't moving as fast.
# Somewhere in the middle (about 4 ~ 25 when DEFAULT_SITE_SIZE is 20) leads to faster simulations.
MIN_AGENT_SPEED = 10  # The slowest possible agent's initial speed
# Each agent's speed will be between these two numbers v^
# 0.8 is the slowest they can go without getting stuck. 25 is about the fastest before it gets too hard to notice sites.
# Above 12, they start to appear on the side of the sites they are at, which is fine if its not too much (like over 25).
MAX_AGENT_SPEED = 12  # The fastest possible agent's initial speed  # Actual speed is AGENT_SPEED * TIME_STEP
# The higher this is, the more their speeds increase when they commit
COMMIT_SPEED_FACTOR = 3  # The number to multiply the agents' speed by when they commit to a site.
MAX_FOLLOWERS = 2  # Maximum number of agents that can follow the same lead agent to a site

# This being lower makes agents take longer to assess, and thus makes the interface longer
MIN_DECISIVENESS = 0.5  # The factor of the least decisive agent possible (slowest assesser)
# This being lower makes agents take longer to assess, and thus makes the interface longer
MAX_DECISIVENESS = 2.0  # The factor of the most decisive agent possible (fastest assesser)

# The lower these numbers are, the more likely agents are to get lost while following, making the interface take longer.
MIN_NAV_SKILLS = 0.05  # The factor of the least skilled navigator possible (most likely to get lost)
MAX_NAV_SKILLS = 2.0  # The factor of the most skilled navigator possible (least likely to get lost)

# The higher this number is, the less accurate the agents' initial judgment about their site is.
# If it really far off, sometimes agents can be taken to a lower quality site than the one they were at.
MIN_QUALITY_MISJUDGMENT = 0  # How close agents' estimatedQuality can be from a site's actual quality.
# The higher this number is, the less accurate the agents' initial judgment about their site is.
# If it really far off, sometimes agents can be taken to a lower quality site than the one they were at.
MAX_QUALITY_MISJUDGMENT = 50  # How far off agents' estimatedQuality can be from a site's actual quality.

""" Predator default values """

PREDATOR_IMAGE = "resources/spider.png"  # The path of the predator image
PREDATOR_ANGLE = pi / 2  # The initial angle the predator in the image is facing
NUM_PREDATORS = 0  # The number of predators that go around attacking agents
PRED_POSITIONS = []  # Where the predators will start. No position = random

""" Ladybug default values """

LADYBUG_IMAGE = "resources/ladybug.png"  # The path of the ladybug image
LADYBUG_ANGLE = pi / 2  # The initial angle the ladybug in the image is facing
NUM_LADYBUGS = 0  # The number of ladybugs that go around helping agents
LADYBUG_POSITIONS = []  # Where the ladybugs will start. No position =
# random

OBSTACLE_IMAGE = "resources/obstacle.jpg"  # The path of the obstacle image
OBSTACLE_ANGLE = pi / 2  # The initial angle the obstacle in the image is facing
NUM_OBSTACLES = 0  # The number of obstacles in the simulation
OBSTACLE_POSITIONS = []  # Where the obstacles will be placed. No position = random

""" Agent Transition Parameters """
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
SEARCH_THRESHOLD = 4  # Should go from AT_NEST to SEARCH
# With 100 agents, 8 ==> about 1 agent every second; if transitions from search are disabled,
# it takes about 45 seconds for half of the agents to go from AT_NEST to SEARCH
SEARCH_FROM_HUB_THRESHOLD = 8  # Should go from AT_NEST(hub) to SEARCH

# This being higher makes agents take longer to assess, and thus makes the interface longer
MAX_ASSESS_THRESHOLD = 9.0  # The assessment threshold of a site with quality 0
# This being higher makes agents take longer to assess, and thus makes the interface longer
ASSESS_DIVIDEND = 50.0  # The number the site quality is divided by before being subtracted from the threshold.

GET_LOST_THRESHOLD = 5  # Influences the likelihood that an agent will get lost while following

FOLLOW_THRESHOLD = 1  # Influences the likelihood that an agent will start following another agent

FOLLOW_DANCE_THRESHOLD = 6  # Influences the likelihood that an agent will start following another agent

# If this is too low (like 3), then the canvasing and committed agents don't stay in the AT_NEST phase much
LEAD_THRESHOLD = 4  # Influences the likelihood that an agent will start recruiting (LEAD_FORWARD or REVERSE_TANDEM)

# The lower this value is, the lower the quality of nests that agents accept can be initially; however, it doesn't make much of a difference in the long run, because agents move from lower-ranked sites to higher-ranked sites either way.
MIN_ACCEPT_VALUE = 255 / 2  # The minimum quality of a nest required for agents to accept it
# The lower this size is, the earlier agents switch over to the committed phase, making other agents come to their site easier.
QUORUM_DIVIDEND = 7  # numAgents/QUORUM_DIVIDEND agents need to be at a site before agents will commit to it

KILL_THRESHOLD = 2  # # Influences the likelihood that a predator will kill an agent

HELP_THRESHOLD = 1  # Influences the likelihood that a ladybug will help an agent


PROB_RA = 0.05
PROB_RE = 0.02
PROB_EA = 0.05
PROB_AD = 0.05
PROB_DA = 0.05
PROB_ER = 0.005
PROB_DR = 0.05


NUM_REPLAYS = 10
