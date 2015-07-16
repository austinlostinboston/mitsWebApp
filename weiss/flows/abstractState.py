"""
AbstractState

Author: Ming Fang

"""
import abc

class AbstractState(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        pass

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


