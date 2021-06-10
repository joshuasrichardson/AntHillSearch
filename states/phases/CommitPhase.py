import numpy as np


class CommitPhase:

    @staticmethod
    def transportOrReverseTandem(state):
        if np.random.randint(0, 3) == 0:
            from states.ReverseTandemState import ReverseTandemState
            state.setState(ReverseTandemState(state.agent), state.agent.assignedSite.pos)
        else:
            from states.TransportState import TransportState
            state.setState(TransportState(state.agent), state.agent.assignedSite.pos)
