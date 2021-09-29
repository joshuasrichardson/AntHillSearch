# Ant Hill Search Simulation

## Overview

- Introduction
- Running the Program
- Parameters
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
depending on their quality. The bright green sites with fewer 
stripes are the best, and the bright red sites with many 
stripes are the worst. Brownish sites with an average number 
of stripes are somewhere in the middle. Agents are represented 
by smaller copters or ants (depending on the settings) and, when 
they are selected, surrounded by circles with colors representing 
their current phase and state.

### Phases: Levels of Commitment

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
For simulations where there is more than one hub, we added a Converged
phase. This phase was not in the original model, but we added it
so that the user can see which groups of agents still need to find a site.

### States

Agents' phases include At Nest, Search, Lead Forward, Follow,
Transport, Reverse Tandem, and Carried. At Nest means the agent is
at one of the sites (which can include the hub). Search means the
agent is out looking for other sites to evaluate. Lead Forward is 
the state where agents in the Canvasing phase start to recruit other
agents to their site. Follow is where the agent goes with an agent 
in the Lead Forward or Reverse Tandem state to get to another site.
Reverse Tandem happens in the committed phase when an agent leads
other agents from their assigned site to another site they know about. 
From there, both the leader and the follower lead more agents back
to the site they are committed to. Transport also only happens in 
the Committed phase, but with the Transport state, committed agents
pick up agents that are either searching or at a nest, not just at
a nest. The Carried state is where an agent is picked up by another
agent in the Transport state and brought to the transporting agent's
site to evaluate it for themselves.

### References

