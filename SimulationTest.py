import json
import time
import unittest

from interface.EmpiricalTestingInterface import EmpiricalTestingInterface
from interface.EngineerInferface import EngineerInterface
from interface.RecordingPlayer import RecordingPlayer
from interface.UserInterface import UserInterface
from model.phases.AssessPhase import AssessPhase
from model.states.AtNestState import AtNestState


class SimulationTest(unittest.TestCase):

    @staticmethod
    def run_sim_with_interface(colony):
        colony.addAgents(50, AtNestState, AssessPhase(), 3)  # You can optionally add agents with specified starting positions, states, phases, and assignments in some of the interfaces
        colony.randomizeInitialState()  # You can optionally randomize which site each agent starts from in some of the interfaces
        colony.runSimulation()  # Starts the interface

    def run_simulation_test(self, test_name, simulation, j=False):
        try:
            print(f"Running {test_name} Test")
            self.run_sim_with_interface(simulation(simulationDuration=3, useJson=j, useRestAPI=False, shouldRecord=False))
        except Exception as err:
            self.fail(f"{test_name} failed with exception: {err}, {type(err)}")

    def test_user_interface(self):
        """ Check that the user interface can run for a few seconds without breaking. """
        self.run_simulation_test("User Interface", UserInterface)

    def test_engineer_interface(self):
        """ Check that the engineer interface can run for a few seconds without breaking. """
        self.run_simulation_test("Engineer Interface", EngineerInterface)

    def test_empirical_testing_interface(self):
        """ Check that the empirical_testing interface can run for a few seconds without breaking. """
        self.run_simulation_test("Empirical Testing Interface", EmpiricalTestingInterface)

    def test_recording_player(self):
        """ Check that the recording player can run for a few seconds without breaking. """
        try:
            self.set_up_recording()
            time.sleep(1)  # Make sure that the recording has enough time to record before this starts
            RecordingPlayer().runSimulation()  # Starts the interface
        except Exception as err:
            self.fail(f"Recording Player failed with exception: {err}, {type(err)}")

    @staticmethod
    def set_up_recording():
        with open(f'recording/results/most_recent.json', 'w') as file:
            data = {'file_base': f'test/test'}
            json.dump(data, file)


if __name__ == '__main__':
    unittest.main()
