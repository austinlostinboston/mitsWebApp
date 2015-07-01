"""
Abstract Flow state

Author: Ming Fang <mingf@cs.cmu.edu>
"""

class State(object):

    def __init__(self, name):
        self._name = name
        self._actions = {} # int (aid) -> State
        self._npa = set()  # next possible actions

    def getName(self):
        return self._name

    def getNextPossibleActions(self):
        return _nps

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


