"""
This file defines the concrete control flow logic

Author: Ming Fang
"""
from weiss.flows.abstractState import State, AbstractState
from weiss.utils.switch import switch


"""
Definitions of the system states
"""


"""
Definition of the control flow
1. Next Random Comment
2. Next Opposite Comment
3. Next Positive Comment
4. Next Negative Comment
5. Next Random Entity (within current type)
6. Sentiment Stats
7. Entity Selection (base on key and within current type)
8. Type Selection
9. Greeting
10. Unknown Action
"""

"""
Systen initialization state
the beginning point of the dialog
"""
class SystemInitiative(AbstractState):

    _npa = set([7, 8])

    def __init__(self, uid):
        AbstractState.__init__(self, uid)

    @property
    def sid(self):
        return State.SystemInitiative

    @property
    def nextPossibleActions(self):
        return self._npa

    def transit(aid):
        for case in switch(aid):
            if case(7):
                return Stete.EntitySelected
            if case(8):
                return State.TypeSelected
            if case():
                raise KeyError("Invaild action id")


"""
Type selected state
The followings should be determined:
    curr_tid
"""
class TypeSelected(AbstractState):

    _npa = set([5,7,8])

    def __init__(self, uid):
        AbstractState.__init__(self, uid)

    @property
    def sid(self):
        return State.TypeSelected

    @property
    def nextPossibleActions(self):
        return self._npa

    def transit(aid):
        for case in switch(aid):
            if case(5):
                return State.EntitySelected
            if case(7):
                return State.EntitySelected
            if case(8):
                return State.TypeSelected
            if case():
                raise KeyError("Invaild action id")

"""
Entity selceted state
The followings should be determined:
    curr_tid
    curr_eid
"""
class EntitySelected(AbstractState):

    _npa = set([1,3,4,5,6,7,8])

    def __init__(self, uid):
        AbstractState.__init__(self, uid)

    @property
    def sid(self):
        return State.EntitySelected

    @property
    def nextPossibleActions(self):
        return self._npa

    def transit(aid):
        for case in switch(aid):
            if case(1):
                return State.CommentSelected
            if case(3):
                return State.CommentSelected
            if case(4):
                return State.CommentSelected
            if case(5):
                return State.EntitySelected
            if case(6):
                return State.EntitySelecetd
            if case(7):
                return State.EntitySelected
            if case(8):
                return State.TypeSelected
            if case():
                raise KeyError("Invaild action id")




"""
Comment selecetd state
The followings should be determined:
    curr_tid
    curr_eid
    curr_cid
"""
class CommentSelected(AbstractState):

    _npa = set([1,2,3,4,5,6,7,8])

    def __init__(self, uid):
        AbstractState.__init__(self, uid)

    @property
    def sid(self):
        return State.CommentSelected

    @property
    def nextPossibleActions(self):
        return self._npa

    def transit(aid):
        for case in switch(aid):
            if case(1):
                return State.CommentSelected
            if case(2):
                return State.CommentSelected
            if case(3):
                return State.CommentSelected
            if case(4):
                return State.CommentSelected
            if case(5):
                return State.EntitySelected
            if case(6):
                return State.CommentSelected
            if case(7):
                return State.EntitySelected
            if case(8):
                return State.TypeSelected
            if case():
                raise KeyError("Invaild action id")


"""
Range Selected state
"""
class RangeSelected(AbstractState):

    def __init__(self, uid):
        AbstractState.__init__(self, uid)

    @property
    def sid(self):
        return State.RangeSelected

    @property
    def nextPossibleActions(self):
        raise NotImplementedError()

    def transit(aid):
        raise NotImplementedError()



