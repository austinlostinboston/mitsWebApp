"""
AbstractState

Author: Ming Fang

"""
import abc
from enum import Enum

class State(Enum):
    SystemInitiative = 1
    TypeSelected = 2
    EntitySelected = 3
    CommentSelected = 4
    RangeSelected = 5

class AbstractState(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, uid):
        self._uid = uid

    @property
    def name(self):
        """
        getter for my name
        """
        return self.sid.name

    @abc.abstractproperty
    def sid(self):
        """
        getter for my state id
        """
        raise NotImplementedError()

    @property
    def uid(self):
        """
        getter for user id
        """
        return self._uid

    @abc.abstractproperty
    def nextPossibleActions(self):
        """
        getter for next possible acitons as set
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def transit(aid):
        """
        return a state id of the destination state
        """
        raise NotImplementedError()

    def __str__(self):
        return self.name


