import numpy as np


def getAngleDiff(angle1, angle2):
    return (angle1 - angle2 + 3 * np.pi) % (2 * np.pi) - np.pi


def getAngleFromPositions(fromPos, toPos):
    return np.arctan2(toPos[1] - fromPos[1], toPos[0] - fromPos[0])


def getAverage(numbers):
    return sum(numbers) / len(numbers)


def getBisector(angle1, angle2):
    avgAngle = getAverage([angle1, angle2])
    if (angle1 < 0 < angle2 or angle2 < 0 < angle1) and np.abs(angle1 - angle2) > np.pi:
        avgAngle += np.pi
    return avgAngle


def toDegrees(angle):
    return angle * 180 / np.pi


def getAveragePos(positions):
    xs = []
    ys = []
    for pos in positions:
        xs.append(pos[0])
        ys.append(pos[1])
    return [getAverage(xs), getAverage(ys)]


def getDistance(pos1, pos2):
    return np.sqrt(np.square(np.abs(pos1[0] - pos2[0])) + np.square(np.abs(pos1[1] - pos2[1])))


def getNextPosition(pos, speed, angle):
    return [int(np.round(float(pos[0]) + speed * np.cos(angle))), int(np.round(float(pos[1]) + speed * np.sin(angle)))]


def isClose(pos1, pos2, closeDistance):
    return getDistance(pos1, pos2) <= closeDistance
