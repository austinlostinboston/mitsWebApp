"""
Flow
Flow represents the context for a user. Each instance contains:
    1. information about the user
    2. state information
    3. misc
Author: Ming Fang
"""
import logging

from django.utils import timezone

from weiss.flows.stateFactory import StateFactory
from weiss.models import State, Type, Entity, Comment, Actions, History, Action

logger = logging.getLogger(__name__)

class Flow(object):
    def __init__(self, user_id, user=None, request=None):
        self._user = user
        self._user_id = user_id
        self._request = request
        self._state = StateFactory(State.SystemInitiative)
        self._action = Action.Greeting
        self._query = None
        self._response = None
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
        getter for user name, a str, unregister user does not have a user name
        """
        return str(self._user)

    @property
    def user_id(self):
        """Every one has the user id, which is a int
        """
        return self._user_id

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

    @property
    def action(self):
        """Getter for current action
        It is of type models.Action enum
        """
        assert(isinstance(self._action, Action))
        return self._action

    @action.setter
    def action(self, new_action):
        """Setter for action
        """
        assert(isinstance(new_action, Action))
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
        assert (isinstance(new_type, Type))
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

    @property
    def query(self):
        return self._query

    @property
    def response(self):
        return self._response

    def transit(self, sid):
        """
        make a transition
        """
        assert (isinstance(sid, State))
        logger.info("Transit from %s to %s" % (self.state.name, sid.name))
        self._state = StateFactory(sid)

    def filter(self, predicate):
        """filter and keep entities base on predicate, which is a function
        :param predicate:
        :return: void
        """
        filter(self._entities, predicate)

    def keep(self, idx):
        """Keep one of the entities based on idx
        :param idx: the index of entity that is kept
        :return: void
        """
        assert (idx < len(self.entities))
        self.entity = self.entities[idx]
<<<<<<< HEAD
        self.entities = [self.entity]
=======
        self.entities = [self.entity]
<<<<<<< HEAD
>>>>>>> 2e0cee4... a lot syntax changes
=======

    def start_line(self, action, query=""):
        self._query = query
        self._action = action

    def end_line(self, response):
        self._response = response
        aid = Actions.objects.get(aid=self.action.value)
        History.objects.create(query=self.query,
                               userid=self.user_id,
                               response=response,
                               aid=aid,
                               eid=self.entity,
                               time=timezone.now())
<<<<<<< HEAD
>>>>>>> f6651f7... refactor action util
=======

    def size(self):
        if self.entities is None:
            return 0
        else:
            return len(self.entities)

    def __str__(self):
        res = "--  Flow State\n"        \
              "--  User ID: %s\n" \
              "--User name: %s\n" \
              "--    State: %s\n"       \
              "--     Step: %s\n"       \
              "--   Action: %s\n"       \
              "--------------\n"        \
              "--      TID: %s\n"       \
              "--      EID: %s\n"       \
              "--      CID: %s\n"       \
              "--  Num Ent: %s\n"       \
              "--------------\n"        \
              "--     Type: %s\n"       \
              "--   Entity: %s\n" % (self.user_id,
                                     self.user,
                                     self.state,
                                     self.state.step,
                                     self.action.name,
                                     self.tid,
                                     self.eid,
                                     self.cid,
                                     self.size(),
                                     self.type,
                                     self.entity)

        return res


>>>>>>> 264440e... a lot of bug fixes, new request and response logic is working
