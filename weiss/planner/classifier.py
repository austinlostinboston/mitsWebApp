"""
This script is the main entry for classifier.
It does action classification and extract keywords from the incoming query.
===========================================================================

TODO(wenjunw@cs.cmu.edu):
- Reconsider the type words
- Consider action 6,7,8 in one query
- log force change of aid
- update _type_recognition function

Usage: refer to demo.py
Dependency: numpy, scipy, sklearn

Author: Wenjun Wang<wenjunw@cs.cmu.edu>
Date: July 1, 2015
"""
import pickle
<<<<<<< HEAD
import nltk
<<<<<<< HEAD
<<<<<<< HEAD
=======
import string
>>>>>>> b54bb32... update classifier
=======
>>>>>>> a533c0f... add heuristic rules
=======
>>>>>>> 6d991c7... a lot of bugs fixed
import timeit
import logging
import os


from sklearn.externals import joblib
from liblinearutil import *
from webapps.settings import BASE_DIR
from weiss.planner.feature import *
from weiss.models import Action

logger = logging.getLogger(__name__)


class Classifier(object):
    modeldir = os.path.abspath(BASE_DIR + "/weiss/planner/models/")
    stopword_path = modeldir + "/english.stp"

    def __init__(self):
        """
        All variables which would be used by every query classification and parsing are listed here.
        Only need to create Classifier object once, i.e. initialize once
        """
        start = timeit.timeit()
        self.action_model, self.type_model = self._get_model()
        self.stopwords = stopword(self.stopword_path)
        self.feature_list = self._get_feature_list()
        end = timeit.timeit()
        print "Load time: " + str(end - start)
        self.feature_arg = parse_options('-uni -pos2 -stem -stprm')
        self.labels = [1, 2, 3, 4, 5, 6, 7]

    def _get_model(self):
        """Load model

        This function is called during initialization

        Return: models, action model and type model
        """
        m1 = load_model(self.modeldir + '/action_model')
        m2 = joblib.load(self.modeldir + '/type_model')
        return m1, m2


    def _get_feature_list(self):
        """Load feature file

        This function is called during initialization

        Return: Feature list
        """
        with open(self.modeldir + '/action_features', 'r') as infile:
            feature_list = pickle.load(infile)
            return feature_list

    def _convert_query_to_dictionary(self, query):
        """Convert each user query to the format required by LibLINEAR

        Args and Need:
            query: the raw query, like 'What do people think of ?'
            self.feature_list: a list of unique features generated by function feature_generator

        Return:
            Convert user's query: store information in a dictionary,
            which is a member of a list.
        """
        features = feature_generator(query, self.stopwords, self.feature_arg)
        onerow = {}
        for f in features:
            try:
                onerow[self.feature_list.index(f) + 1] = 1
            except ValueError:
                pass

        return [onerow]

    def classify(self, query):
        """Does query classification, which decides which action need to be taken

        This function is called by self.action_info

        Return: Action id
        """
        x = self._convert_query_to_dictionary(query)
        p_label, p_val = predict(self.labels, x, self.action_model, '-b 0')
        if p_val[0][int(p_label[0]) - 1] == 0:
            p_label[0] = 10

        return Action(int(p_label[0]))  # API changes here
