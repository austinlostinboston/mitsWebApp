from django.test import TestCase
from weiss.flows.abstractState import State
from weiss.flows.factory import getFlowManager
from weiss.actions.actions import Action


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
