import numpy as np

from config.Config import MAX_SEARCH_DIST
from display.simulation.ObstacleDisplay import getObstacleImage


class Obstacle:
    """ Harmless rocks that get in the way of agents while they walk around the world """

    def __init__(self, world, pos=None):
        """ world - the world where the obstacle is located
        pos - the x, y coordinates on the screen where the top left corner of the obstacle is """
        self.world = world
        if pos is None:
            self.pos = [world.getHubs()[0].getPosition()[0] + (np.random.randint(-MAX_SEARCH_DIST, MAX_SEARCH_DIST)),
                        world.getHubs()[0].getPosition()[1] + (
                            np.random.randint(-MAX_SEARCH_DIST, MAX_SEARCH_DIST))]  # Where the obstacle will be placed
        else:
            self.pos = pos
        self.obstacleHandle = getObstacleImage(self.pos)  # Image on screen representing a obstacle
        self.obstacleRect = self.obstacleHandle.get_rect()  # Rectangle around the obstacle to help track collisions
        self.obstacleRect.centerx = self.pos[0]  # Horizontal center of the obstacle
        self.obstacleRect.centery = self.pos[1]  # Vertical center of the obstacle
        self.angle = np.random.uniform(0, 2 * np.pi)  # The direction the obstacle is facing in radians
        self.agentNeighbors = []  # Agents colliding with the obstacle
        self.oldNeighborList = []  # Agents that collided with the obstacle in the previous round

    def getAgentNeighbors(self):
        return self.agentNeighbors

    def setAgentNeighbors(self, agentNeighbors):
        self.agentNeighbors = agentNeighbors

    def getOldNeighborList(self):
        return self.oldNeighborList

    def setOldNeighborList(self, oldNeighborList):
        self.oldNeighborList = oldNeighborList

    def getRect(self):
        return self.obstacleRect

    def setPosition(self, x, y):
        self.obstacleRect.centerx = x
        self.obstacleRect.centery = y
        self.pos = list([x, y])

    def setAngle(self, angle):
        self.angle = angle

    def changeAgentAngle(self, agent, sideOfObstacle):
        """ Changes the angle of the agent based on what side of the obstacle it collides with """
        if sideOfObstacle == "left":
            angleDiff = agent.getAngle() - (np.pi / 2)
            if angleDiff > 0:
                agent.setAngle(3 * np.pi / 2)  # Turn up
            else:
                agent.setAngle(np.pi / 2)  # Turn down
        elif sideOfObstacle == "top":
            angleDiff = agent.getAngle() - (np.pi)
            if angleDiff < 0:
                agent.setAngle(np.pi)  # Turn left
            else:
                agent.setAngle(2 * np.pi)  # Turn right
        elif sideOfObstacle == "right":
            angleDiff = agent.getAngle() - (np.pi / 2)
            if angleDiff < 0:
                agent.setAngle(3 * np.pi / 2)  # Turn up
            else:
                agent.setAngle(np.pi / 2)  # Turn down
        elif sideOfObstacle == "bottom":
            angleDiff = agent.getAngle() - (np.pi)
            if angleDiff > 0:
                agent.setAngle(np.pi)  # Turn left
            else:
                agent.setAngle(2 * np.pi)  # Turn right

    def getSideOfObstacle(self, agent):
        """Determines which side of the obstacle an agent collided with"""
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dirNames = ["left", "right", "top", "bottom"]

        dx = agent.getRect().centerx - self.obstacleRect.centerx
        dy = agent.getRect().centery - self.obstacleRect.centery

        max_dir = max([i for i in range(len(direction))], key=lambda i: dx * direction[i][0] + dy * direction[i][1])
        return dirNames[max_dir]

    def obstruct(self):
        """Obstructs an agent's path and forces the agent to find its way around the obstacle"""
        for agent in self.agentNeighbors:
            if agent.getRect().colliderect(self.obstacleRect):
                if not agent.getPrevRect().colliderect(
                        self.obstacleRect):  # If the agent is colliding with obstacle for first time
                    agent.angleBeforeObstacle = agent.getAngle()
                else:
                    agent.setAngle(agent.angleBeforeObstacle)

                sideOfObstacle = self.getSideOfObstacle(agent)
                self.changeAgentAngle(agent, sideOfObstacle)
