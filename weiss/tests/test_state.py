from django.test import TestCase

from weiss.flows.states import *


class StateTestCase(TestCase):
    def setUp(self):
        pass


    def test_next_possible_actions(self):
        self.assertEqual(set([7,8]), SystemInitiative.getNextPossibleActions());
        self.assertEqual(set([5,7,8]), TypeSelected.getNextPossibleActions());
        self.assertEqual(set([1,3,4,5,6,7,8]), EntitySelected.getNextPossibleActions());
        self.assertEqual(set([1,2,3,4,5,6,7,8]), CommentSelected.getNextPossibleActions());
