"""
Flow

Flow represents the context for a user. Each instance contains:
    1. information about the user
    2. state information
    3. misc


Author: Ming Fang

"""
from weiss.flows.factory import getFlowManager, StateFactory
from weiss.models import State

class Flow(object):

    def __init__(self, user):
        self._user = user
        self._fmgr = getFlowManager
        self._state = StateFactory(State.SystemInitiative)
        self.fmgr.register(self.user, self.state)
        self._action = None
        self._entities = None
        self._type = None
        self._comment = None



    @property
    def user(self):
        """
        getter for user id, which is a django obj
        """
        return self._user

    @property
    def state(self):
        """
        getter for state obj
        """
        return self._state

    def transit(self, sid):
        """
        make a transition
        """
        assert(isinstance(sid, State))
        logger.info("Transit from %s to %s" % (self.state.name, sid.name))
        self._state = StateFactory(sid)


    def __str__(self):
        return "%s in %s" % (self.user, self.state.name)

    @property
    def action(self):
        """
        getter for current action
        of type models.Action enum
        """
        return self._action

    @action.setter
    def action(self, new_action):
        self._action = new_action

    @property
    def entities(self):
        """
        getter for current range of entities
        elements are of type models.Entity
        """
        return self._entities

    @entities.setter
    def entities(self, new_entities):
        self._entities = new_entities


    @property
    def comment(self):
        """
        getter for current comment
        of type models.Comment
        """
        return self._comment

    @comment.setter
    def comment(self, new_comment):
        self._comment = new_comment

    @property
    def type(self):
        """
        getter for current type
        of type models.Type
        """
        return self._type

    @type.setter
    def type(self, new_type):
        self._type = new_type


    def filter(self, predicate):
        """
        filter and keep entities base on predicate
        which is a function
        """
        filter(self._entities, predicate)




