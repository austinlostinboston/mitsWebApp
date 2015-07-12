from django.test import TestCase
from weiss.flows.abstractState import State
from weiss.flows.factory import getFlowManager


class StateTestCase(TestCase):
    def setUp(self):
        fmgr = getFlowManager()
        self.SI = fmgr.createState(1, State.SystemInitiative)
        self.TS = fmgr.createState(2, State.TypeSelected)
        self.ES = fmgr.createState(3, State.EntitySelected)
        self.CS = fmgr.createState(4, State.CommentSelected)
        self.RS = fmgr.createState(5, State.RangeSelected)
        pass

    def test_next_possible_actions(self):
        self.assertEqual(set([7,8]), self.SI.nextPossibleActions);
        self.assertEqual(set([5,7,8]), self.TS.nextPossibleActions);
        self.assertEqual(set([1,3,4,5,6,7,8]), self.ES.nextPossibleActions);
        self.assertEqual(set([1,2,3,4,5,6,7,8]), self.CS.nextPossibleActions);