More details about the phases and states can be found by reading
["An agent-based model of collective nest choice by the ant Temnothorax albipennis"](https://www-sciencedirect-com.erl.lib.byu.edu/science/article/pii/S0003347205002332) 
by Stephen C. Pratt, David J. T. Sumpter, Eamonn B. Mallon, and Nigel R. 
Franks. The model in this Anthill Search program is mostly based on the 
model represented in the "Structure of the Model" section of this paper, b
ut adjustments such as the converged phase and the Go state have been added.

Another useful paper about this topic is found at 
["Nest Site Choices in Social Insects"](https://www-sciencedirect-com.erl.lib.byu.edu/science/article/pii/B9780128096338012620?via%3Dihub) 
I did not find this one till after implementing the model,
but it had useful information about when the ants decide to 
switch from the Canvas phase to the Commit phase.
It also contains a paragraph about factors that make a site good.
We could implement these in the future, but for now, the quality is 
just represented by a number.

### Additional Information

In addition to the states and phases described above, many options for 
user interaction have been added. See the "Parameters" section for 
details about how to change the simulation's set up. See the "Controls"
section for details about how to interact with the simulation while
it is running.

## Running the Program

1. Using the terminal, navigate to the <code>AntHillSearch/</code>
   directory on your computer (It should be the same directory as 
   this <code>README.md</code>).
2. If this is your first time running the program on your machine,
   enter <code>pip install -r requirements.txt</code>
3. To change parameters from the default parameters, set 
   parameters in the <code>main()</code> function in 
   <code>colony.Colony.py</code> (see "Parameters" section 
   for more details) or set which interface you would like to
   use by uncommenting it out and commenting out the others
   (see "Interfaces" section for more details).
4. Enter <code>python Colony.py</code> in the terminal.
5. If desired, try using some user controls while the
   simulation is running (see "Controls" for more details).

## Parameters

The parameters set before the simulation begins can have a big
impact on the set up and behavior of the simulation. The default 
parameters and more information about them can be found in 
<code>Constants.py</code>. Most of these can be overridden by 
passing something else in as a parameter in
<code>Colony.py</code>'s <code>main()</code> method. They are
also overridden by settings set while the program is running
that appear in the <code>display/mainmenu/settings.json</code> file.
Important methods and their parameters to know about are listed 
below.

Using the interfaces mentioned in the "Interfaces" Section below 
is an easy way to change many of these parameters at the same time
to fit the purposes of the interfaces.

### <code>LiveSimulation()</code>               

The constructor for the <code>LiveSimulation</code> class (the class that runs the simulation).
This is an abstract class and cannot be run without implementing a few methods, but the parameters
shown here can be changed in the inheriting classes.

- <code>simulationDuration</code>: Integer that sets the max time of the simulation in seconds. 
  The simulation can end before this time runs out if all the agents converge to the same site.
  
- <code>numHubs</code>: Integer that sets the number of hubs.

- <code>numSites</code>: Integer that sets the initial number of sites, not including the hubs. More sites
  can optionally be added or removed during the simulation (see "Site Controls" below).
  
- <code>useRestAPI</code>: Boolean that decides whether to send information from the hubs to the Rest API.
  Note that when running the simulation with this value set to True, the RestAPI needs to be started before 
  the simulation is started.

- <code>shouldRecord</code>: Boolean that decides whether the simulation is recorded to the recording.json file.
 
- <code>convergenceFraction</code>: Float that sets the percentage of agents that need to be assigned to 
  one site before the simulation will end.
  
- <code>hubLocations</code>: List of ordered pairs that sets the initial positions of the agents' original homes.
  
- <code>hubRadii</code>: List of Integers that sets the sizes of the agents' original homes.
  
- <code>hubAgentCounts</code>: List of Integers that sets the numbers of agents to start at the hubs.
  
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
  
- <code>hubCanMove</code>: Boolean that determines whether the user can move the hub from its
  starting position.
  
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
  
- <code>findSitesEasily</code>: Boolean that determines whether agents know where their sites
  are even after they have been moved.
  
- <code>commitSpeedFactor</code>: Number that determines how much faster agents get when they 
  commit.
  
  
### <code>RecordingPlayer()</code>

Constructor for the <code>RecordingPlayer</code> class. This class can be used instead of the 
<code>LiveSimulation</code> to replay a previously recorded simulation from the recording.json
file.

This method has no parameters because everything is determined by the recording.json file.


### <code>Simulation.initializeAgentList()</code>

Generates a list of agents with the specified attributes.

This method must be called before <code>runSimulation()</code> is called 
or else the simulation will end immediately because there will not be
any agents.

- <code>hubAgentCounts</code>: A list of integers that set the number of agents at each hub 
  at the start of the simulation. If a hub is not assigned a number of agents here, it will
  be given a random number of agents.
  
  
### <code>LiveSimulation.randomizeInitialState()</code>

Assigns each agent in the simulation a random site to start from.

This method has no parameters. Also, note that it cannot be called with the 
RecordingPlayer.


### <code>LiveSimulation.addAgents()</code>

Adds agents to the simulation (in addition to the "numAgents" specified in the constructor).
These agents can be given specific starting states, phases, locations, and assignments.

- <code>numAgents</code> (required): Integer to set the number of agents to create with the specified state, 
  phase, assignedSite, and startingPosition.
  
- <code>state</code> (required): State that the agents start in.
  
- <code>phase</code> (required): Integer to set the phase that the agents start in.
  
- <code>assignedSiteIndex</code> (required): Integer that sets the agents' assigned site to the 
  nth site in the site list.
  
- <code>startingPosition</code>: Ordered pair that sets where the agents start in the simulation.

Note that this method can not be used with the RecordingPlayer.

## Interfaces

There are currently 4 different interfaces available as listed below.

For a more game-like simulation, you can make a <code>StartUpDisplay</code>
object and pass an interface into the constructor. To play this one,
call <code>run()</code> on the <code>StartUpDisplay</code> object.

### EngineerInterface

This interface is the one that shows the most information. When
there is a choice between drawing something and not drawing it,
this interface usually draws it. It also provides accurate info
about where agents are and site values. This interface also
allows more user controls than the other interfaces. All parameters
can still be manually set by the user as is shown for the 
LiveSimulation in the "Parameters" section above, but different
default values apply.

### UserInterface

This interface does not show as much information as the Engineering 
Interface. Agents and their paths are only drawn when they are close 
to the hub, and sites drawn only reflect what the agents that have
returned to the hub have estimated about them. This interface allows
some user controls, but they are limited to what can be done from the 
hub. All parameters can still be manually set by the user as is shown 
for the LiveSimulation in the "Parameters" section above, but 
different default values apply.

### EmpiricalTestingInterface

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
have no effect on the simulation because all the information comes
from the <code>recording.json</code> file.

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
  they can see information about the next agent in the list of agents
  by pushing the right arrow key. This action will also move the outer 
  red circle from the current agent to the next agent so it always
  surrounds the agent whose information appears on the left side of 
  the screen.</p>

- <strong>Previous Agent</strong> - <code>LEFT</code>:
  <p>When users have selected a group of agents with "Wide Select,"
  they can see information about the previous agent in the list of agents
  by pushing the left arrow key. This action will also move the outer 
  red circle from the current agent to the previous agent so it always
  surrounds the agent whose information appears on the left side of 
  the screen.</p>

- <strong>Speed Up</strong> - <code>f</code>:
  <p>Users can cause the agents to move faster by pushing the 
  <code>f</code> key. This is not the same as fast forwarding 
  the simulation because the time still runs at the same speed.
  It is just a way to make each agent move faster.</p>

- <strong>Slow Down</strong> - <code>s</code>:
  <p>Users can cause the agents to move slower by pushing the 
  <code>s</code> key. This is not the same as slowing the whole 
  simulation down because the time still runs at the same speed.
  It is just a way to make each agent move slower.</p>

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

- <strong>Next Site</strong> - <code>RIGHT</code>:
  <p>When users have selected a group of sites with "Wide Select,"
  they can see information about the next site in the list of sites
  by pushing the right arrow key.</p>

- <strong>Previous Site</strong> - <code>LEFT</code>:
  <p>When users have selected a group of sites with "Wide Select,"
  they can see information about the previous site in the list of sites
  by pushing the left arrow key.</p>

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

- <strong>Command Agents to Go</strong> - <code>SPACE</code> or <code>RIGHT_CLICK</code>:
  <p>Users can set a point where all agents who stop at the selected site must
  go after arriving by selecting the site and pushing the <code>SPACE</code>
  bar with the mouse in the position the agents should go to.</p>

- <strong>Command Agents to Be Assigned</strong> - <code>a</code>:
  <p>Users can set a site that all agents who stop at the selected site will
  be assigned to after arriving by selecting the site and pushing the <code>a</code>
  key with the mouse positioned over the site the agents should be assigned to.</p>

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

- <strong>Zoom In</strong> - <code>CTRL</code> +  <code>MOUSEWHEEL</code>:
  <p>Users can zoom in by holding down <code>CTRL</code> and scrolling up on the 
  mouse. If they have a mouse pad, zooming in works on that too.</p>
  
- <strong>Zoom Out</strong> - <code>CTRL</code> +  <code>MOUSEWHEEL</code>:
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
  <p>Users can enable or disable site commands by clickingon the blue/gray box next 
  to the words "Command Site Agents:" on the screen. When the box is blue, site commands 
  are enabled. When the box is gray, they is disabled.</p>

- <strong>Show/Hide Graphs</strong> - <code>g</code>:
  <p>Users can have the graphs on the left side of the screen appear or disappear by pressing the <code>G</code> key.</p>

- <strong>Expand/Shrink Command History Box</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEMOTION</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can expand or shrink the box that shows a history of all the commands executed throughout the 
  simulation by left clicking on the top of it and dragging it up or down. This will cause more or less
  commands to be displayed.</p>

- <strong>Scroll Command History Box</strong> - <code>MOUSEWHEEL</code>:
  <p>Users can view commands executed earlier by scrolling down and commands executed more recently
  by scrolling up. When there are more executed commands that are not already displayed on the screen,
  an arrow will be drawn on the side of the box pointing in the direction of the commands that are not
  being displayed.</p>

- <strong>Show Next Page of Options</strong> - <code>RIGHT</code> or <code>MOUSEBUTTONDOWN</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can view the second page of options by pushing the right arrow key or clicking on "NEXT"
  while the simulation is paused and the option menu is showing.</p>

- <strong>Show Previous Page of Options</strong> - <code>LEFT</code> or <code>MOUSEBUTTONDOWN</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can view the first page of options by pushing the left arrow key or clicking on "PREVIOUS"
  while the simulation is paused and the option menu is showing.</p>
