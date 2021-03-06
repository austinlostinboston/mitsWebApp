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

from weiss.planner.classifier import Classifier
from weiss.planner.parser import Parser

from weiss.models import State, Type, Action, Step
from weiss.utils.switch import switch

import logging
import string
import fuzzy

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
        query = query.lower()
        query = query.decode('utf8','ignore').encode('ascii','ignore')
        query = query.translate(string.maketrans("", ""), string.punctuation)

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
            logger.info("RangeInitiative")
            self._parser.type_recognition(query, arguments)
            if arguments['tid'] == Type.Unknown:
                arguments['aid'] = Action.UnknownAction
            else:
                arguments['aid'] = Action.EntityConfirmation
        elif step == Step.TypeSelected:
            logger.info("TypeSelected")
            self._parser.type_recognition(query, arguments)
            if arguments['tid'] != Type.Unknown:
                arguments['aid'] = Action.TypeSelection
            else:
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

        if arguments['aid'] == Action.NextOppositeSummary:
            arguments['aid'] = Action.NextSummary


    def _comment_selected(self, query, arguments):
        self._entity_or_comment_selected_helper(query, arguments)


    def _entity_or_comment_selected_helper(self, query, arguments):
        self._parser.type_recognition(query, arguments)
        arguments['aid'] = self._classifier.classify(query)

        if arguments['aid'] == Action.EntitySelection:
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
        elif arguments['aid'] == Action.NextSummary:
            sentiment = self._parser.calculate_sentiment(query)
            logger.info(sentiment)
            if sentiment < -1: 
                arguments['aid'] = Action.NextNegativeSummary
            elif sentiment > 1: 
                arguments['aid'] = Action.NextPositiveSummary