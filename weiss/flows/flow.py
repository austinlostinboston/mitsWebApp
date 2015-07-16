"""
Flow

Flow represents the context for a user. Each instance contains:
    1. information about the user
    2. state information
    3. misc


Author: Ming Fang

"""
import logging

from weiss.flows.factory import getFlowManager, StateFactory
from weiss.models import State

logger = logging.getLogger(__name__)

class Flow(object):

    def __init__(self, request):
        self._request = request
        self._fmgr = getFlowManager()
        self._state = StateFactory(State.SystemInitiative)
        self._fmgr.register(request.user, self)
        self._action = None

        self._entities = None
        self._entity = None
        self._eid = None

        self._type = None
        self._tid = None

        self._cid = None
        self._comment = None



    @property
    def user(self):
        """
        getter for user id, which is a django obj
        """
        return self._request.user

    @property
    def request(self):
        """
        getter for request
        """
        return self._request

    @request.setter
    def request(self, request):
        self._request = request

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
        """Getter for current action

        It is of type models.Action enum
        """
        return self._action

    @action.setter
    def action(self, new_action):
        """Setter for action
        """
        self._action = new_action

    @property
    def entities(self):
        """Getter for current range of entities

        elements are of type models.Entity
        """
        return self._entities

    @entities.setter
    def entities(self, new_entities):
        """Setter for entities
        """
        self._entities = new_entities
        self._eid = None
        self._entity = None

    @property
    def eid(self):
        """Getter for eid in form of int
        """
        if self._eid is None:
            if self._entity is None:
                return None
            else:
                return self._entity.eid
        return self._eid

    @eid.setter
    def eid(self, new_eid):
        """Setter for eid
        """
        self._eid = new_eid
        self._entities = None


    @property
    def entity(self):
        """Getter for entity
        """
        if self._entity is None:
            if self._eid is None:
                return None
            else:
                return Entity.objects.get(eid=self._eid)
        else:
            return self._entity

    @entity.setter
    def entity(self, new_entity):
        """Setter for entity
        """
        self._entity = new_entity
        self._eid = None

    @property
    def cid(self):
        """Getter for current comment id
        """
        if self._cid is None:
            if self._comment is None:
                return None
            else:
                return self._comment.cid
        else:
            return self._cid

    @cid.setter
    def cid(self, new_cid):
        """Setter for cid
        """
        self._cid = new_cid
        self._comment = None


    @property
    def comment(self):
        """Getter comment
        """
        if self._comment is None:
            if self._cid is None:
                return None
            else:
                return Comment.objects.get(cid=self._cid)
        else:
            return self._comment

    @property
    def type(self):
        """Getter for current type

        of type models.Type
        """
        return self._type

    @type.setter
    def type(self, new_type):
        """Setter for type
        """
        self._type = new_type

    @property
    def tid(self):
        """Getter for tid
        """
        if self._type is None:
            return None
        else:
            return self._type.value

    @tid.setter
    def tid(self, new_tid):
        """Setter for tid
        """
        self._type = Type(new_tid)


    def filter(self, predicate):
        """
        filter and keep entities base on predicate
        which is a function
        """
        filter(self._entities, predicate)

    def keep(self, idx):
        assert(idx < len(self.entities))
        self.entity = self.entities[idx]
        self.entities = [self.entity]




