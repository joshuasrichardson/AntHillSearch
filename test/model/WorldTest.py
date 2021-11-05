import unittest

import numpy as np

import Constants
from model.World import World


class WorldTest(unittest.TestCase):

    def setUp(self) -> None:
        self.world = World(5, 5, [], [], [], [], [], [])

    def tearDown(self) -> None:
        del self.world
        self.world = None

    def test_hub_generation(self):
        """ Check that all randomly generated hubs are far enough apart from each other. """
        for i in range(4):
            for j in range(i + 1, 4):
                farEnough = (np.abs(self.world.hubs[i].getPosition()[0] - self.world.hubs[j].getPosition()[0]) >= Constants.MAX_SEARCH_DIST) or \
                            (np.abs(self.world.hubs[i].getPosition()[1] - self.world.hubs[j].getPosition()[1]), Constants.MAX_SEARCH_DIST)
                self.assertTrue(farEnough)


if __name__ == '__main__':
    unittest.main()
