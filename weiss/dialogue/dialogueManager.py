"""
dialogue Mnager

this class is responsible for
    1. loop up action executor by action
    2. handle an request
    3. dispatch a requset based on query

Author: Ming Fang <mingf@cs.cmu.edu>
"""

from weiss.dialogue.actions import *
from weiss.dialogue.actionUtil import initNewLine, flushNewLine
from weiss.dialogue.responseGenerator import responseHandler
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
        :rtype : method
        """
        for case in switch(action):
            if case(Action.NextRandomComment):
                return nextRandomCmt

            if case(Action.NextOppositeComment):
                return nextRandomOppositeCmt

            if case(Action.NextNegativeComment):
                return nextRandomNegativeCmt

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

            if case(Action.EntityConfirmation):
                return entityConfirmation

            if case():
                raise KeyError("No such action %s" % action)

    def handle(self, request):
        """
        handle a request from user, will call dispatch
        """
        query = str(request.POST.get('queryinput', False))
        logger.debug("query:%s" % query)

        flow = self.fmgr.lookUp(request.user)
        flow.request = request

        decision = self.classifier.action_info(query, flow)

        self.dispatch(flow, query, decision)
        return

    def dispatch(self, flow, query, decision):
        """
        dispatch a request based on query
        """
        flow.action = Action(decision['aid'])
        request = flow.request
        action = flow.action
        logger.debug(action.name)

        if query is None:
            query = action.name + " : " + decision['keywords']

        logger.debug("Dispatch action: %s, %s" % (action.value, action.name))

        initNewLine(request.session, query, action)

        actionExecutor = self.getExecutor(action)

        actionExecutor(flow, decision)  # transition happens inside

        response = responseHandler(flow)

        flushNewLine(request, response)

        return
