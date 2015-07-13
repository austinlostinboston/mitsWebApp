"""
dialogue Mnager

this class is responsible for
    1. loop up action executor by action
    2. handle an request
    3. dispatch a requset based on query

Author: Ming Fang <mingf@cs.cmu.edu>
"""

import logging
from weiss.models import Action
from weiss.utils.switch import switch
from weiss.dialogue.actions import *
from weiss.dialogue.actionUtil import initNewLine, flushNewLine
from weiss.flows.factory import getFlowManager
from weiss.classifier.factory import getClassifier

logger = logging.getLogger(__name__)

class DialogueManager(object):

    def __init__(self):
        self._classifier = getClassifier()
        self._fmgr = getFlowManager()

    @property
    def classifier(self):
        return self._classifier

    @property
    def fmgr(self):
        return self._fmgr

    def getExecutor(self, action):
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
                raise KeyError("No such action %s" % action)

    def handle(self, request):
        """
        handle a request from user, will call dispatch
        """
        query = str(request.POST.get('queryinput', False))
        logger.debug("query:%s" % query)

        curr_state = self.fmgr.lookUp(request.user)

        args = self.classifier.action_info(query, curr_state)

        self.dispatch(request, query, args)
        return

    def dispatch(self, request, query, args):
        """
        dispatch a request based on query
        """
        action = Action(args['aid'])
        logger.debug(action.name)
        actioninput = ""

        # make a state transition
        self.fmgr.transit(request, action)

        if query is None:
            query = action.name + " : " + args['keywords']

        logger.debug("Dispatch action: %s, %s, %s" % (action.value, action.name, actioninput))

        initNewLine(request.session, query, action.value)

        actionExecutor = self.getExecutor(action)

        response = actionExecutor(request.session, args)

        flushNewLine(request, response)

        return



