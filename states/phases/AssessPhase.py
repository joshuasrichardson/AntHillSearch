from Constants import *


class AssessPhase:

    @staticmethod
    def acceptOrReject(state):
        # If they determine the site is good enough after they've been there long enough,
        if state.agent.estimatedQuality > MIN_ACCEPT_VALUE:
            # they enter the canvasing phase and start recruiting others.
            state.agent.setPhase(CANVAS_PHASE)
            from states.LeadForwardState import LeadForwardState
            state.setState(LeadForwardState(state.agent), state.agent.assignedSite.getPosition())
        else:
            state.agent.setPhase(EXPLORE_PHASE)
            from states.SearchState import SearchState
            state.setState(SearchState(state.agent), None)
