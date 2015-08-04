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

This file defines the concrete control flow logic
"""
from django.test import TestCase
from weiss.flows.factory import getFlowManager
from weiss.models import Action, State


class StateTestCase(TestCase):
    def setUp(self):
        fmgr = getFlowManager()
        self.SI = fmgr.createState(Action(1), State.SystemInitiative)
        self.TS = fmgr.createState(Action(2), State.TypeSelected)
        self.ES = fmgr.createState(Action(3), State.EntitySelected)
        self.CS = fmgr.createState(Action(4), State.CommentSelected)
        self.RS = fmgr.createState(Action(5), State.RangeSelected)
        pass

    def test_next_possible_actions(self):
        self.assertEqual(set([Action(7),Action(8)]), self.SI.nextPossibleActions);
        self.assertEqual(set([Action(5),Action(7),Action(8)]), self.TS.nextPossibleActions);
        self.assertEqual(set([Action(1),Action(3),Action(4),Action(5),Action(6),Action(7),Action(8)]), self.ES.nextPossibleActions);
        self.assertEqual(set([Action(1),Action(2),Action(3),Action(4),Action(5),Action(6),Action(7),Action(8)]), self.CS.nextPossibleActions);
