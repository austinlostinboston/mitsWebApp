"""
Copyright 2015 Austin Ankney, Ming Fang, Wenjun Wang and Yao Zhou

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Flow

Flow represents the context for a user. Each instance contains:
    1. information about the user
    2. state information
    3. current action
    4. current entity or entities
    5. current query
    6. current response
    7. current type
    8. current comment


Author: Ming Fang

"""
import logging
import uuid

from django.utils import timezone

from django.db.models import Q

from weiss.flows.stateFactory import StateFactory
from weiss.models import State, Type, Entity, Comment, Actions, History, Action, Summary, Step
from weiss.dialogue import entityRanker
from weiss.dialogue import actionUtil

logger = logging.getLogger(__name__)


class Flow(object):
    def __init__(self, request):
        if request.user.id is None:
            user_id = uuid.uuid1()
        else:
            user_id = uuid.UUID(int=request.user.id)
        self._user = request.user
        self._user_id = user_id
        self._request = None
        self._state = StateFactory(State.SystemInitiative)
        self._action = Action.Greeting
        self._query = None
        self._response = None
        self._entities = None
        self._entity = None
        self._eid = None
        self._type = None
        self._types = None
        self._tid = None
        self._cid = None
        self._comment = None
        self._sentiment_stats = None

        self._summary = None
        self._sbid = None
        self._next_pos_rank = 1
        self._next_neg_rank = 1

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
        assert (isinstance(self._action, Action))
        return self._action

    @action.setter
    def action(self, new_action):
        """Setter for action
        """
        assert (isinstance(new_action, Action))
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
        self._entity = None
        self.cid = None
        self._type = None
        self.next_pos_rank = 1
        self.next_neg_rank = 1

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
        self._type = None
        self.cid = None
        self.summary = None
        self.next_pos_rank = 1
        self.next_neg_rank = 1

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

    @comment.setter
    def comment(self, new_comment):
        self._cid = None
        self._comment = new_comment

    @property
    def types(self):
        return self._types

    @types.setter
    def types(self, new_types):
        self._types = new_types
        self._type = None

    @property
    def type(self):
        """Getter for current type

        of type models.Type
        """
        if self._type is not None:
            return self._type
        elif self.entity is not None:
            self._type = Type(self.entity.tid.tid)
            return self._type

    @type.setter
    def type(self, new_type):
        """Setter for type
        """
        assert (isinstance(new_type, Type))
        self.types = None
        self._type = new_type

    @property
    def tid(self):
        """Getter for tid
        """
        if self.type is None:
            return None
        else:
            return self._type.value

    @tid.setter
    def tid(self, new_tid):
        """Setter for tid
        """
        self.types = None
        self._type = Type(new_tid)

    @property
    def summary(self):
        if self._summary is None and self._sbid is None:
            return None
        elif self._summary is not None:
            return self._summary
        else:
            return Summary.objects.get(sbid=self._sbid)

    @summary.setter
    def summary(self, new_summary):
        self._summary = new_summary
        self._sbid = None

    @property
    def sbid(self):
        if self._summary is None and self._sbid is None:
            return None
        elif self._summary is not None:
            return self._summary.sbid
        else:
            return self._sbid

    @sbid.setter
    def sbid(self, new_sbid):
        self._sbid = new_sbid
        self._summary = None

    @property
    def next_pos_rank(self):
        return self._next_pos_rank

    @next_pos_rank.setter
    def next_pos_rank(self, new_next_pos_rank):
        self._next_pos_rank = new_next_pos_rank

    @property
    def next_neg_rank(self):
        return self._next_neg_rank

    @next_neg_rank.setter
    def next_neg_rank(self, new_next_neg_rank):
        self._next_neg_rank = new_next_neg_rank

    @property
    def query(self):
        """
        Getter for query, a string
        :return:
        """
        return self._query

    @property
    def response(self):
        """
        Getter for response, a string
        :return:
        """
        return self._response

    @property
    def sentiment_stats(self):
        return self._sentiment_stats

    @sentiment_stats.setter
    def sentiment_stats(self, new_stats):
        try:
            num_pos, num_neu, num_all = new_stats
        except ValueError:
            logger.error("sentiment_stats should be a 3 items tuple")
            return
        self._sentiment_stats = SentimentStats(num_pos, num_neu, num_all)

    def transit(self, sid):
        """
        make a transition
        """
        assert (isinstance(sid, State))
        logger.info("Transit from %s to %s" % (self.state.name, sid.name))
        self._state = StateFactory(sid)

    def transit_under_range(self):
        """
        make a transition based on the range
        :return:
        """
        assert self.entities is not None
        if len(self.entities) == 1:
            # good, we found only one, go to EntitySelected with curr_eid set
            self.transit(State.EntitySelected)
            self.keep(0)
            return True
        elif len(self.entities) > 1:
            # It gave a shitload, go to RangeSelected with state.entities set
            self.transit(State.RangeSelected)
            if self.type is not None:
                self.state.step = Step.TypeSelected
            else:
                type_range = actionUtil.get_type_range(self.entities)
                if len(type_range) == 1:
                    self.type = type_range.pop()
                    self.state.step = Step.TypeSelected
                    self.rank()
                else:
                    assert len(type_range) > 1
                    self.state.step = Step.RangeInitiative
                    self.types = type_range
            return True
        else:
            return False

    def match_by_title(self, keywords):
        """
        Try to match a list of keywords
        :param keywords: a list of keywords with which we match entities
        :return: True if successfully matched all keywords
                 False if not exists a entity that matches all keywords
        """
        if self.type is not None:
            base = Q(tid=self.tid)
        else:
            base = Q()

        # before the first, we try to match all keywords as a whole
        q = base
        keyword = " ".join(keywords)
        q &= Q(name__icontains=keyword)
        self.entities = Entity.objects.filter(q)
        if self.transit_under_range():
            return True

        # first, we try to match first 3 key words by title
        q = base
        for keyword in keywords:
            q &= Q(name__icontains=keyword)
        self.entities = Entity.objects.filter(q)
        if self.transit_under_range():
            return True

        # failed, return false
        return False

    def match_by_description(self, keywords):
        """
        Try to match a list of keywords
        :param keywords: a list of keywords with which we match entities
        :return: True if successfully matched all keywords
                 False if not exists a entity that matches all keywords
        """
        if self.type is not None:
            base = Q(tid=self.tid)
        else:
            base = Q()

        # before the first, we try to match all keywords as a whole
        q = base
        keyword = " ".join(keywords)
        q &= Q(name__icontains=keyword)
        self.entities = Entity.objects.filter(q)
        if self.transit_under_range():
            return True

        # failed, we try to match first 3 key words by description
        q = base
        for keyword in keywords:
            q &= Q(description__icontains=keyword)
        self.entities = Entity.objects.filter(q)
        if self.transit_under_range():
            return True

        # failed, return false
        return False

    def filter(self, predicate):
        """filter and keep entities base on predicate, which is a function
        :param predicate:
        :return: void
        """
        self.entities = filter(predicate, self.entities)

    def keep(self, idx):
        """Keep one of the entities based on idx

        TODO: Look closer into this case, query set behaves differently than build in list
        :param idx: the index of entity that is kept
        :return: void
        """
        logger.info("Keep %s, entities = %s" % (idx, self.entities))
        assert (idx < len(self.entities))
        self.entities = [self.entities[idx]]
        self.entity = self.entities[0]

    def rank(self):
        """Rank the entities
        """
        assert self.type in Type
        self.entities = entityRanker.ranked(self.entities, self.type)

    def start_line(self, action, query=""):
        """
        Start a line.
        :param action:
        :param query: The query string
        :return:
        """
        self._query = query
        self._action = action

    def end_line(self, response):
        """
        End a line. Create a record in the backend db
        :param response: The response string
        :return:
        """
        self._response = response
        aid = Actions.objects.get(aid=self.action.value)
        History.objects.create(query=self.query,
                               userid=self.user_id,
                               response=response,
                               aid=aid,
                               eid=self.entity,
                               time=timezone.now())

    def size(self):
        """Get the size of the entities

            handle None case
        :return: the size of entities
        """
        if self.entities is None:
            return 0
        else:
            return len(self.entities)

    def save_into(self, request):
        """
        Save myself to session
        :return:
        """
        request.session['flow'] = self

    def __str__(self):
        return "--  Flow State\n" \
               "--  User ID: %s\n" \
               "--User name: %s\n" \
               "--    State: %s\n" \
               "--     Step: %s\n" \
               "--   Action: %s\n" \
               "--------------\n" \
               "--    Types: %s\n" \
               "--      TID: %s\n" \
               "--      EID: %s\n" \
               "--      CID: %s\n" \
               "--     SBID: %s\n" \
               "-- next pos: %s\n" \
               "-- next neg: %s\n" \
               "--    Stats: %s\n" \
               "--  Num Ent: %s\n" \
               "--     Ents: %s\n" \
               "--------------\n" \
               "--     Type: %s\n" \
               "--   Entity: %s\n" % (self.user_id,
                                      self.user,
                                      self.state,
                                      self.state.step,
                                      self.action.name,
                                      self.types,
                                      self.tid,
                                      self.eid,
                                      self.cid,
                                      self.sbid,
                                      self.next_pos_rank,
                                      self.next_neg_rank,
                                      self.sentiment_stats,
                                      self.size(),
                                      self.entities,
                                      self.type,
                                      self.entity)


class SentimentStats(object):
    def __init__(self, num_pos, num_neu, num_all):
        self._num_pos = num_pos
        self._num_neu = num_neu
        self._num_all = num_all

    @property
    def num_pos(self):
        return self._num_pos

    @property
    def num_neu(self):
        return self._num_neu

    @property
    def num_neg(self):
        return self._num_all - self._num_pos - self._num_neu

    @property
    def num_all(self):
        return self._num_all

    def __str__(self):
        return "Pos: %s, Neu: %s, Neg: %s, All: %s" % (self.num_pos,
                                                       self.num_neu,
                                                       self.num_neg,
                                                       self.num_all)
