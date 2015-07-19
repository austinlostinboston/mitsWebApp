'''
Provide singleton for flowManager

Author: Ming Fang
'''

from weiss.flows.flowManager import FlowManager
from weiss.flows.states import *
from weiss.models import State
from weiss.utils.switch import switch

_instance = None


def getFlowManager():
    global _instance
    if _instance is None:
        _instance = FlowManager()

    return _instance


def StateFactory(sid):
    assert (isinstance(sid, State))
    """
    Factory for state class
    """
    for case in switch(sid):
        if case(State.SystemInitiative):
            return SystemInitiative()

        if case(State.TypeSelected):
            return TypeSelected()

        if case(State.EntitySelected):
            return EntitySelected()

        if case(State.CommentSelected):
            return CommentSelected()

        if case(State.RangeSelected):
            return RangeSelected()

        if case():
            raise KeyError("No such state %s" % sid)
