from weiss.planner.classifier import Classifier
from weiss.planner.parser import Parser

from weiss.models import State, Type, Action, Step
from weiss.utils.switch import switch

import logging

logger = logging.getLogger(__name__)

class Planner(object):
    def __init__(self):
        self._parser = Parser()
        self._classifier = Classifier()

    def plan(self, query, flow):
        """API function in this script. Gives all info of an action

        This is the only function which will be called outside this script.

        Args:
            query: query need to classify and parse
            state: current state, which contains every thing about this state

        Return:
            arguments: a dictionary contains all the info needed by calling function

        """
        arguments = {}
        state = flow.state
        # plausible = state.nextPossibleActions
        # query = unicode(query,errors='ignore')

        for case in switch(state.sid):
            if case(State.SystemInitiative):
                self._system_initiative(query, arguments)
            elif case(State.TypeSelected):
                self._type_selected(query, arguments)
            elif case(State.RangeSelected):
                step = state.step
                entities = flow.entities
                self._range_selected(query, arguments, step, entities)
            elif case(State.EntitySelected):
                self._entity_selected(query, arguments)
            elif case(State.CommentSelected):
                self._comment_selected(query, arguments)
            elif case():
                logger.error("No such state" + state)

        return arguments


    def _system_initiative(self, query, arguments):
        self._parser.type_recognition(query, arguments)
        self._parser.entity_recognition(query, arguments)
        if 'keywords' in arguments:
            arguments['aid'] = Action.EntitySelection
        else:
            if arguments['tid'] != Type.Unknown:
                arguments['aid'] = Action.TypeSelection
            else:
                arguments['aid'] = Action.UnknownAction


    def _type_selected(self, query, arguments):
        self._parser.type_recognition(query, arguments)
        self._parser.entity_recognition(query, arguments)
        if 'keywords' in arguments:
            arguments['aid'] = Action.EntitySelection
        else:
            if arguments['tid'] == Type.Unknown:
                arguments['aid'] = Action.UnknownAction
            elif query.find('recommend') != -1 or query.find('suggest') != -1:
                arguments['aid'] = Action.NextRandomEntity
            else:
                arguments['aid'] = Action.TypeSelection


    def _range_selected(self, query, arguments, step, entities):
        if step == Step.RangeInitiative:
            logger.debug("RangeInitiative")
            self._parser.type_recognition(query, arguments)
            if arguments['tid'] == Type.Unknown:
                arguments['aid'] = Action.UnknownAction
            else:
                arguments['aid'] = Action.TypeSelection
        elif step == Step.TypeSelected:
            logger.debug("TypeSelected")
            query = query.lower()
            self._parser.find_number(query, arguments, entities)
            if 'idx' not in arguments:
                self._parser.entity_recognition(query, arguments)
                self._parser.keyword_matching(arguments, entities)
            if 'idx' in arguments:
                arguments['aid'] = Action.EntityConfirmation
            else:
                arguments['aid'] = Action.UnknownAction


    def _entity_selected(self, query, arguments):
        self._entity_or_comment_selected_helper(query, arguments)

        if arguments['aid'] == Action.NextOppositeComment:
            arguments['aid'] = Action.NextRandomComment


    def _comment_selected(self, query, arguments):
        self._entity_or_comment_selected_helper(query, arguments)


    def _entity_or_comment_selected_helper(self, query, arguments):
        self._parser.type_recognition(query, arguments)
        action = self._classifier.classify(query)
        if action == Action.EntitySelection:
            self._parser.entity_recognition(query, arguments)
            if 'keywords' not in arguments:
                if arguments['tid'] != Type.Unknown:
                    arguments['aid'] = Action.TypeSelection
                else:
                    if query.find('another') != -1 or query.find('recommend') != -1 or query.find('suggest') != -1:
                        arguments['aid'] = Action.NextRandomEntity
                    else:
                        arguments['aid'] = Action.UnknownAction
            else:
                arguments['aid'] = Action.EntitySelection
        elif action == Action.NextRandomComment:
            sentiment = self._parser.calculate_sentiment(query)
            logger.debug(sentiment)
            if sentiment < -1: 
                arguments['aid'] = Action.NextNegativeComment
            elif sentiment > 1: 
                arguments['aid'] = Action.NextPositiveComment
        else:
            arguments['aid'] = action