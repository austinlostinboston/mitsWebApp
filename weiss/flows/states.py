"""
This file defines the concrete control flow logic

Author: Ming Fang
"""
from weiss.flows.abstractState import AbstractState
from weiss.models import Action, State, Step # for enums

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
11. Entity Comcirmation
"""


class SystemInitiative(AbstractState):
    """
    Systen initialization state
    the beginning point of a dialogue
    """

    _npa = {Action.EntitySelection,
            Action.TypeSelection,
            Action.UnknownAction}

    def __init__(self):
        AbstractState.__init__(self)

    @property
    def sid(self):
        return State.SystemInitiative

    @property
    def nextPossibleActions(self):
        return self._npa


class TypeSelected(AbstractState):
    """
    Type selected state
    The followings should be determined:
        curr_tid
    """

    _npa = {Action.NextRandomEntity,
            Action.EntitySelection,
            Action.TypeSelection,
            Action.UnknownAction}

    def __init__(self):
        AbstractState.__init__(self)

    @property
    def sid(self):
        return State.TypeSelected

    @property
    def nextPossibleActions(self):
        return self._npa


class EntitySelected(AbstractState):
    """
    Entity selected state
    The followings should be determined:
        curr_tid
        curr_eid
    """

    _npa = {Action.NextRandomComment,
            Action.NextPositiveComment,
            Action.NextNegativeComment,
            Action.NextRandomEntity,
            Action.SentimentStats,
            Action.EntitySelection,
            Action.TypeSelection,
            Action.UnknownAction}

    def __init__(self):
        AbstractState.__init__(self)

    @property
    def sid(self):
        return State.EntitySelected

    @property
    def nextPossibleActions(self):
        return self._npa


class CommentSelected(AbstractState):
    """
    Comment selecetd state
    The followings should be determined:
        curr_tid
        curr_eid
        curr_cid
    """

    _npa = {Action.NextRandomComment,
            Action.NextOppositeComment,
            Action.NextPositiveComment,
            Action.NextNegativeComment,
            Action.NextRandomEntity,
            Action.SentimentStats,
            Action.EntitySelection,
            Action.TypeSelection,
            Action.UnknownAction}

    def __init__(self):
        AbstractState.__init__(self)

    @property
    def sid(self):
        return State.CommentSelected

    @property
    def nextPossibleActions(self):
        return self._npa


class RangeSelected(AbstractState):
    """
    Range Selected state
    """

    _npa = {Action.TypeSelection,
            Action.EntityConfirmation,
            Action.UnknownAction}

    def __init__(self):
        AbstractState.__init__(self)
        self._step = Step.RangeInitiative

    @property
    def sid(self):
        return State.RangeSelected

    @property
    def nextPossibleActions(self):
        return self._npa

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, new_step):
        self._step = new_step

