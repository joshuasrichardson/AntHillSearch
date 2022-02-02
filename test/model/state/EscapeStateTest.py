import unittest

import numpy as np

import Utils
from config.Config import MIN_AVOID_DIST
from model.states.EscapeState import EscapeState
from model.states.SearchState import SearchState


class MockAgent:
    def __init__(self, angle, pos):
        self.angle = angle
        self.pos = pos
        self.speed = 3
        self.target = Utils.getNextPosition(self.pos, self.speed, self.angle)
        self.state = None

    def setAngle(self, angle):
        self.angle = angle

    def getAngle(self):
        return self.angle

    def getPosition(self):
        return self.pos


class EscapeStateTest(unittest.TestCase):

    def test_get_enemy_position_from_down_left(self):
        angle = np.pi / 4
        pos = [0, 0]
        enemyPositions = [[0, MIN_AVOID_DIST - 2], [MIN_AVOID_DIST - 2, 0]]
        expectedPos = [MIN_AVOID_DIST / 2 - 1, MIN_AVOID_DIST / 2 - 1]
        expectedAngle = np.pi / 4
        expectedDiff = -np.pi  # This is because it is called once in the constructor, and we are calling it again below
        self.run_enemy_pos_test(angle, pos, enemyPositions, expectedPos, expectedAngle, expectedDiff)

    def test_get_enemy_position_from_right(self):
        angle = np.pi
        pos = [0, 0]
        a = (MIN_AVOID_DIST - 2) * (np.sqrt(2) / 2)
        enemyPositions = [[-a, a], [-a, -a]]
        expectedPos = [-a, 0]
        expectedAngle = np.pi
        expectedDiff = -np.pi  # This is because it is called once in the constructor, and we are calling it again below
        self.run_enemy_pos_test(angle, pos, enemyPositions, expectedPos, expectedAngle, expectedDiff)

    def run_enemy_pos_test(self, angle, pos, enemyPositions, expectedPos, expectedAngle, expectedDiff):
        self.agent = MockAgent(angle, pos)
        self.agent.state = EscapeState(self.agent, SearchState(self.agent), enemyPositions)
        actualPos, actualAngle, actualDiff = self.agent.state.getEnemyLocation(enemyPositions)
        self.assertEqual(expectedPos, actualPos, f"expected pos: {expectedPos}, got: {actualPos}")
        self.assertEqual(expectedAngle, actualAngle, f"expected angle: {Utils.toDegrees(expectedAngle)}, "
                                                     f"got: {Utils.toDegrees(actualAngle)}")
        self.assertAlmostEqual(expectedDiff, actualDiff, 2, f"expected diff: {Utils.toDegrees(expectedDiff)}, "
                                                            f"got: {Utils.toDegrees(actualDiff)}")


if __name__ == '__main__':
    unittest.main()
