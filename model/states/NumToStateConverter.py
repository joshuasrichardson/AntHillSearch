from Constants import SEARCH, AT_NEST, LEAD_FORWARD, FOLLOW, REVERSE_TANDEM, TRANSPORT, GO, CARRIED, DEAD, ESCAPE


def numToState(num, agent):
    """ Get a state object using the number that represents it. """
    if num == AT_NEST:
        from model.states.AtNestState import AtNestState
        return AtNestState(agent)
    if num == SEARCH:
        from model.states.SearchState import SearchState
        return SearchState(agent)
    if num == CARRIED:
        from model.states.CarriedState import CarriedState
        return CarriedState(agent)
    if num == FOLLOW:
        from model.states.FollowState import FollowState
        return FollowState(agent)
    if num == LEAD_FORWARD:
        from model.states.LeadForwardState import LeadForwardState
        return LeadForwardState(agent)
    if num == REVERSE_TANDEM:
        from model.states.ReverseTandemState import ReverseTandemState
        return ReverseTandemState(agent)
    if num == TRANSPORT:
        from model.states.TransportState import TransportState
        return TransportState(agent)
    if num == GO:
        from model.states.GoState import GoState
        return GoState(agent)
    if num == DEAD:
        from model.states.DeadState import DeadState
        return DeadState(agent)
    if num == ESCAPE:
        from model.states.EscapeState import EscapeState
        return EscapeState(agent, SEARCH, [[0, 0]])
