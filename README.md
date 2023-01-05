# Ant Hill Search Simulation

## Overview

- Introduction
- Running the Program
- Parameters
- Optional Methods
- Interfaces
- Controls

## Introduction

This program is a simulation of how ants find a new home
after their previous home has been destroyed. Agents (the
ants who search for a new home) go through various
levels of commitment (referred to as phases) as well as various
states on their way to reaching their new home. Their goal is
to converge to the site with the highest quality (to solve the
best of N problem).

In the simulation, the hub (the agents' original home) is
represented by a black circle, and the other sites are
represented by circles with different shades of red or green
depending on their quality. The bright green sites are the best,
and the bright red sites are the worst. Brownish sites are
somewhere in the middle. There are also bars next to each site
that represent the quality. The fuller the bar, the higher the
quality. Agents are represented by smaller copters or ant images
(depending on the settings) and, when they are selected,
surrounded by circles with colors representing
their current phase and state.

### Phases: Levels of Commitment

#### Explore

Each agent starts out in the Explore phase, where they have no
knowledge of any site beside the hub. When they come to a new
site, they enter the Assess phase.

#### Assess

In the Assess phase, an agent initially accepts
or rejects the site. If they reject the site, they stay in the
Assess phase and go look for other sites. If they accept it,
they enter the Canvasing phase.

#### Canvas

The Canvasing phase is where they start recruiting other agents
to their assigned site. When a quorum has met at a site,
in other words if enough agents are
at the same site at the same time, these agents will enter the
Committed phase.

#### Committed

The agent is fully committed to their assigned site and their
recruiting becomes faster.

#### Converged

For simulations where there is more than one hub, we added a Converged
phase. This phase was not in the original model, but we added it
so that the user can see which groups of agents still need to find a site.

### States

#### Original States

Agents' states include At Nest, Search, Lead Forward, Follow,
Transport, Reverse Tandem, Carried, Escape, Go, and Dead. These
states use phases.

Use these by setting <code>Constants.SIMPLIFY_STATES</code>
to <code>False</code>

##### At Nest

The agent is at one of the sites (which can include the hub).

##### Search

The agent is out looking for other sites to evaluate.

##### Lead Forward

The agent (in the Canvasing phase) starts to recruit other
agents to their assigned site.

##### Follow

The agent goes with an agent in the Lead Forward or Reverse Tandem
state to get to another site.

##### Reverse Tandem

The agent (in the committed phase) leads other agents from their
assigned site to another site they know about.
From there, both the leader and the follower lead more agents back
to the site they are committed to.

##### Transport

The agent (in the Committed phase) picks up agents that are either
searching or at a nest.

##### Carried

The agent is picked up by another agent in the Transport state
and brought to the transporting agent's site to evaluate it for
themselves.

##### Escape

The agent saw a dead agent or a predator and is running away
from where they saw it.

##### Go

The agent is going where the user sent them.

##### Dead

The agent will not move again for the rest of the simulation.


#### Simplified States (4-State State Machine)

Agents' states include Rest, Explore, Assess, and Dance. These
states do not use phases.

Use these by setting <code>Constants.SIMPLIFY_STATES</code>
to <code>True</code>

##### Rest

The agent is at the hub doing nothing.

##### Explore

The agent is out looking for other sites to evaluate.

##### Assess

The agent has found a site and is evaluating how good it is.

##### Dance

The agent has found a site that they like and are back at the 
hub recommending it to other agents.


### Other Bugs

Predators can also be added to the simulation. When the agents come
in contact with the predators, the predators attack them. If the agents
get away safely, they avoid the area, if not, they die and stay there
till the end of the simulation. Agents who come across dead agents
turn away and avoid coming back to that area.

Lady bugs can also be added to the simulation. When an agent finds
a lady bug, the lady bug directs it to the best quality site.

### References

More details about the phases and states can be found by reading
["An agent-based model of collective nest choice by the ant Temnothorax albipennis"](https://www-sciencedirect-com.erl.lib.byu.edu/science/article/pii/S0003347205002332)
by Stephen C. Pratt, David J. T. Sumpter, Eamonn B. Mallon, and Nigel R.
Franks. The model in this Anthill Search program is mostly based on the
model represented in the "Structure of the Model" section of this paper, but
adjustments such as the Converged phase, Go state, and Dead state have been added
to allow for interactions with users and predators.

Another useful paper about this topic is found at
["Nest Site Choices in Social Insects"](https://www-sciencedirect-com.erl.lib.byu.edu/science/article/pii/B9780128096338012620?via%3Dihub)
We did not find this one till after implementing the model,
but it had useful information about when the ants decide to
switch from the Canvas phase to the Commit phase.
It also contains a paragraph about factors that make a site good.
We could implement these in the future, but for now, the quality is
just represented by a number.

### Additional Information

In addition to the states and phases described above, many options for
user interaction have been added. See the "Parameters" section for
details about how to change the simulation's set up. The provided
interfaces handle many of these parameters, allowing for a few different
use cases, but variables such as the number of sites may need to be
changed by the one running the program. See the "Controls"
section for details about how to interact with the simulation while
it is running.

## Running the Program

1. Using the terminal, navigate to the <code>AntHillSearch/</code>
   directory on your computer (It should be the same directory as
   this <code>README.md</code>).
2. If this is your first time running the program on your machine,
   enter <code>pip install -r requirements.txt</code>. This will
   install all the necessary dependencies for running the program.
3. (Optional) To change parameters from the default parameters, see the
   "Parameters" section below.
4. (Optional) To change which interface you want to run, see the comments
   in <code>Colony.py</code>'s <code>main</code> method. (Learn more about
   interfaces in the "Interface" section of this document).
5. Enter <code>python Colony.py</code> in the terminal to start up the
   program.
6. If you are using the Empirical Testing interface, simply wait
   for the ants to find their new home. Otherwise, select "Tutorial"
   or "Practice" to become familiar with how the program works.
   1. If desired, try using some user controls while the
      simulation is running (see "Controls" for more details).

## Parameters

The parameters can have a big impact on the setup and behavior
of the simulation. A list of the default parameters and more
information about them can be found in
<code>config/Config.py</code>.

There are 2 main ways to change the parameters:

1. While the program is running, select the Settings tab from
   the main menu, select the option to be changed, type the
   desired values, and press enter.
   Note that this method can only change certain parameters,
   but it will override the method below.
2. Change the values in <code>config/config.json</code>.
   For a complete list of parameters that can be changed here,
   refer to <code>Constants.py</code>'s <code>CONFIG_KEYS</code>

Some other parameters such as <code>SIMPLIFY_STATES</code> must
be changed directly in the code. These can generally be found in
<code>Constants.py</code> or <code>config/Config.py</code>.

Important methods and their parameters to know about are listed
below.

Using the interfaces mentioned in the "Interfaces" Section below
is an easy way to change the way the simulation runs without changing
a bunch of parameters.

## Optional Methods to Add to Colony.py

The following methods can be added to a live colony simulation
(not the RecordingPlayer interface) in
the main function to change the initial state.

### <code>LiveSimulation.randomizeInitialState()</code>

Assigns each agent in the simulation a random site and position to start from.

This method has no parameters. Also, note that it cannot be called with the
RecordingPlayer.

### <code>LiveSimulation.addAgents()</code>

Adds agents to the simulation (in addition to the <code>numAgents</code> specified in
the constructor). These agents can be given specific starting states, phases,
locations, and assignments.

- <code>numAgents</code> (required): Integer to set the number of agents to create with
  the specified state, phase, assignedSite, and startingPosition.
- <code>state</code> (required): State that the agents start in.
- <code>phase</code> (required): Integer to set the phase that the agents start in.
- <code>assignedSiteIndex</code> (required): Integer that sets the agents' assigned
  site to the nth site in the site list.
- <code>startingPosition</code>: Ordered pair that sets where the agents start in
  the simulation.

Note that this method can not be used with the RecordingPlayer.

## Interfaces

There are currently 4 different interfaces available as listed below.

For a more game-like simulation, you can make a <code>StartUpDisplay</code>
object and pass an interface into the constructor (either <code>UserInterface</code>
or <code>EngineerInterface</code>). To play this one, call <code>run()</code>
on the <code>StartUpDisplay</code> object.

### EngineerInterface

This interface is the one that shows the most information. When
there is a choice between drawing something and not drawing it,
this interface usually draws it. It also provides accurate info
about where agents are and site values. This interface also
allows more user controls than the other interfaces. All parameters
can still be manually set by the user as is shown for the
LiveSimulation in the "Parameters" section above, but different
default values apply.

This interface is good for testing new functionality and more
clearly seeing how the simulation works.

### UserInterface

This interface does not show as much information as the Engineering
Interface. Agents and their paths are only drawn when they are close
to the hub, and the sites drawn only reflect what the agents that have
returned to the hub have estimated about them. This interface allows
some user controls, but they are limited to what can be done from the
hub. All parameters can still be manually set by the user as is shown
for the LiveSimulation in the "Parameters" section above, but
different default values apply.

This interface is good if you want the user to have the perspective of
a leader at the hub.

### EmpiricalTestingInterface

This interface is good for collecting results quickly without user
interactions. It is many times faster than the
<code>UserInterface</code> because it doesn't draw the screen, and
it can run 16 simulations concurrently.

This interface is the one that shows the least information. Nothing
is drawn on the screen, and the user has no control over what happens.
The most important information is simply reported at the end of the
simulation. This information is not the complete accurate information in
the Engineer Interface; it is what is known from the hub like in the
User Interface. With nothing being drawn, this interface is faster than
the others and allows users to run more simulations in a shorter time
to gather empirical data. All parameters can still be manually set
by the user as is shown for the LiveSimulation in the "Parameters"
section above, but different default values apply.

### RecordingPlayer

This interface shows about as much information as the Engineering
Interface, but users have no control over what happens. Parameters
have no effect on the simulation because all the instructions come
from the <code>recording/_date-time_\_RECORDING.json</code> file.

## Controls

The controls allow a user to interact with the
simulation by doing things such as telling agents
where to go, creating sites, pausing, etc. These
can be adjusted by changing statements in the
<code>handleEvent</code> method found in <code>
user.Controls</code> Below is a complete list of
all the controls available right now (There may
be more to come).

All of these controls are available in the Engineering
interface, but many are not available in the User
interface or Recording interface. None are available in
the Empirical Testing interface.

### Agent Controls

- <strong>Select Agent</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can select agents by clicking on them with the mouse. 
  A circle will be drawn around the selected agent to help the user 
  keep track of where it is. Selected agents can also be told where 
  to go, assigned to a site, told to avoid an area, killed, or deleted 
  (see "Move Agent," "Assign Agent to Site," "Delete Agent," "Avoid Area,"
  and "Kill Agent" below).</p>
- <strong>Wide Select</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEMOTION</code>,
  <code>MOUSEBUTTONUP</code>:
  <p>Users can select a group of agents by clicking
  somewhere with the mouse, sliding the mouse over the 
  agents they want to select, and releasing the mouse button.
  When a group of agents is selected and the "Move Agent,"
  "Assign Agent to Site," "Delete Agent," "Avoid Area,"
  or "Kill Agent" command is used, the command applies to 
  all the selected agents. The number of agents currently 
  selected shows up on the screen next to the cursor.</p>

- <strong>Set Agent Group</strong> - <code>CTRL</code>, <code>0-9</code>:
  <p>Users can set the selected agents to be a group that can 
  easily be selected again later (see "Select Agent Group" below)
  by holding down the <code>CTRL</code> key and pushing a number key.</p>
- <strong>Select Agent Group</strong> - <code>0-9</code>:
  <p>Users can select a set group of agents (see "Set Agent Group" above)
  by pressing the corresponding number key. This does not work if
  a site is selected because the "Set Site Quality" control will 
  apply. Additional agent groups can be selected by holding down 
  <code>SHIFT</code> and selecting the other groups numbers. By 
  default, 10% of the agents are assigned to each number group to start.</p>

- <strong>Half</strong> - <code>h</code>:
  <p>Users can unselect half of the selected agents by pressing the 
  <code>h</code> key. The agent that is surrounded by a red circle and
  whose information shows up on the side of the screen will not be
  unselected by this, but other than that, there is no way to predict
  which agents will be unselected.</p>

- <strong>Next Agent</strong> - <code>RIGHT</code>:
  <p>When users have selected a group of agents with "Wide Select,"
  they can see which site one of the agents is assigned to and where
  that agent is heading by looking at the dashed lines coming from it.
  Using "Next" allows the user to see the next selected agent's site
  and target instead.
  the screen.</p>

- <strong>Previous Agent</strong> - <code>LEFT</code>:
  <p>When users have selected a group of agents with "Wide Select,"
  they can see which site one of the agents is assigned to and where
  that agent is heading by looking at the dashed lines coming from it.
  Using "Previous" allows the user to see the previous selected agent's 
  site and target instead.</p>

- <strong>Speed Up</strong> - <code>f</code>:
  <p>Users can cause the agents to move faster by pushing the 
  <code>f</code> key. In live simulations, this is not the same 
  as fast forwarding the simulation because the time still 
  runs at the same speed. It is just a way to make each agent 
  move faster. In recordings, it is like fast forwarding</p>

- <strong>Slow Down</strong> - <code>s</code>:
  <p>Users can cause the agents to move slower by pushing the 
  <code>s</code> key. In live simulations, this is not the same 
  as slowing the whole simulation down because the time still
  runs at the same speed. It is just a way to make each agent 
  move slower. In recordings, it is slowing the whole simulation down.</p>

- <strong>Set Check Point</strong> - <code>W</code>:
  <p>Users can tell agents where to go on the way to their destination
  before using the "Move Agent" command by pressing <code>w</code>.</p>

- <strong>Move Agent</strong> - <code>SPACE</code> or <code>RIGHT_CLICK</code>:
  <p>Users can tell agents where to go by selecting the agents 
  (see "Select Agent" and "Wide Select" above), moving the mouse
  to the position they want the agent to go to, and pushing the
  <code>SPACE</code> bar. All selected agents then keep moving
  toward the indicated spot until they get there. When they arrive, 
  they transition into the Search state.</p>

- <strong>Assign Agent to Site</strong> - <code>a</code>:
  <p>Users can assign agents to a site by selecting the agents 
  (see "Select Agent" and "Wide Select" above), moving the mouse
  over the site they want the agent to be assigned to, and pushing the
  <code>a</code> key. All selected agents then keep moving
  toward the indicated site until they get there. When they arrive, 
  they transition into the At Nest state.</p>

- <strong>Set Agent State</strong> - <code>ALT</code> + <code>0-6</code>:
  <p>Users can set the state of an agent by holding down the <code>ALT</code> 
  key and pressing a number corresponding with the state. When <code>ALT</code>
  is held down, the numbers corresponding to the states appear on the screen. 
  Note that if states are dependent on other agents being in a certain state
  and no other agents are in that certain state, then this command will not
  actually do anything. For example, if the user commands agents to enter the
  FOLLOW state, but there are no agents in a recruiting state, then the agent
  will stay in the same state it was in before the command was executed.</p>

- <strong>Create Agent</strong> - <code>x</code>:
  <p>Users can create new agents during the simulation by pressing
  the <code>x</code> key. A new agent will appear where the mouse is
  and start moving in a random direction in the Search state.</p>

- <strong>Delete Agents</strong> - <code>SLASH</code> or <code>DELETE</code>:
  <p>Users can delete all the selected agents by pressing the <code>/</code> 
  or <code>DELETE</code> key (on some keyboards, the <code>DELETE</code> key
  does not work).</p>

- <strong>Unselect Agents</strong> - <code>ESC</code>:
  <p>Users can unselect all agents by pressing the escape button.</p>

- <strong>Avoid Area</strong> - <code>Z</code>:
  <p>Users can tell all the selected agents to avoid an area by pressing the
  <code>Z</code> key with their cursor over the center of the area to avoid.</p>

- <strong>Kill Agent</strong> - <code>K</code>:
  <p>Users can kill agents by pressing <code>K</code> while the agents are selected.</p>

### Site Controls

- <strong>Select Site</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can select sites by clicking on them with the mouse. 
  A circle will be drawn around the site to  help the user see 
  where it is. Selected sites can also be moved, expanded, shrunk, 
  deleted, or have their quality increased, decreased, or set to 
  any number between 0 and 255. (see "Move Site," "Expand Site," 
  "Shrink Site," "Delete Site," "Raise Quality," "Lower Quality," 
  and "Set Quality" below).</p>

- <strong>Wide Select</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEMOTION</code>,
  <code>MOUSEBUTTONUP</code>:
  <p>Users can select a group of sites by clicking
  somewhere with the mouse, sliding the mouse over the sites 
  they want to select, and releasing the mouse button.
  When a group of sites is selected and the "Move Site," 
  "Expand Site," "Shrink Site," "Delete Site,""Raise Quality," 
  "Lower Quality," or "Set Quality" command is used,
  the command applies to all the selected sites.</p>

- <strong>Raise Quality</strong> - <code>UP</code>:
  <p>When users have selected a site (sites) they can raise the quality
  (qualities) by one point by pushing the up arrow key. If the quality 
  is already at its max (255), this action will not do anything.</p>

- <strong>Lower Quality</strong> - <code>DOWN</code>:
  <p>When users have selected a site (sites) they can lower the quality
  (qualities) by one point by pushing the down arrow key. If the quality 
  is already at its min (0), this action will not do anything.</p>

- <strong>Set Quality</strong> - <code>0-9</code> or <code>BACKSPACE</code> and <code>RETURN</code>:
  <p>When users have selected a site (sites) they can set the quality
  (qualities) by typing any number and pushing <code>ENTER</code>.
  When they start typing, "Set Quality:" with the value to set the
  quality to will appear above the site.
  If the number would go outside the range 0-255, the number is reset
  and only the most recently pushed digit will show up as the value to
  set the quality to. For example, if the user has typed "25" and then
  they type "6," the value will not be "256." It will be "6." The 
  <code>BACKSPACE</code> key also works as expected. If only one digit
  remains and <code>BACKSPACE</code> is pushed, the "Set Quality:" 
  display disappears.</p>

- <strong>Create Site</strong> - <code>c</code>:
  <p>Users can create new sites during the simulation by pressing
  the <code>c</code> key. A new site will appear where the mouse is
  with the default quality (which is set in the Constants.py file).</p>

- <strong>Delete Site</strong> - <code>SLASH</code> or <code>DELETE</code>:
  <p>Users can delete all the selected sites by pressing the <code>/</code> 
  or <code>DELETE</code> key (on some keyboards, the <code>DELETE</code> key
  does not work).</p>

- <strong>Expand Site</strong> - <code>EQUALS (PLUS)</code>:
  <p>Users can increase the size of the selected sites by pressing the 
  <code>=</code> (<code>+</code>) key.</p>

- <strong>Shrink Site</strong> - <code>MINUS</code>:
  <p>Users can decrease the size of the selected sites by pressing the 
  <code>-</code> key.</p>

- <strong>Move Site</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEMOTION</code>,
  <code>MOUSEBUTTONUP</code>:
  <p>Users can move sites by clicking them with the mouse, dragging 
  them to a new location, and releasing the mouse button.</p>

- <strong>Set Check Point</strong> - <code>W</code>:
  <p>Users can tell agents where to go on the way to their destination
  before using the "Command Agents to Go" command by pressing <code>w</code>.</p>

- <strong>Command Agents to Go</strong> - <code>SPACE</code> or <code>RIGHT_CLICK</code>:
  <p>Users can set a point where all agents who stop at the selected site must
  go after arriving by selecting the site and pushing the <code>SPACE</code>
  bar with the mouse in the position the agents should go to.</p>

- <strong>Command Agents to Be Assigned</strong> - <code>a</code>:
  <p>Users can set a site that all agents who stop at the selected site will
  be assigned to after arriving by selecting the site and pushing the <code>a</code>
  key with the mouse positioned over the site the agents should be assigned to.</p>

- <strong>Command Agents to Avoid Area</strong> - <code>Z</code>:
  <p>Users can tell the agents who visit a site to avoid an area by pressing the
  <code>Z</code> key with their cursor over the center of the area to avoid
  while the site is selected.</p>

- <strong>Unselect Sites</strong> - <code>ESC</code>:
  <p>Users can unselect all sites by pressing the escape button.</p>

- <strong>Cancel Site Commands</strong> - <code>PERIOD</code>:
  <p>Users can cancel all selected sites' commands by pressing the 
  <code>.</code> key.</p>

### Other Controls

- <strong>Pause</strong> - <code>p</code>:
  <p>Users can pause and unpause the simulation by pressing the <code>p</code> key. 
  While the simulation is paused, all user interactions are still possible.
  However, agents who are told to go somewhere (see "Move Agent" above) will
  not start moving until the simulation resumes.</p>

- <strong>Zoom In</strong> - <code>CTRL</code> + <code>MOUSEWHEEL</code>:
  <p>Users can zoom in by holding down <code>CTRL</code> and scrolling up on the 
  mouse. If they have a mouse pad, zooming in works on that too.</p>
- <strong>Zoom Out</strong> - <code>CTRL</code> + <code>MOUSEWHEEL</code>:
  <p>Users can zoom out by holding down <code>CTRL</code> and scrolling down on the 
  mouse. If they have a mouse pad, zooming out works on that too.</p>
- <strong>Move Camera</strong> - <code>MOUSEMOTION</code>:
  <p>Users can move the view of the camera by moving the mouse to the edge of the screen
  in the direction they want the camera to move.</p>
- <strong>Lock Screen</strong> - <code>CAPS</code>:
  <p>Users can lock the screen so that the screen cannot be moved or zoomed by pressing the 
  <code>CAPS LOCK</code> key. The screen can be unlocked the same way.</p>

- <strong>Show/Hide Options</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEBUTTONUP</code> or <code>o</code>:
  <p>Users can view the options mentioned above ("Agent Controls" and "Site Controls")
  by clicking on the gray box next to the words "Show Options:" on the screen, or by 
  pressing the <code>o</code> key while the simulation is paused. A list of the
  options described in "Agent Controls" and "Site Controls" will then be displayed in
  the middle of the screen. These controls still work while the Options Menu is showing,
  but it is difficult to see most of the screen. The options menu can be disabled the
  same way it is enabled.</p>

- <strong>Enable/Disable Agent Selection</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can enable or disable the selection of agents by clicking on the blue/gray box next to the words
  "Select Agents:" on the screen. When the box is blue, agent selection is enabled. When the box is gray,
  it is disabled. Disabling agent selection can be useful when a user wants to do something like deleting
  a site without deleting agents they accidentally selected.</p>

- <strong>Enable/Disable Site Selection</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can enable or disable the selection of sites by clicking on the blue/gray box next to the words
  "Select Sites:" on the screen. When the box is blue, site selection is enabled. When the box is gray,
  it is disabled. Disabling site selection can be useful when a user wants to do something like deleting
  agents without deleting sites they accidentally selected.</p>

- <strong>Enable/Disable Agents' Site Selection</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can enable or disable the selection of the site that belongs to the selected agents by clicking 
  on the blue/gray box next to the words "Select Agents Sites:" on the screen. When the box is blue, agents site 
  selection is enabled. When the box is gray, it is disabled. Enabling agents site selection can be useful when 
  a user wants to do something like see which site an agent is assigned to without looking at the information
  on the side of the screen. Note that the agents' site will only be selected if all the selected agents are assigned
  to the same site.</p>

- <strong>Enable/Disable Sites' Agents Selection</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can enable or disable the selection of the agents that belong to the selected sites by clicking 
  on the blue/gray box next to the words "Select Sites Agents:" on the screen. When the box is blue, sites agents 
  selection is enabled. When the box is gray, it is disabled. Enabling sites agents selection can be useful when 
  a user wants to do something like see which agents are assigned to the selected sites.</p>

- <strong>Enable/Disable Site Commands</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can enable or disable site commands by clicking on the blue/gray box next 
  to the words "Command Site Agents:" on the screen. When the box is blue, site commands 
  are enabled. When the box is gray, they is disabled.</p>

- <strong>Move Box</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEMOTION</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can move the display boxes around the screen by clicking on them and dragging
  them to where they want them to be.</p>

- <strong>Expand/Shrink Box</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEMOTION</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can expand or shrink some box-shaped displays on the screen during the 
  simulation by left-clicking on a side or corner of it and dragging it around.</p>

- <strong>Scroll Box</strong> - <code>MOUSEWHEEL</code>:
  <p>Users can scroll up or down on some box displays to bring words that are off the screen onto the 
  screen. An arrow will be drawn on the side of the box pointing in the direction of the words that 
  are not being displayed if any.</p>

- <strong>Show Next Page of Options</strong> - <code>RIGHT</code> or <code>MOUSEBUTTONDOWN</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can view the second page of options by pushing the right arrow key or clicking on "NEXT"
  while the simulation is paused and the option menu is showing.</p>

- <strong>Show Previous Page of Options</strong> - <code>LEFT</code> or <code>MOUSEBUTTONDOWN</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can view the first page of options by pushing the left arrow key or clicking on "PREVIOUS"
  while the simulation is paused and the option menu is showing.</p>
