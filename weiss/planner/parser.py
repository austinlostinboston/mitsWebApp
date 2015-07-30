from webapps.settings import BASE_DIR
from nltk.tag.stanford import StanfordPOSTagger
from weiss.planner.feature import stopword
from weiss.models import Type

import nltk
import logging
import os

logger = logging.getLogger(__name__)

class Parser(object):
    modeldir = os.path.abspath(BASE_DIR + "/weiss/planner/models/")
    stopword_path = modeldir + "/english.stp"

    def __init__(self):
        self._postagger = StanfordPOSTagger(self.modeldir + '/postagger/models/english-bidirectional-distsim.tagger',
                                           self.modeldir + '/postagger/stanford-postagger.jar')
        self._stemmer = nltk.SnowballStemmer("english")
        self._stopwords = stopword(self.stopword_path)
        self._type_words = self._set_type_words()
        self._sentiment = self._get_sentiment()


    def _get_sentiment(self):
        sentiment = {}
        for line in open(self.modeldir + "/AFINN.txt"):
            word, score = line.split('\t')
            sentiment[word] = int(score)
        return sentiment


    def calculate_sentiment(self,query):
    	tokens = nltk.word_tokenize(query)
        score = 0
        for token in tokens:
            if token in self._sentiment:
                score += self._sentiment[token]
        return score


    def entity_recognition(self, query, arguments):
        """Parse query and extract keywords

        This function is called in planner

        Args:
            query: query needs to be parsed
            arguments: info needs to be updated
        """
        tokens = nltk.word_tokenize(query)
        tags = self._postagger.tag(tokens)

        tuples = []

        for i in tags:
            if ((i[1][:2] == 'NN' or i[1][:2] == 'JJ')
                and i[0] not in self._stopwords
                and self._stemmer.stem(i[0]) not in self._type_words['movie']
                and self._stemmer.stem(i[0]) not in self._type_words['article']
                and self._stemmer.stem(i[0]) not in self._type_words['restaurant']):
                tuples.append(i[0])

        if len(tuples) > 0:
            arguments['keywords'] = tuples
            logger.info("Here are the keywords: %s" % arguments['keywords'])


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
            topic['movie'].add(self._stemmer.stem(m))
        for a in article:
            topic.setdefault('article', set([]))
            topic['article'].add(self._stemmer.stem(a))
        for r in restaurant:
            topic.setdefault('restaurant', set([]))
            topic['restaurant'].add(self._stemmer.stem(r))
        return topic


    def type_recognition(self, query, arguments):
        """Identity the type of the topic: movie, article or restaurant

        This is called in planner

        Args:
            query: query needs to be parsed
            arguments: info needs to be updated

        """
        tokens = nltk.word_tokenize(query)
        first = self._stemmer.stem(tokens[0])
        last = self._stemmer.stem(tokens[-1])
        lastsecond = self._stemmer.stem(tokens[-2]) if len(tokens) > 1 else "toy"
        if (first in self._type_words['article'] or last in self._type_words['article']
            or lastsecond in self._type_words['article']):
            arguments['tid'] = Type.News
        elif (first in self._type_words['restaurant'] or last in self._type_words['restaurant']
              or lastsecond in self._type_words['restaurant']):
            arguments['tid'] = Type.Restaurant
        elif (first in self._type_words['movie'] or last in self._type_words['movie']
              or lastsecond in self._type_words['movie']):
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
    def keyword_matching(arguments, entities):
        words = arguments['keywords']
        phrase = " ".join(words).strip()
        logger.info("confirmed keywords: %s" % phrase)

        for i in xrange(0, len(entities)):
            entity_name = entities[i].name.lower()
            logger.info("entity_name: %s" % entity_name)
            if entity_name.find(phrase) != -1:
                arguments['idx'] = i
                break


    def find_number(self, query, arguments, entities):
        tokens = nltk.word_tokenize(query)
        tags = self._postagger.tag(tokens)
        last = query.find('last')

        # Edge case, "first" cannot be tagged correctly
        if len(query.split(" ")) <= 3 and query.find('first') != -1:
            arguments['idx'] = 0
            return 

        number = None
        for t in tags:
            if t[1] == 'JJ' and t[0][-2:] in set(['th', 'nd', 'st', 'rd']):
                number = t[0]
                break
            elif t[1] == 'CD':
                number = t[0]
                if number.isdigit():
                	arguments['idx'] = int(number) - 1
                	return
                break

        if number is not None:
            if last == -1:
                arguments['idx'] = self._string_to_idx(number)
            else:
                arguments['idx'] = len(entities) - self._string_to_idx(number) - 1
