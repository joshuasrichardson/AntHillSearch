import json

import numpy as np

from Constants import CONFIG_FILE_NAME, CONFIG_KEYS, COPY_FROM_CONFIG, SETTING_KEYS
from config import Config  # This is important for copyJsonToConfig.
from config.Config import *  # This is important for resetConfig.


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


def copyJsonToConfig():
    try:
        with open(CONFIG_FILE_NAME, 'r') as file:
            data = json.load(file)
        for i, key in enumerate(CONFIG_KEYS):
            if key in data:
                try:
                    exec(f"Config.{CONFIG_KEYS[i]} = {data[key]}")
                except NameError:
                    exec(f"Config.{CONFIG_KEYS[i]} = \"{data[key]}\"")
    except FileNotFoundError:
        print(f"File '{CONFIG_FILE_NAME}' Not Found")
        with open(f'{CONFIG_FILE_NAME}', 'w'):
            print(f"Created '{CONFIG_FILE_NAME}'")
    except json.decoder.JSONDecodeError:
        print(f"File '{CONFIG_FILE_NAME}' is empty")


def setConfig(currentConfigFileName, copy=True):
    """ Copy the current trial's settings to the settings file that will be used in the simulation """
    currentSettings = open(CONFIG_FILE_NAME, 'r')
    current = json.load(currentSettings)
    currentSettings.close()
    with open(currentConfigFileName, 'r') as trialFile, open(CONFIG_FILE_NAME, 'w') as currentSetting:
        trial = json.load(trialFile)
        if copy:
            for setting in COPY_FROM_CONFIG:
                trial[setting] = current[setting]
        json.dump(trial, currentSetting)


def resetConfig():
    for key in SETTING_KEYS:
        try:
            exec(f"Config.{key} = {eval(key)}")
        except NameError:
            exec(f"Config.{key} = \"{eval(key)}\"")
