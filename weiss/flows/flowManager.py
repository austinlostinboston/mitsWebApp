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

    def register(self, uid, flow):
        """Register a user's flow object
            deprecated

        :param uid: the user id
        :param flow: the flow obj associated with the user
        :return: void
        """
        self._flowTable[uid] = flow
        return

    def lookUp(self, uid):
        """Look up a flow given a user id, a int
            deprecated
        :param uid: the user id to be looked up, get it by request.user
        :return: the flow obj associated with the given user, or None if not found
        """
        return self._flowTable.get(uid, None)

    def new(self, request):
        flow = Flow(request)
        assert(type(flow.user_id) is int, "%s" % type(flow.user_id))
        #self.register(flow.user_id, flow)
        return flow

    def delete(self, user):
        if user in self._flowTable:
            del self._flowTable[user]
            return True
        else:
            return False
