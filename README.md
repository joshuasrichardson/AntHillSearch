# Ant Hill Search Simulation

## Overview

- Introduction
- Running the Program
- Parameters
- Controls

## Introduction

This program is a simulation of how ants find a new home
after their previous home has been destroyed. Agents (the 
ants who go out searching for a new home) go through various
levels of commitment (referred to as phases) as well as various
states on their way to reaching their new home. Their goal is 
to converge to the site with the highest quality (to solve the 
best of N problem).

In the simulation, the hub (the agents' original home) is 
represented by a black circle, and the other sites are 
represented by circles with different shades of red or green
depending on their quality. The bright green sites are the best, 
and the bright red sites are the worst. Brownish sites are 
somewhere in the middle. Agents are represented by smaller 
circles which have optional colors representing their current 
phase and state.

Agents start out in the Explore phase, where they have no 
knowledge of any site beside the hub. When they come to a new 
site, they enter the Assess phase, where they initially accept 
or reject the site. If they reject the site, they stay in the 
Assess phase and go look for other sites. If they accept it, 
they enter the Canvasing phase. The Canvasing phase is where 
they start recruiting other agents to their assigned site. When 
a quorum has met at a site, in other words if enough agents have 
been assigned to the same site, these agents will enter the 
Committed phase where their recruiting becomes faster.

Agents' phases include At Nest, Search, Lead Forward, Follow,
Transport, Reverse Tandem, and Carried. At Nest means the agent is
at one of the sites (which can include the hub). Search means the
agent is out looking for other sites to evaluate. Lead Forward is 
the state where agents in the Canvasing phase start to recruit other
agents to their site. Follow is where the agent goes with an agent 
in the Lead Forward or Reverse Tandem state to get to another site.
Reverse Tandem happens in the committed phase when an agent leads
other agents from the site they are committed to to another site that the
leader knows about, and from there, they each lead more agents back
to the site they are committed to. Transport also only happens in 
the Committed phase, but with the Transport state, committed agents
pick up agents that are either searching or at a nest, not just at
a nest. The Carried state is where an agent is picked up by another
agent in the Transport state and brought to the transporting agent's
site to evaluate it for themselves.

More details about the phases and states can be found by reading
["An agent-based model of collective nest choice by the ant Temnothorax albipennis"](https://www-sciencedirect-com.erl.lib.byu.edu/science/article/pii/S0003347205002332) 
by Stephen C. Pratt, David J. T. Sumpter, Eamonn B. Mallon, and Nigel R. 
Franks. The model in this program is based mostly on the model represented in the 
"Structure of the Model" section of this paper.

In addition to the states and phases described above, many options for 
user interaction have been added. See the "Parameters" section for 
details about how to change the simulation's set up. See the "Controls"
section for details about how to interact with the simulation while
it is running.

## Running the Program

1. Using the terminal, navigate to the <code>AntHillSearch/</code>
   directory on your computer (It should be the same directory 
   this <code>README.md</code> file is in).
2. If this is your first time running the program on your machine,
   enter <code>pip install -r requirements.txt</code>
3. To change parameters from the default parameters, set 
   parameters in the <code>main()</code> function in 
   <code>colony.Colony.py</code> (see "Parameters" section 
   for more details).
4. Enter <code>python colony/Colony.py</code> in the terminal.
5. If desired, try using some of the user controls while the
   simulation is running (see "Controls" for more details).

## Parameters

The parameters set before the simulation begins can have a big
impact on the set up and behavior of the simulation. The default 
parameters and more information about them can be found in 
<code>Constants.py</code>. Most of these can be overridden by 
passing something else in as a parameter in
<code>colony.Colony.py</code>'s <code>main()</code> method. 
Important methods and their parameters to know about are listed 
below.

### <code>ColonySimulation()</code>

The constructor for the <code>ColonySimulation</code> class (the class that runs the simulation).

- <code>simulationDuration</code>: Integer that sets the max time of the simulation in seconds. 
  The simulation can end before this time runs out if all the agents converge to the same site.
  
- <code>numSites</code>: Integer that sets the initial number of sites, not including the hub. More sites
  can optionally be added or removed during the simulation (see "Site Controls" below).
  
- <code>shouldReport</code>: Boolean that decides whether information about the hub is sent to a Rest API.
  
- <code>shouldRecord</code>: Boolean that decides whether the simulation is recorded to the recording.json file.
  
- <code>shouldDraw</code>: Boolean that decides whether the simulation is drawn onto the screen.
  
- <code>convergenceFraction</code>: Float that sets the percentage of agents that need to be assigned to 
  one site before the simulation will end.
  
- <code>hubLocation</code>: Ordered pair that sets the initial position of the agents' original home.
  
- <code>hubRadius</code>: Integer that sets the size of the agents' original home.
  
- <code>hubAgentCount</code>: Integer that sets the number of agents to start at the hub.
  
- <code>sitePositions</code>: List of ordered pairs that set positions for the sites. Each site that
  is not given a position here will be assigned a random position.
  
- <code>siteQualities</code>: List of integers that set the qualities of the sites. Each site that
  is not given a quality here will be assigned a random quality.
  
- <code>siteRadii</code>: List of integers that set the sizes of the sites. Each site that
  is not given a size here will be assigned a random size.
                 
- <code>siteNoCloserThan</code>: Integer that sets the closest distance a randomly assigned 
  site can be to the hub at the start of the simulation. This is overridden by
  positions that users set with <code>sitePositions</code> as well as the "Move
  Site" command (see "Site Controls" below).
  
- <code>siteNoFartherThan</code>: Integer that sets the farthest distance a randomly assigned 
  site can be from the hub at the start of the simulation. This is overridden by
  positions that users set with <code>sitePositions</code> as well as the "Move
  Site" command (see "Site Controls" below).
  
### <code>RecordingPlayer()</code>

Constructor for the <code>RecordingPlayer</code> class. This class can be used instead of the 
<code>ColonySimulation</code> to replay a previously recorded simulation from the recording.json
file.

This method has no parameters because everything is determined by the recording.json file.

### <code>ColonySimulation.initializeAgentList()</code>

Generates a list of agents with the specified attributes.

This method must be called before <code>runSimulation()</code> is called 
or else the simulation will end immediately because there will not be
any agents.

- <code>numAgents</code>: The total number of agents at the start of the simulation. 
  If the user never adds or removes any agents, the total number of 
  agents will not change, but if they add or remove agents, the total 
  number changes accordingly.
  
- <code>homogenousAgents</code>: Boolean that when True sets all the agents attributes
  to be the same (these values are the max values of each parameter below) 
  and when False sets values somewhere in the ranges specified by the parameters below.
  
- <code>minSpeed</code>: Integer that sets the slowest an agent can move on the screen.
                            
- <code>maxSpeed</code>: Integer that sets the fastest an agent can move on the screen.
  
- <code>minDecisiveness</code>: Integer that influences how long the least decisive agent 
  takes to assess a site. Lower numbers take longer.
  
- <code>maxDecisiveness</code>: Integer that influences how long the most decisive agent 
  takes to assess a site. Lower numbers take longer.
                            
- <code>minNavSkills</code>: Integer that influences how likely the least oriented agent 
  is to get lost. Higher numbers make the agents get lost easier.
  
- <code>maxNavSkills</code>: Integer that influences how likely the most oriented agent 
  is to get lost. Higher numbers make the agents get lost easier.
  
- <code>minEstAccuracy</code>: Integer that influences how close the least accurate agent's 
  site assessments will be. Higher numbers make the agents' estimations farther away from
  the sites' actual qualities.
  
- <code>maxEstAccuracy</code>: Integer that influences how close the most accurate agent's 
  site assessments will be. Higher numbers make the agents' estimations farther away from
  the sites' actual qualities.
  
- <code>maxSearchDist</code>: Integer representing the farthest distance agents can go away 
  from their assigned site or the hub before they are forced to come a little closer to their 
  assigned site or the hub.

### <code>ColonySimulation.randomizeInitialState()</code>

Assigns each agent in the simulation a random site to start from.

This method has no parameters, but note that it can only 
be called with the ColonySimulation (not with the 
RecordingPlayer).

### <code>ColonySimulation.addAgents()</code>

Adds agents to the simulation (in addition to the "numAgents" specified in the constructor).
These agents can be given specific starting states, phases, locations, and assignments.

- <code>numAgents</code> (required): Integer to set the number of agents to create with the specified state, 
  phase, assignedSite, and startingPosition.
  
- <code>state</code> (required): State that the agents start in.
  
- <code>phase</code> (required): Integer to set the phase that the agents start in.
  
- <code>assignedSiteIndex</code> (required): Integer that sets the agents' assigned site to the 
  nth site in the site list.
  
- <code>startingPosition</code>: Ordered pair that sets where the agents start in the simulation.

Note that this method can only 
be called with the ColonySimulation
(not with the RecordingPlayer).

## Controls

The controls allow a user to interact with the 
simulation by doing things like telling agents
where to go, creating sites, pausing, etc. These
can be adjusted by changing statements in the 
<code>handleEvent</code> method found in <code>
user.Controls</code> Below is a complete list of
all the controls available right now (There will 
be more to come).

### Agent Controls

- <strong>Select Agent</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can select agents by clicking on them with the mouse. 
  The selected agent's information will then show up on the side
  of the screen, and a circle will be drawn around the agent to 
  help the user keep track of where it is. Selected agents can also
  be told where to go, assigned to a site, or deleted (see "Move Agent,"
  "Assign Agent to Site," and "Delete Agent" below).</p>
  
- <strong>Wide Select</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEMOTION</code>, 
  <code>MOUSEBUTTONUP</code>:
  <p>Users can select a group of agents by clicking
  somewhere with the mouse, sliding the mouse over the 
  agents they want to select, and releasing the mouse button.
  When a group of agents is selected and the "Move Agent,"
  "Assign Agent to Site," or "Delete Agent" command is used,
  the command applies to all the selected agents.</p>
  
- <strong>Half</strong> - <code>K_h</code>:
  <p>Users can unselect half of the selected agents by pressing the 
  <code>h</code> key. The agent that is surrounded by a red circle and
  whose information shows up on the side of the screen will not be
  unselected by this, but other than that, there is no way to predict
  which agents will be unselected.</p>

- <strong>Next Agent</strong> - <code>K_RIGHT</code>:
  <p>When users have selected a group of agents with "Wide Select,"
  they can see information about the next agent in the list of agents
  by pushing the right arrow key. This action will also move the outer 
  red circle from the current agent to the next agent so it always
  surrounds the agent whose information appears on the left side of 
  the screen.</p>

- <strong>Previous Agent</strong> - <code>K_LEFT</code>:
  <p>When users have selected a group of agents with "Wide Select,"
  they can see information about the previous agent in the list of agents
  by pushing the left arrow key. This action will also move the outer 
  red circle from the current agent to the previous agent so it always
  surrounds the agent whose information appears on the left side of 
  the screen.</p>

- <strong>Speed Up</strong> - <code>K_f</code>:
  <p>Users can cause the agents to move faster by pushing the 
  <code>f</code> key. This is not the same as fast forwarding 
  the simulation because the time still runs at the same speed.
  It is just a way to make each agent move faster.</p>

- <strong>Slow Down</strong> - <code>K_s</code>:
  <p>Users can cause the agents to move slower by pushing the 
  <code>s</code> key. This is not the same as slowing the whole 
  simulation down because the time still runs at the same speed.
  It is just a way to make each agent move slower.</p>

- <strong>Move Agent</strong> - <code>SPACE</code>:
  <p>Users can tell agents where to go by selecting the agents 
  (see "Select Agent" and "Wide Select" above), moving the mouse
  to the position they want the agent to go to, and pushing the
  <code>SPACE</code> bar. All selected agents then keep moving
  toward the indicated spot until they get there. When they arrive, 
  they transition into the Search state.</p>

- <strong>Assign Agent to Site</strong> - <code>K_a</code>:
  <p>Users can assign agents to a site by selecting the agents 
  (see "Select Agent" and "Wide Select" above), moving the mouse
  over the site they want the agent to be assigned to, and pushing the
  <code>a</code> key. All selected agents then keep moving
  toward the indicated site until they get there. When they arrive, 
  they transition into the At Nest state.</p>

- <strong>Create Agent</strong> - <code>K_x</code>:
  <p>Users can create new agents during the simulation by pressing
  the <code>x</code> key. A new agent will appear where the mouse is
  and start moving in a random direction in the Search state.</p>

- <strong>Delete Agents</strong> - <code>K_SLASH</code> or <code>K_DELETE</code>:
  <p>Users can delete all the selected agents by pressing the <code>/</code> 
  or <code>DELETE</code> key (on some keyboards, the <code>DELETE</code> key
  does not work).</p>

### Site Controls

- <strong>Select Site</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can select sites by clicking on them with the mouse. 
  The selected site's information will then show up on the side
  of the screen, and a circle will be drawn around the site to 
  help the user keep track of where it is. Selected sites can also
  be moved, expanded, shrunk, deleted, or have their quality
  increased, decreased, or set to any number between 0 and 255.
  (see "Move Site," "Expand Site," "Shrink Site," "Delete Site,"
  "Raise Quality," "Lower Quqlity," and "Set Quality" below).</p>

- <strong>Wide Select</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEMOTION</code>, 
  <code>MOUSEBUTTONUP</code>:
  <p>Users can select a group of sites by clicking
  somewhere with the mouse, sliding the mouse over the sites 
  they want to select, and releasing the mouse button.
  When a group of sites is selected and the "Move Site," 
  "Expand Site," "Shrink Site," "Delete Site,""Raise Quality," 
  "Lower Quqlity," or "Set Quality" command is used,
  the command applies to all the selected sites.</p>

- <strong>Next Site</strong> - <code>K_RIGHT</code>:
  <p>When users have selected a group of sites with "Wide Select,"
  they can see information about the next site in the list of sites
  by pushing the right arrow key.</p>

- <strong>Previous Site</strong> - <code>K_LEFT</code>:
  <p>When users have selected a group of sites with "Wide Select,"
  they can see information about the previous site in the list of sites
  by pushing the left arrow key.</p>

- <strong>Raise Quality</strong> - <code>K_UP</code>:
  <p>When users have selected a site (sites) they can raise the quality
  (qualities) by one point by pushing the up arrow key. If the quality 
  is already at its max (255), this action will not do anything.</p>

- <strong>Lower Quality</strong> - <code>K_DOWN</code>:
  <p>When users have selected a site (sites) they can lower the quality
  (qualities) by one point by pushing the down arrow key. If the quality 
  is already at its min (0), this action will not do anything.</p>

- <strong>Set Quality</strong> - <code>0-9</code> or <code>BACKSPACE</code> and <code>K_RETURN</code>:
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

- <strong>Create Site</strong> - <code>K_c</code>:
  <p>Users can create new sites during the simulation by pressing
  the <code>c</code> key. A new site will appear where the mouse is
  with the default quality (which is set in the Constants.py file).</p>

- <strong>Delete Site</strong> - <code>K_SLASH</code> or <code>K_DELETE</code>:
  <p>Users can delete all the selected sites by pressing the <code>/</code> 
  or <code>DELETE</code> key (on some keyboards, the <code>DELETE</code> key
  does not work).</p>

- <strong>Expand Site</strong> - <code>K_EQUALS</code>:
  <p>Users can increase the size of the selected sites by pressing the 
  <code>=</code> (<code>+</code>) key.</p>

- <strong>Shrink Site</strong> - <code>K_MINUS</code>:
  <p>Users can decrease the size of the selected sites by pressing the 
  <code>-</code> key.</p>

- <strong>Move Site</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEMOTION</code>, 
  <code>MOUSEBUTTONUP</code>:
  <p>Users can move sites by clicking them with the mouse, dragging 
  them to a new location, and releasing the mouse button.</p>

### Other Controls

- <strong>Pause</strong> - <code>K_p</code>:
  <p>Users can pause and unpause the simulation by pressing the <code>p</code> key. 
  While the simulation is paused, all user interactions are still possible.
  However, agents who are told to go somewhere (see "Move Agent" above) will
  not start moving until the simulation resumes.</p>

- <strong>View Options</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEBUTTONUP</code> or <code>K_o</code>:
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