<<<<<<< HEAD

    def action_info(self, query, flow):
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
        plausible = state.nextPossibleActions
        # query = unicode(query,errors='ignore')

        for case in switch(state.sid):
            if case(State.SystemInitiative):
                self._system_initiative(query, arguments)
            elif case(State.TypeSelected):
                self._type_selected(query, arguments)
            elif case(State.RangeSelected):
                step = state.step
                self._range_selected(query, arguments, step, flow.entities)
            elif case(State.EntitySelected):
                self._entity_selected(query, arguments)
            elif case(State.CommentSelected):
                self._comment_selected(query, arguments)
            elif case():
                logger.error("No such state" + state)
                pass

        return arguments

    def _entity_recognition(self, query, arguments):
        """Parse query and extract keywords

        This function is called by self.action_info

        Args:
            query: query needs to be parsed
            arguments: info needs to be updated
        """
        tokens = nltk.word_tokenize(query)
        tags = self.postagger.tag(tokens)

        entities = nltk.chunk.ne_chunk(tags)
        # print entities

        tuples = []
        trees = []
        for i in entities:
            if isinstance(i, tuple):
                if ((i[1][:2] == 'NN' or i[1][:2] == 'JJ')
                    and i[0].lower() not in self.stopwords
                    and self.stemmer.stem(i[0]) not in self.type_words['movie']
                    and self.stemmer.stem(i[0]) not in self.type_words['article']
                    and self.stemmer.stem(i[0]) not in self.type_words['restaurant']):
                    tuples.append(i[0])
            elif isinstance(i, nltk.tree.Tree):
                phrase = []
                for element in i:
                    if element[0].lower() not in self.stopwords:
                        phrase.append(element[0])
                if len(phrase) > 0:
                    trees.append(' '.join(phrase))

        if len(trees) > 0:
            arguments['keywords'] = '#'.join(trees).strip('#')
        elif len(tuples) > 0:
            arguments['keywords'] = '#'.join(tuples).strip('#')

    def _set_type_words(self):
        """Initialize synonymy words of movie, article and restaurant

        This function is called during initialization

        Return: A dictionary, key: movie, article, restaurant, value: their synonymy words
        """
        topic = {}
        movie = ['cinema', 'show', 'film', 'picture', 'cinematograph',
                 'videotape', 'flick', 'pic', 'cine', 'cinematics', 'photodrama',
                 'photoplay', 'talkie', 'flicker', 'DVD', 'movie']
        article = ['report', 'announcement', 'story', 'account',
                   'newscast', 'headlines', 'press', 'communication', 'talk', 'word',
                   'communique', 'bulletin', 'message', 'dispatch', 'broadcast',
                   'statement', 'intelligence', 'disclosure', 'revelation',
                   'gossip', 'dispatch', 'news', 'article']
        restaurant = ['bar', 'cafeteria', 'diner', 'dining', 'saloon', 'coffeehouse',
                      'canteen', 'chophouse', 'drive-in', 'eatery', 'grill', 'lunchroom', 'inn', 'food',
                      'pizzeria', 'hideaway', 'cafe', 'charcuterie', 'deli', 'restaurant']
        for m in movie:
            topic.setdefault('movie', set([]))
            topic['movie'].add(self.stemmer.stem(m))
        for a in article:
            topic.setdefault('article', set([]))
            topic['article'].add(self.stemmer.stem(a))
        for r in restaurant:
            topic.setdefault('restaurant', set([]))
            topic['restaurant'].add(self.stemmer.stem(r))
        return topic

    def _type_recognition(self, query, arguments):
        """Identity the type of the topic: movie, article or restaurant

        This is called by self.action_info

        Args:
            query: query needs to be parsed
            arguments: info needs to be updated

        """
        query = query.translate(string.maketrans("", ""), string.punctuation)
        tokens = nltk.word_tokenize(query)
        first = self.stemmer.stem(tokens[0])
        last = self.stemmer.stem(tokens[-1])
        lastsecond = self.stemmer.stem(tokens[-2]) if len(tokens) > 1 else "toy"
        if (first in self.type_words['article'] or last in self.type_words['article']
            or lastsecond in self.type_words['article']):
            arguments['tid'] = Type.News
        elif (first in self.type_words['restaurant'] or last in self.type_words['restaurant']
              or lastsecond in self.type_words['restaurant']):
            arguments['tid'] = Type.Restaurant
        elif (first in self.type_words['movie'] or last in self.type_words['movie']
              or lastsecond in self.type_words['movie']):
            arguments['tid'] = Type.Movie
        else:
            arguments['tid'] = Type.Unknown

    @staticmethod
    def _string_to_idx(number):
        if number == 'first' or number == 'one':
            return 0
        if number == 'second' or number == 'two':
            return 1
        if number == 'third' or number == 'three':
            return 2
        if number == 'fourth' or number == 'four':
            return 3
        if number == 'fifth' or number == 'five':
            return 4

    @staticmethod
    def _keyword_matching(arguments, entities):
        words = arguments['keywords'].split("#")
        phrase = " ".join(words).strip()

        for i in xrange(0, len(entities)):
            if entities[i].find(phrase) != -1:
                arguments['idx'] = i
                break

    def _find_number(self, query, arguments, entities):
        tokens = nltk.word_tokenize(query)
        tags = self.postagger.tag(tokens)
        last = query.find('last')

        number = None
        for t in tags:
            logger.debug(t[1])
            if t[1] == 'JJ' and t[0][-2:] in set(['th', 'nd', 'st']):
                number = t[0]
            elif t[1] == 'CD':
                number = t[0]
            elif t[1] == 'LS':
                arguments['idx'] = int(t[0]) - 1

        if number is not None:
            if last == -1:
                arguments['idx'] = self._string_to_idx(number.lower())
            else:
                arguments['idx'] = len(entities) - self._string_to_idx(number.lower()) - 1

    def _system_initiative(self, query, arguments):
        self._type_recognition(query, arguments)
        self._entity_recognition(query, arguments)
        if 'keywords' in arguments:
            arguments['aid'] = Action.EntitySelection
        else:
            if arguments['tid'] != Type.Unknown:
                arguments['aid'] = Action.TypeSelection
            else:
                arguments['aid'] = Action.UnknownAction

    def _type_selected(self, query, arguments):
        self._type_recognition(query, arguments)
        self._entity_recognition(query, arguments)
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
            self._type_recognition(query, arguments)
            if arguments['tid'] == Type.Unknown:
                arguments['aid'] = Action.UnknownAction
            else:
                arguments['aid'] = Action.TypeSelection
        elif step == Step.TypeSelected:
            logger.debug("TypeSelected")
            query = query.lower()
            self._find_number(query, arguments, entities)
            if 'idx' not in arguments:
                self._entity_recognition(query, arguments)
                self._keyword_matching(arguments, entities)
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
        self._type_recognition(query, arguments)
        action = self._classify(query)
        if action == Action.EntitySelection:
            self._entity_recognition(query, arguments)
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
            tokens = nltk.word_tokenize(query.lower())
            score = 0
            for token in tokens:
                if token in self.sentiment:
                    score += self.sentiment[token]
<<<<<<< HEAD
            if score < -1:arguments['aid'] = Action.NextNegativeComment
            if score > 1:arguments['aid'] = Action.NextPositiveComment
=======
            if score < -1: arguments['aid'] = Action.NextNegativeComment
            if score > 1: arguments['aid'] = Action.NextPositiveComment
<<<<<<< HEAD:weiss/classifier/classifier.py
>>>>>>> 6d991c7... a lot of bugs fixed
=======
        else:
            arguments['aid'] = action
>>>>>>> 0f60d68... classifier seems working and does major refactor for classifiers:weiss/planner/classifier.py
=======
>>>>>>> 35e14f1... refactor
