""" Global constants used in swarm simulation program """

RESULTS_DIR = "recording/results/"  # The directory that stores the results

CONVERGENCE_FRACTION_NAME = "CONVERGENCE_FRACTION"
SIM_DURATION_NAME = "SIM_DURATION"
FONT_SIZE_NAME = "FONT_SIZE"
LARGE_FONT_SIZE_NAME = "LARGE_FONT_SIZE"
NUM_HUBS_NAME = "NUM_HUBS"
HUB_LOCATIONS_NAME = "HUB_LOCATIONS"
HUB_RADII_NAME = "HUB_RADII"
NUM_SITES_NAME = "NUM_SITES"
SITE_RADII_NAME = "SITE_RADII"
SITE_QUALITIES_NAME = "SITE_QUALITIES"
SITE_POSITIONS_NAME = "SITE_POSITIONS"
SITE_RADIUS_NAME = "SITE_RADIUS"
AGENT_IMAGE_NAME = "AGENT_IMAGE"
SITE_NO_CLOSER_THAN_NAME = "SITE_NO_CLOSER_THAN"
HUB_AGENT_COUNTS_NAME = "HUB_AGENT_COUNTS"
SHOULD_RECORD_NAME = "SHOULD_RECORD"
RECORD_ALL_NAME = "RECORD_ALL"
MAX_SEARCH_DIST_NAME = "MAX_SEARCH_DIST"
SITE_NO_FARTHER_THAN_NAME = "SITE_NO_FARTHER_THAN"
NUM_PREDATORS_NAME = "NUM_PREDATORS"
PRED_POSITIONS_NAME = "PRED_POSITIONS"

CONFIG_FILE_NAME = "config/config.json"
# The files that have the settings for user trials
TRIAL_SETTINGS = ["config/trial1settings.json",
                  "config/trial2settings.json",
                  "config/trial3settings.json"]

# Keys for settings that can be changed while the program is running
SETTING_KEYS = [CONVERGENCE_FRACTION_NAME, SIM_DURATION_NAME, FONT_SIZE_NAME, LARGE_FONT_SIZE_NAME, NUM_HUBS_NAME,
                HUB_LOCATIONS_NAME, HUB_RADII_NAME, HUB_AGENT_COUNTS_NAME, NUM_SITES_NAME, SITE_POSITIONS_NAME,
                SITE_QUALITIES_NAME, SITE_RADII_NAME, SHOULD_RECORD_NAME, RECORD_ALL_NAME, SITE_RADIUS_NAME,
                SITE_NO_CLOSER_THAN_NAME, SITE_NO_FARTHER_THAN_NAME, AGENT_IMAGE_NAME, MAX_SEARCH_DIST_NAME,
                NUM_PREDATORS_NAME, PRED_POSITIONS_NAME]

CONFIG_KEYS = SETTING_KEYS + ["SECONDS_BETWEEN_SENDING_REQUESTS", "INITIAL_ZOOM", "SHOULD_DRAW", "SHOULD_DRAW_PATHS",
                              "DRAW_ESTIMATES", "HUB_CAN_MOVE", "DRAW_FAR_AGENTS",
                              "HUB_OBSERVE_DIST", "INITIAL_BLUR", "SHOULD_DRAW_FOG", "AGENT_IMAGES", "HOMOGENOUS_AGENTS", "FIND_SITES_EASILY",
                              "MIN_AVOID_DIST", "MAX_NUM_AVOIDS",
                              "MIN_AGENT_SPEED", "MAX_AGENT_SPEED", "COMMIT_SPEED_FACTOR", "MAX_FOLLOWERS",
                              "MIN_DECISIVENESS", "MAX_DECISIVENESS", "MIN_NAV_SKILLS", "MAX_NAV_SKILLS",
                              "MIN_QUALITY_MISJUDGMENT", "MAX_QUALITY_MISJUDGMENT", "PREDATOR_IMAGE", "PREDATOR_ANGLE",
                              "AT_NEST_THRESHOLD", "SEARCH_THRESHOLD", "SEARCH_FROM_HUB_THRESHOLD",
                              "MAX_ASSESS_THRESHOLD", "ASSESS_DIVIDEND", "GET_LOST_THRESHOLD", "FOLLOW_THRESHOLD",
                              "LEAD_THRESHOLD", "MIN_ACCEPT_VALUE", "QUORUM_DIVIDEND", "KILL_THRESHOLD"]

