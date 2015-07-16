'''
Provide singleton for flowManager

Author: Ming Fang
'''

from weiss.flows.flowManager import FlowManager
from weiss.models import State
from weiss.utils.switch import switch

_instance = None

def getFlowManager():
    global _instance
    if _instance is None:
        _instance = FlowManager()

    return _instance

def StateFactory(sid):
    assert(isinstance(sid, State))
    """
    Factory for state class
    """
    for case in switch(sid):
        if case(State.SystemInitiative):
            return SystemInitiative(uid)

        if case(State.TypeSelected):
            return TypeSelected(uid)

        if case(State.EntitySelected):
            return EntitySelected(uid)

        if case(State.CommentSelected):
            return CommentSelected(uid)

        if case(State.RangeSelected):
            return RangeSelected(uid)

        if case():
            raise KeyError("No such state %s" % sid)


