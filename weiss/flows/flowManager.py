"""
Flow Mnager

NOTE: this class should be created by signleton factory in factory.py

this class is responsible for
    1. user state factory.
    2. loop up state by sid
    3. make transit from one state based on a given action

Author: Ming Fang <mingf@cs.cmu.edu>
"""

import logging

from weiss.models import State # for enums
from weiss.utils.switch import switch
from weiss.flows.states import *

logger = logging.getLogger(__name__)

class FlowManager:

    def __init__(self):
        self._stateTable = {}

    def createState(self, uid, sid):
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

    def register(self, uid):
        state = self.createState(uid, State.SystemInitiative)
        self._stateTable[uid] = state
        return state

    def lookUp(self, uid):
        if not self._stateTable.has_key(uid):
            return None
        else:
            return self._stateTable[uid]


    def transit(self, user, sid):
        curr_state = self.lookUp(user)
        if curr_state is None:
            logger.error("Can not make transit from a none state, %s, %s" %(user, action))
            return
        new_state = self.createState(user, sid)
        logger.info("Transit from %s to %s" % (curr_state, new_state))
        self._stateTable[user] = new_state


