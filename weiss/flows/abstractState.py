"""
Abstract Flow state

Author: Ming Fang <mingf@cs.cmu.edu>
"""

StateTable = {}


class State(object):

    def __init__(self, name, sid):
        self._sid = sid
        self._name = name
        self._actions = {} # int (aid) -> State
        self._npa = set()  # next possible actions
        StateTable[sid] = self

    def getName(self):
        return self._name

    def getSid(self):
        return self._sid

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

    @staticmethod
    def transit(session, aid):
        sid = session['curr_sid']
        session['curr_sid'] = State.lookup(sid).getSid()

    @staticmethod
    def lookup(sid):
        return StateTable[sid]



