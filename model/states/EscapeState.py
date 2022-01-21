import numpy as np

import Utils
from Constants import ESCAPE_COLOR, ESCAPE, MIN_AVOID_DIST, SEARCH
from model.states.State import State, numToState


class EscapeState(State):

    def __init__(self, agent, prevStateNum, enemyPositions):
        super().__init__(agent)
        self.stateNumber = ESCAPE
        self.prevStateNum = prevStateNum
        self.enemyPositions = enemyPositions
        self.checkTarget()
        self.isTangent = False
        self.setAngle(enemyPositions)

    def checkTarget(self):
        """ If they are trying to go inside the avoid area, just send them out searching instead."""
        if self.agent.target is not None:
            for pos in self.enemyPositions:
                if Utils.isClose(pos, self.agent.target, MIN_AVOID_DIST):
                    self.agent.target = None
                    self.prevStateNum = SEARCH
                    break

    def setAngle(self, enemyPositions):
        enemyPos, enemyAngle, angleDiff = self.getEnemyLocation(enemyPositions)
        enemyDist = Utils.getDistance(self.agent.getPosition(), enemyPos)

        self.isTangent = np.abs(angleDiff - (np.pi / 2)) < np.pi / 16

        if enemyDist < (MIN_AVOID_DIST - self.agent.speed):  # If the agent is inside the avoid circle:
            self.agent.setAngle(enemyAngle - np.pi)  # Turn away from the center of the circle
        else:  # If the agent is on the border of the circle:
            if angleDiff <= 0:  # If the center of the avoid area is to the right of where the agent is headed,
                # Turn left (relative to the center of the area we are avoiding)
                self.agent.setAngle(enemyAngle - np.pi / 2)
            else:
                # Turn right (relative to the center of the area we are avoiding)
                self.agent.setAngle(enemyAngle + np.pi / 2)

    def getEnemyLocation(self, positions):
        agentAngle = self.agent.getAngle()

        pos = positions[0]
        angle = Utils.getAngleFromPositions(self.agent.getPosition(), pos)
        angleDiff = Utils.getAngleDiff(agentAngle, angle)

        if len(positions) > 1:  # If the agent is inside to areas they are supposed to avoid,
            # Get the position of the second area to avoid
            pos2 = positions[1]
            # Get the angle between the agent and the second position to avoid
            angle2 = Utils.getAngleFromPositions(self.agent.getPosition(), pos2)

            # Have the agent avoid the position in the middle of the two areas to avoid.
            pos = Utils.getAveragePos([pos, pos2])
            angle = Utils.getBisector(angle2, angle)
            angleDiff = Utils.getAngleDiff(agentAngle, angle)

        return pos, angle, angleDiff

    def changeState(self, neighborList):
        avoidPlaces = self.agent.getNearbyPlaceToAvoid()
        if (len(avoidPlaces) == 0 or self.isTangent) and self.agentIsFacingTarget():  # If the agent is far enough from the place they are supposed to avoid
            self.agent.setState(numToState(self.prevStateNum, self.agent))  # Go back to their previous state
        else:
            if len(avoidPlaces) == 0:
                avoidPlaces = self.enemyPositions
            else:
                self.enemyPositions = avoidPlaces
            self.setAngle(avoidPlaces)

    def agentIsFacingTarget(self):
        if self.agent.target is None:
            return True

        angle = Utils.getAngleFromPositions(self.agent.getPosition(), self.agent.target)
        angleDiff = Utils.getAngleDiff(self.agent.getAngle(), angle)
        return np.abs(angleDiff) < np.pi / 16

    def toString(self):
        return "ESCAPE"

    def getColor(self):
        return ESCAPE_COLOR