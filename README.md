# Ant Hill Search Simulation

##Overview

- Running the Program
- Parameters
- Controls

## Running the Program

1. Using the terminal, navigate to the <code>AntHillSearch/</code>
  directory on your computer (It should be the same directory 
  this <code>README.md</code> file is in).
2. Set parameters in the <code>main</code> function in 
   <code>colony.Colony.py</code> (See "Parameters" section 
   for more detail).
3. Enter <code>python colony/Colony.py</code> in the terminal.

##Parameters

The default parameters can be found in <code>Constants.py</code>.
Most of these can be overridden by passing something else in as 
a parameter in the <code>colony.Colony.py</code>'s <code>main</code>
 method. Important parameters to know about include:

###<code>ColonySimulation()</code>

- numAgents: The total number of agents at the start of the simulation. 
  If the user never adds or removes any agents, the total number of 
  agents will not change, but if they add or remove agents, the total 
  number changes accordingly.
- TODO

###<code>ColonySimulation.addAgents()</code>

- TODO

###<code>ColonySimulation.initializeAgentList()</code>

- TODO

###<code>ColonySimulation.randomizeInitialState()</code>

This method has no parameters, but note that it can only 
be called with the ColonySimulation (not with the 
RecordingPlayer).

## Controls

The controls allow a user to interact with the 
simulation by doing things like telling agents
where to go, creating sites, pausing, etc. These
can be adjusted by changing statements in the 
<code>handleEvent</code> method found in <code>
user.Controls</code> Below is a complete list of
all the controls available right now (There will 
be more to come).

###Agent Controls

- <strong>Select</strong> Agent - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can select agents by clicking on them with the mouse.</p>
- <strong>Wide Select</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEMOTION</code>, 
  <code>MOUSEBUTTONUP</code>:
  <p>Users can select a group of agents by clicking
  somewhere with the mouse, sliding the mouse over the 
  agents they want to select, and releasing the mouse button.</p>
- <strong>Half</strong> - <code>K_h</code>:
  <p>Users can unselect half of the selected agents by pressing the 
  <code>h</code> key.</p>
- <strong>Next Agent</strong> - <code>TODO</code>:
  <p></p>
- <strong>Previous Agent</strong> - <code>TODO</code>:
  <p></p>
- <strong>Speed Up</strong> - <code>TODO</code>:
  <p></p>
- <strong>Slow Down</strong> - <code>TODO</code>:
  <p></p>
- <strong>Move Agent</strong> - <code>TODO</code>:
  <p></p>
- <strong>Assign Agent to Site</strong> - <code>TODO</code>:
  <p></p>
- <strong>Create Agent</strong> - <code>TODO</code>:
  <p></p>
- <strong>Delete Agent</strong> - <code>TODO</code>:
  <p></p>

###Site Controls

- <strong>Select Site</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEBUTTONUP</code>:
  <p>Users can select sites by clicking on them with the mouse.</p>
- <strong>Wide Select</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEMOTION</code>, 
  <code>MOUSEBUTTONUP</code>:
  <p>Users can select a group of sites by clicking
  somewhere with the mouse, sliding the mouse over the sites 
  they want to select, and releasing the mouse button.</p>
- <strong>Next Site</strong> - <code>TODO</code>:
  <p></p>
- <strong>Previous Site</strong> - <code>TODO</code>:
  <p></p>
- <strong>Raise Quality</strong> - <code>TODO</code>:
  <p></p>
- <strong>Lower Quality</strong> - <code>TODO</code>:
  <p></p>
- <strong>Set Quality</strong> - <code>TODO</code>:
  <p></p>
- <strong>Create Site</strong> - <code>TODO</code>:
  <p></p>
- <strong>Delete Site</strong> - <code>TODO</code>:
  <p></p>
- <strong>Expand Site</strong> - <code>TODO</code>:
  <p></p>
- <strong>Shrink Site</strong> - <code>TODO</code>:
  <p></p>
- <strong>Move Site</strong> - <code>MOUSEBUTTONDOWN</code>, <code>MOUSEMOTION</code>, 
  <code>MOUSEBUTTONUP</code>:
  <p>Users can move sites by clicking them with the mouse, dragging 
  them to a new location, and releasing the mouse button.</p>

###Other Controls

Coming soon: Enable and disable agent and site controls so that 
agents assigned to a site aren't deleted when the site is deleted 
if the user doesn't want them to be deleted etc.
