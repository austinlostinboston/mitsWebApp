"""
Flow Manager

NOTE: this class should be created by singleton factory in factory.py

this class is responsible for
    1. register a user's flow
    2. loop up flow by user id

Author: Ming Fang <mingf@cs.cmu.edu>
"""

import logging
from weiss.flows.flow import Flow

logger = logging.getLogger(__name__)


class FlowManager:
    def __init__(self):
        self._flowTable = {}
        self.next_userid = 2147483647

    def register(self, uid, flow):
        """Register a user's flow object

        :param uid: the user id
        :param flow: the flow obj associated with the user
        :return: void
        """
        self._flowTable[uid] = flow
        return

    def lookUp(self, uid):
        """Look up a flow given a user id, a int

        :param uid: the user id to be looked up, get it by request.user
        :return: the flow obj associated with the given user, or None if not found
        """
        return self._flowTable.get(uid, None)

    def new(self, request=None):
        if request is None:
            flow = Flow(self.next_userid)
            self.next_userid -= 1
        else:
            flow = Flow(request.user.id, request.user, request)
        assert(type(flow.user_id) is int, "%s" % type(flow.user_id))
        self.register(flow.user_id, flow)
        return flow

    def delete(self, user):
        if user in self._flowTable:
            del self._flowTable[user]
