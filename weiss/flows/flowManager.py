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

    def register(self, uid, flow):
        self._stateTable[uid] = flow
        return

    def lookUp(self, uid):
        if not self._stateTable.has_key(uid):
            return None
        else:
            return self._stateTable[uid]


    def transit(self, user, sid):
        flow = self.lookUp(user)
        if flow is None:
            logger.error("Can not make transit from a none state, %s, %s" %(user, action))
            return
        flow.transit(sid)


