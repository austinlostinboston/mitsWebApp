"""
This file defines the concrete control flow logic

Author: Ming Fang
"""
from weiss.flows.abstractState import State, AbstractState
from weiss.utils.switch import switch
from weiss.dialogue.actions import Action


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

    _npa = set([Action.EntitySelection,
                Action.TypeSelection])

    def __init__(self, uid):
        AbstractState.__init__(self, uid)

    @property
    def sid(self):
        return State.SystemInitiative

    @property
    def nextPossibleActions(self):
        return self._npa

    def transit(self, aid):
        for case in switch(aid):
            if case(Action.EntitySelection):
                return Stete.EntitySelected

            if case(Action.TypeSelection):
                return State.TypeSelected

            if case():
                raise KeyError("Invaild action")


"""
Type selected state
The followings should be determined:
    curr_tid
"""
class TypeSelected(AbstractState):

    _npa = set([Action.NextRandomEntity,
                Action.EntitySelection,
                Action.TypeSelection])

    def __init__(self, uid):
        AbstractState.__init__(self, uid)

    @property
    def sid(self):
        return State.TypeSelected

    @property
    def nextPossibleActions(self):
        return self._npa

    def transit(self, aid):
        for case in switch(aid):
            if case(Action.NextRandomEntity):
                return State.EntitySelected

            if case(Action.EntitySelection):
                return State.EntitySelected

            if case(Action.TypeSelection):
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

    _npa = set([Action.NextRandomComment,
                Action.NextPositiveComment,
                Action.NextNegativeComment,
                Action.NextRandomEntity,
                Action.SentimentStats,
                Action.EntitySelection,
                Action.TypeSelection])

    def __init__(self, uid):
        AbstractState.__init__(self, uid)

    @property
    def sid(self):
        return State.EntitySelected

    @property
    def nextPossibleActions(self):
        return self._npa

    def transit(self, aid):
        for case in switch(aid):
            if case(Action.NextRandomComment):
                return State.CommentSelected

            if case(Action.NextPositiveComment):
                return State.CommentSelected

            if case(Action.NextNegativeComment):
                return State.CommentSelected

            if case(Action.NextRandomEntity):
                return State.EntitySelected

            if case(Action.SentimentStats):
                return State.EntitySelecetd

            if case(Action.EntitySelection):
                return State.EntitySelected

            if case(Action.TypeSelection):
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

    _npa = set([Action.NextRandomComment,
                Action.NextOppositeComment,
                Action.NextPositiveComment,
                Action.NextNegativeComment,
                Action.NextRandomEntity,
                Action.SentimentStats,
                Action.EntitySelection,
                Action.TypeSelection])

    def __init__(self, uid):
        AbstractState.__init__(self, uid)

    @property
    def sid(self):
        return State.CommentSelected

    @property
    def nextPossibleActions(self):
        return self._npa

    def transit(self, aid):
        for case in switch(aid):
            if case(Action.NextRandomComment):
                return State.CommentSelected

            if case(Action.NextOppositeComment):
                return State.CommentSelected

            if case(Action.NextPositiveComment):
                return State.CommentSelected

            if case(Action.NextNegativeComment):
                return State.CommentSelected

            if case(Action.NextRandomEntity):
                return State.EntitySelected

            if case(Action.SentimentStats):
                return State.CommentSelected

            if case(Action.EntitySelection):
                return State.EntitySelected

            if case(Action.TypeSelection):
                return State.TypeSelected

            if case():
                raise KeyError("Invaild action")


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

    def transit(self, aid):
        raise NotImplementedError()