MAX_TIME = 5000  # Maximum allowed duration in seconds
MAX_NUM_SITES = 30  # Maximum number of possible sites

SCREEN_COLOR = 225, 220, 190  # Light brown

WORDS_COLOR = 0, 41, 0  # Dark green

BORDER_COLOR = 105, 100, 70, 255  # Dark Brown

FOG_COLOR = 145, 140, 112  # Grey

TRANSPARENT = 60, 60, 60  # This value is set to represent a see-through color in the program

# Does not affect interface besides making it easier to see what's happening
GRAPHS_TOP_LEFT = [20, 20]  # The position of the top left corner of the first graph.
#                             The others all build off of that depending on what is being displayed.

""" Site marker names """
GO_NAME = "Go"
AVOID_NAME = "Avoid"
STOP_AVOID_NAME = "StopAvoid"
ASSIGN_NAME = "Assign"
SET_STATE_NAME = "SetState"
NO_MARKER_NAME = "None"

""" States and their colors """
AT_NEST = 0  # Rest agent state
AT_NEST_COLOR = 0, 0, 0  # Black

SEARCH = 1  # Explore agent state
SEARCH_COLOR = 0, 0, 255  # Blue

CARRIED = 2
CARRIED_COLOR = 128, 0, 128  # Purple

FOLLOW = 3  # Following another ant to a nest
FOLLOW_COLOR = 255, 165, 0  # Orange

LEAD_FORWARD = 4  # After accepting a site, start to recruit other agents there
LEAD_FORWARD_COLOR = 204, 204, 0  # Yellow

REVERSE_TANDEM = 5  # Going back to the original nest or another known site with a follower to recruit more
REVERSE_TANDEM_COLOR = 0, 128, 128  # Teal

TRANSPORT = 6  # Picking up other agents and bringing them to the assigned site
TRANSPORT_COLOR = 0, 255, 0  # Green

GO = 7  # Moving toward a specific position until getting there
GO_COLOR = 0, 255, 255  # Cyan

DEAD = 8  # No longer respond to anything.
DEAD_COLOR = 140, 140, 140  # Grey

ESCAPE = 9  # Trying to run away from predators.
ESCAPE_COLOR = 255, 255, 255  # White

NUM_POSSIBLE_STATES = 10
# Colors that show up on the screen representing each state
STATE_COLORS = [AT_NEST_COLOR, SEARCH_COLOR, CARRIED_COLOR, FOLLOW_COLOR, LEAD_FORWARD_COLOR, REVERSE_TANDEM_COLOR,
                TRANSPORT_COLOR, GO_COLOR, DEAD_COLOR, ESCAPE_COLOR]
# The name of each state
STATES_LIST = ['AT_NEST', 'SEARCH', 'CARRIED', 'FOLLOW', 'LEAD_FWD', 'RVRS_TNDM', 'TRANSPORT', 'GO', 'DEAD', 'ESCAPE']

""" Phases and their colors """
EXPLORE = 0  # Still at the hub or just leaving for the first time to search
EXPLORE_COLOR = 0, 0, 255  # Blue

ASSESS = 1  # Found a potential site and considering whether it is good enough
ASSESS_COLOR = 255, 0, 0  # Red

CANVAS = 2  # Partially committed to a site, and starting to lead others there
CANVAS_COLOR = 204, 204, 0  # Yellow

COMMIT = 3  # Met quorum at a site and now fully committed to the site
COMMIT_COLOR = 0, 255, 0  # Green

CONVERGED = 4  # Enough agents are at the site, so they can be done moving
CONVERGED_COLOR = 255, 105, 180

NUM_POSSIBLE_PHASES = 5
# Colors that show up on the screen representing each phase
PHASE_COLORS = [EXPLORE_COLOR, ASSESS_COLOR, CANVAS_COLOR, COMMIT_COLOR, CONVERGED_COLOR]
# The name of each phase
PHASES_LIST = ['EXPLORE', 'ASSESS', 'CANVAS', 'COMMIT', "CONVERGED"]

""" Interaction """
SELECTED_COLOR = 0, 255, 244  # Cyan

AGENT_OPTIONS = ['Select', 'Wide Select', 'Set Group', 'Select Group', 'Half', 'Next', 'Previous', 'Speed Up',
                 'Slow Down', 'Set Check Point', 'Move', 'Assign to Site', 'Avoid', 'Set State', 'Kill', 'Create',
                 'Delete', 'Unselect']

