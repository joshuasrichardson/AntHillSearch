import numpy as np

from config import Config
from config.Config import MAX_SEARCH_DIST
from display.RockDisplay import getRockImage

class Rock:
	def __init__(self, world, pos=None):
		self.world = world
		if pos is None:
			self.pos = [world.getHubs()[0].getPosition()[0] + (np.random.randint(-MAX_SEARCH_DIST, MAX_SEARCH_DIST)),
						world.getHubs()[0].getPosition()[1] + (np.random.randint(-MAX_SEARCH_DIST, MAX_SEARCH_DIST))]  # Where the rock will be placed
		else:
			self.pos = pos
		self.rockHandle = getRockImage(self.pos)  # Image on screen representing a rock
		self.rockRect = self.rockHandle.get_rect()  # Rectangle around the rock to help track collisions
		self.rockRect.centerx = self.pos[0]  # Horizontal center of the rock
		self.rockRect.centery = self.pos[1]  # Vertical center of the rock
		self.angle = np.random.uniform(0, 2 * np.pi)  # The direction the rock is facing in radians

	def getRect(self):
		return self.rockRect

	def setPosition(self, x, y):
		self.rockRect.centerx = x
		self.rockRect.centery = y
		self.pos = list([x, y])

	def setAngle(self, angle):
		self.angle = angle

	def obstruct(self, agentList):
		for agent in agentList:
			agent.angle += 90