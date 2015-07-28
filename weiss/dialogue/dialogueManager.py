"""
dialogue Mnager

this class is responsible for
    1. loop up action executor by action
    2. handle an request
    3. dispatch a requset based on query

Author: Ming Fang <mingf@cs.cmu.edu>
"""

from weiss.dialogue.actions import *
from weiss.dialogue.responseGenerator import responseHandler
from weiss.flows.factory import getFlowManager
from weiss.planner.factory import getPlanner
from weiss.utils.switch import switch

from django.utils import timezone

from weiss.models import History

import HTMLParser
import datetime

logger = logging.getLogger(__name__)


class DialogueManager(object):
    def __init__(self):
        self._planner = getPlanner()
        self._fmgr = getFlowManager()
        self._html_parser = HTMLParser.HTMLParser()

    @property
    def planner(self):
        return self._planner

    @property
    def fmgr(self):
        return self._fmgr

    @property
    def html_parser(self):
        return self._html_parser

    def getExecutor(self, action):
        """return action handler according to action
        :param action Action enum
        :rtype : method
        """
        for case in switch(action):
            if case(Action.NextRandomComment):
                return nextRandomCmt

            elif case(Action.NextOppositeComment):
                return nextRandomOppositeCmt

            elif case(Action.NextNegativeComment):
                return nextRandomNegativeCmt

            elif case(Action.NextPositiveComment):
                return nextRandomPositiveCmt

            elif case(Action.NextRandomEntity):
                return nextRandomEntity

            elif case(Action.SentimentStats):
                return sentimentStats

            elif case(Action.EntitySelection):
                return entitySelection

            elif case(Action.TypeSelection):
                return typeSelection

            elif case(Action.Greeting):
                return greeting

            elif case(Action.UnknownAction):
                return unknownAction

            elif case(Action.EntityConfirmation):
                return entityConfirmation

            elif case(Action.NextSummary):
                return next_summary

            elif case(Action.NextPositiveSummary):
                return next_positive_summary

            elif case(Action.NextNegativeSummary):
                return next_negative_summary

            elif case(Action.NextPositiveSummary):
                return next_opposite_summary

            elif case():
                raise KeyError("No such action %s" % action)

    def handle(self, request, query_obj=None):
        """Handle a request from user, will call dispatch
        """
        if query_obj is not None:
            query = query_obj.query
        else:
            query = str(request.POST.get('queryinput', False))
        logger.debug("query:%s" % query)

        flow = request.session.get('flow', None)

        if flow is None:
            logger.debug("No such flow %s" % query_obj)
            return None

        decision = self.planner.plan(query, flow)
        self.dispatch(flow, query, decision)

        flow.save_into(request)
        return flow

    def dispatch(self, flow, query, decision):
        """Dispatch a request based on query
        """
        flow.action = decision['aid']
        action = flow.action
        logger.debug(action.name)

        if query is None:
            query = action.name + " : " + decision['keywords']

        logger.debug("Dispatch action: %s, %s" % (action.value, action.name))

        flow.start_line(action, query)

        executor = self.getExecutor(action)

        executor(flow, decision)  # transition happens inside

        response = responseHandler(flow)

        flow.end_line(response)

        return

    def start_new_dialogue(self, request):
        flow = self.fmgr.new(request)
        greeting_executor = self.getExecutor(Action.Greeting)
        greeting_executor(flow, None)
        response = responseHandler(flow)
        flow.start_line(Action.Greeting)
        flow.end_line(response)
        flow.save_into(request)
        return flow

    def end_dialogue(self, user):
        self.fmgr.delete(user)

    def get_dialogue(self, user_id, limit=10):
        ten_min_ago = timezone.now() - datetime.timedelta(minutes=10)  # 10 min ago
        lines = History.objects.filter(Q(userid=user_id), Q(time__gt=ten_min_ago)).order_by("-time")[:limit]
        if len(lines) == 0:
            # If no line in the last 10 min, relax the time constraint
            lines = History.objects.filter(Q(userid=user_id)).order_by("-time")[:1]
        num_greeting = 0
        # Do not show multiple Greeting
        for line in reversed(lines):
            if line.aid.aid != Action.Greeting.value:
                break
            num_greeting += 1

        # more than 1 greeting
        if num_greeting > 1:
            num_greeting -= 1 # keep at least one
            num_keep = len(lines) - num_greeting
            lines = lines[:num_keep]

        for line in lines:
            line.response = self.html_parser.unescape(line.response)
        return lines