AGENT_OPTION_BUTTONS = ['- LEFT CLICK', '- DRAG LEFT CLICK', '- CTRL + 0-9', '- 0-9', '- H', '- RIGHT ARROW',
                        '- LEFT ARROW', '- F', '- S', '- W', '- SPACE or RIGHT CLICK', '- A', '- Z', '- ALT + 0-6',
                        '- K', '- X', '- DEL or /', '- ESC']

SITE_OPTIONS = ['Select', 'Wide Select', 'Next', 'Previous', 'Move', 'Set Quality', 'Raise Quality', 'Lower Quality',
                'Expand', 'Shrink', 'Create', 'Delete', 'Set Check Point', 'Set Go Point', 'Set Assign Site',
                'Set Avoid Area', 'Set Agents States', 'Remove Command', 'Unselect']

SITE_OPTION_BUTTONS = ['- LEFT CLICK', '- DRAG LEFT CLICK', '- RIGHT ARROW', '- LEFT ARROW', '- DRAG LEFT CLICK',
                       '- 0-9/BACKSPACE + RETURN', '- UP ARROW', '- DOWN ARROW', '- = (+)', '- -', '- C',
                       '- DEL or /', '- W', '- SPACE or RIGHT CLICK', '- A', '- Z', '- ALT + 0-6', '- .', '- ESC']

CONTROL_OPTIONS = {"agentOptions": AGENT_OPTIONS,
                   "agentOptionButtons": AGENT_OPTION_BUTTONS,
                   "siteOptions": SITE_OPTIONS,
                   "siteOptionButtons": SITE_OPTION_BUTTONS}

UI_AGENT_OPTIONS = ['Select', 'Wide Select', 'Half', 'Next', 'Previous', 'Set Check Point', 'Move', 'Assign to Site',
                    'Avoid', 'Set State', 'Unselect']

UI_AGENT_OPTION_BUTTONS = ['- LEFT CLICK', '- DRAG LEFT CLICK', '- H', '- RIGHT ARROW', '- LEFT ARROW',
                           '- W', '- SPACE or RIGHT CLICK', '- A', '- Z', '- ALT + 0-6', '- ESC']

UI_SITE_OPTIONS = ['Select', 'Wide Select', 'Next', 'Previous', 'Set Check Point', 'Set Go Point', 'Set Assign Site',
                   'Set Avoid Area', 'Set Agents States', 'Remove Command', 'Unselect']

UI_SITE_OPTION_BUTTONS = ['- LEFT CLICK', '- DRAG LEFT CLICK', '- RIGHT ARROW', '- LEFT ARROW',
                          '- W', '- SPACE or RIGHT CLICK', '- A', '- Z', '- ALT + 0-6', '- .', '- ESC']

UI_CONTROL_OPTIONS = {"agentOptions": UI_AGENT_OPTIONS,
                      "agentOptionButtons": UI_AGENT_OPTION_BUTTONS,
                      "siteOptions": UI_SITE_OPTIONS,
                      "siteOptionButtons": UI_SITE_OPTION_BUTTONS}

RECORDING_AGENT_OPTIONS = ['Select', 'Wide Select', 'Half', 'Next', 'Previous', 'Unselect']

RECORDING_AGENT_OPTION_BUTTONS = ['- LEFT CLICK', '- DRAG LEFT CLICK', '- H', '- RIGHT ARROW', '- LEFT ARROW', '- ESC']

RECORDING_SITE_OPTIONS = ['Select', 'Wide Select', 'Next', 'Previous', 'Unselect']

RECORDING_SITE_OPTION_BUTTONS = ['- LEFT CLICK', '- DRAG LEFT CLICK', '- RIGHT ARROW', '- LEFT ARROW', '- ESC']

RECORDING_CONTROL_OPTIONS = {"agentOptions": RECORDING_AGENT_OPTIONS,
                             "agentOptionButtons": RECORDING_AGENT_OPTION_BUTTONS,
                             "siteOptions": RECORDING_SITE_OPTIONS,
                             "siteOptionButtons": RECORDING_SITE_OPTION_BUTTONS}

""" Json result keys """
NUM_ROUNDS_NAME = "numRounds"
SIM_TIMES_NAME = "simulationTimes"
HOME_POSITIONS_NAME = "chosenHomesPositions"
HOME_QUALITIES_NAME = "chosenHomesQualities"
NUM_ARRIVALS_NAME = "numArrivals"
NUM_DEAD_NAME = "numDeadAgents"
TOTAL_NAME = "totalNumAgents"
