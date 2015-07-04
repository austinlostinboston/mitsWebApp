"""
Abstract Flow state and State manager

Author: Ming Fang <mingf@cs.cmu.edu>
"""

import logging

logger = logging.getLogger(__name__)

class FlowManager:

    def __init__(self):
        self._stateTable = {}

    def createState(self, name):
        state = self.State(name)
        sid = len(self._stateTable.keys())
        state.setSid(sid)
        self._stateTable[sid] = state
        return state

    def lookUp(self, sid):
        print self._stateTable
        return self._stateTable[sid]

    def nameOf(self, sid):
        return self.lookUp(sid).getName()

    def transit(self, session, aid):
        sid = session['curr_sid']
        curr_state = self.lookUp(sid)
        new_state = curr_state[aid]
        logger.debug("Transit from %s to %s" % (self.nameOf(sid), new_state))
        session['curr_sid'] = new_state.getSid()


    class State(object):
        def __init__(self, name):
            self._name = name
            self._actions = {} # int (aid) -> State
            self._npa = set()  # next possible actions

        def getName(self):
            return self._name

        def getSid(self):
            return self._sid

        def setSid(self, sid):
            self._sid = sid

        def getNextPossibleActions(self):
            """
            get next possible acitons as set
            """
            return self._npa

        def __setitem__(self, aid, state):
            self._actions[aid] = state
            self._npa = set(self._actions.keys())

        def __getitem__(self, aid):
            if aid not in self._npa:
                raise KeyError
            else:
                return self._actions[aid]

        def __str__(self):
            return self._name





