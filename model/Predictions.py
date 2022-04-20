from config.Config import *

class Predictions():

	def __init__(self):
		self.chanceOfSuccess = 50

	def getChanceOfSuccess(self, world, numRounds):
		"""Returns an estimate of the overall probability that the agents will converge to a site
		within the time limit"""
		print(f'world in getChanceSuccess: {world}')
		agentsRemaining = len(world.agentList) - world.numDeadAgents[0]
		highestAgentCount = max(site.agentCount for site in world.siteList if
								world.hubs.count(site) != 1) # The new site with the highest agent count
		percentConverged = (highestAgentCount / agentsRemaining) / CONVERGENCE_FRACTION
		percentRoundsRemaining = (SIM_DURATION - numRounds) / SIM_DURATION

		# chanceOfSuccess = int((((percentConverged * 2) + (percentRoundsRemaining)) * 50) / 1.5)
		chanceOfSuccess = max(percentConverged, percentRoundsRemaining) * 100
		return int(chanceOfSuccess)

	def getTimeRemainingPrediction(self, world, numRounds):
		"""Returns an estimate of the amount of time it will take the agents to converge to a site"""
		agentsRemaining = len(world.agentList) - world.numDeadAgents[0]
		highestAgentCount = max(site.agentCount for site in world.siteList if
								world.hubs.count(site) != 1)  # The new site with the highest agent count
		percentConverged = (highestAgentCount / agentsRemaining) / CONVERGENCE_FRACTION
		percentRoundsElapsed = numRounds / SIM_DURATION

		estimatedTimeRemaining = (1 - max(percentRoundsElapsed, percentConverged)) * 120
		return int(estimatedTimeRemaining)

	def getChanceOfConvergingToSite(self, world, siteIndex):
		"""Returns an estimate of the probability that the agents will converge to an available site"""
		agentsRemaining = len(world.agentList) - world.numDeadAgents[0]
		percentConverged = ((world.siteList[siteIndex].agentCount / agentsRemaining) / CONVERGENCE_FRACTION) * 100
		return int(percentConverged)
