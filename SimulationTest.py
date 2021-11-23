import time
import unittest

import pygame

from interface.EmpiricalTestingInterface import EmpiricalTestingInterface
from interface.EngineerInferface import EngineerInterface
from interface.RecordingPlayer import RecordingPlayer
from interface.UserInterface import UserInterface
from model.phases.AssessPhase import AssessPhase
from model.states.AtNestState import AtNestState


class SimulationTest(unittest.TestCase):

    def setUp(self) -> None:
        self.simulation = None
        time.sleep(1)

    def tearDown(self) -> None:
        del self.simulation

    @staticmethod
    def run_sim_with_interface(colony):
        colony.addAgents(50, AtNestState, AssessPhase(), 3)  # You can optionally add agents with specified starting positions, states, phases, and assignments in some of the interfaces
        colony.randomizeInitialState()  # You can optionally randomize which site each agent starts from in some of the interfaces
        colony.runSimulation()  # Starts the interface
        pygame.quit()

    def run_simulation_test(self, test_name, simulation):
        try:
            self.run_sim_with_interface(simulation(simulationDuration=3, useJson=False, useRestAPI=False))
        except Exception as err:
            self.fail(f"{test_name} failed with exception: {err}, {type(err)}")

    def test_user_interface(self):
        """ Check that the user interface can run for a few seconds without breaking. """
        self.run_simulation_test("User Interface", UserInterface)

    def test_engineer_interface(self):
        """ Check that the engineer interface can run for a few seconds without breaking. """
        self.run_simulation_test("Engineer Interface", EngineerInterface)

    def test_recording_player(self):
        """ Check that the recording player can run for a few seconds without breaking. """
        try:
            RecordingPlayer().runSimulation()  # Starts the interface
            pygame.quit()
        except Exception as err:
            self.fail(f"Recording Player failed with exception: {err}, {type(err)}")

    def test_empirical_testing_interface(self):
        """ Check that the empirical_testing interface can run for a few seconds without breaking. """
        self.run_simulation_test("Empirical Testing Interface", EmpiricalTestingInterface)


if __name__ == '__main__':
    unittest.main()
