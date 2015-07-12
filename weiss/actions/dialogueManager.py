"""
Action Mnager

NOTE: currently all methods are static

this class is responsible for
    1. loop up action handler by action
    2. handle an action request

Author: Ming Fang <mingf@cs.cmu.edu>
"""

import logging
from weiss.utils.switch import switch
from weiss.actions.actions import *
from weiss.flows.factory import getFlowManager

logger = logging.getLogger(__name__)

class DialogueManager(object):

    @staticmethod
    def getHandler(action):
        """
        return action handler according to action
        """
        for case in switch(action):
            if case(Action.NextRandomComment):
                return nextRandomCmt

            if case(Action.NextOppositeComment):
                return nextOppositeCmt

            if case(Action.NextNegativeComment):
                return nextNegativeCmt

            if case(Action.NextRandomEntity):
                return nextRandomEntity

            if case(Action.SentimentStats):
                return sentimentStats

            if case(Action.EntitySelection):
                return entitySelection

            if case(Action.TypeSelection):
                return typeSelection

            if case(Action.Greeting):
                return greeting

            if case(Action.UnknownAction):
                return unknownAction

            if case():
                raise KeyError()

    @staticmethod
    def handle(action, request, args):
        """
        Handle an action request
        Return:
            the result from the action
        """
        actionHandler = DialogueManager.getHandler(action)
        return actionHandler(request.session, args)

