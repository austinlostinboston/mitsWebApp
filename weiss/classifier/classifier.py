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
import os
import pickle
import nltk
<<<<<<< HEAD
=======
import string
>>>>>>> b54bb32... update classifier
import timeit
import string

from webapps.settings import BASE_DIR
from weiss.classifier.feature import *
from weiss.flows.states import *
from nltk.tag.stanford import StanfordPOSTagger
from sklearn.externals import joblib
from liblinearutil import *

class Classifier(object):
    modeldir = os.path.abspath(BASE_DIR + "/weiss/classifier/models/")
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
        self.stemmer = nltk.SnowballStemmer("english")
        self.sentiment = self._get_sentiment()
        end = timeit.timeit()
        print "Load time: " + str(end-start)
        self.feature_arg = parse_options('-uni -pos2 -stem -stprm')
        self.type_words = self._set_type_words()
        self.labels = [1,2,3,4,5,6,7]

    def _get_model(self):
        """Load model

        This function is called during initialization

        Return: models, action model and type model
        """
        m1 = load_model(self.modeldir + '/action_model')
        m2 = joblib.load(self.modeldir + '/type_model')
        return m1, m2

    def _get_sentiment(self):
        sentiment = {}
        for line in open(self.modeldir + "/AFINN.txt"):
            word, score = line.split('\t')
            sentiment[word] = int(score)
        return sentiment

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
                onerow[self.feature_list.index(f)+1] = 1
            except ValueError:
                pass

        return [onerow]

    def _classify(self, query):
        """Does query classification, which decides which action need to be taken

        This function is called by self.action_info

        Return: Action id
        """
        x = self._convert_query_to_dictionary(query)
        p_label, p_val = predict(self.labels, x, self.action_model, '-b 0')
        if p_val[0][int(p_label[0])-1] == 0:
            p_label[0] = 10

        return int(p_label[0]) # API changes here

    def action_info(self, query, state):
        """API function in this script. Gives all info of an action

        This is the only function which will be called outside this script.

        Args:
            query: query need to classify and parse
            state: current state, which contains every thing about this state

        Return:
            arguments: a dictionary contains all the info needed by calling function

        """
        arguments = {}
        plausible = state.getNextPossibleActions()
        self._type_recognition(query, arguments)
        temp = arguments['aid']
        # State System Initiative and State Type Selected
        # TODO<wenjunw@cs.cmu.edu>:
        # Reconsider the logic for SystemInitiative and TypeSelected
        if state is SystemInitiative or state is TypeSelected:
            q = list2Vec(hashit(query))
            arguments['tid'] = int(self.type_model.predict(q)[0])
            self._entity_recognition(query,arguments)
            if 'keywords' in arguments:
                arguments['aid'] = 7
            else:
                if temp != 8:
                    if 5 in plausible:
                        arguments['aid'] = 5
                    else:
                        arguments['aid'] = 10
                else:
                    if query.find('another') != -1:
                        # TODO<wenjunw@cs.cmu.edu>:
                        # Need to think about this heuristic later how to differentiate 5,7,8
                        # Or do we still allow action 5?
                        arguments['aid'] = 5
        # State Entity Selected and State Comment Selected
        else:
            arguments['aid'] = self._classify(query)
            if arguments['aid'] == 7:
                self._entity_recognition(query,arguments)
                if 'keywords' not in arguments:
                    if temp == 10:
                        arguments['aid'] = 5
                    else:
                        arguments['aid'] = 8
            elif arguments['aid'] == 5:
                # TODO<wenjunw@cs.cmu.edu>:
                # Need to think about this heuristic later how to differentiate 5,7,8
                if temp == 8 and query.find('another') == -1:
                    arguments['aid'] = 8
            elif arguments['aid'] == 2 and 2 not in plausible:
                arguments['aid'] = 1
            elif arguments['aid'] == 1:
                tokens = nltk.word_tokenize(query.lower())
                score = 0
                for token in tokens:
                    if token in self.sentiment:
                        score += self.sentiment[token]
                if score < -1:arguments['aid'] = 4
                if score > 1:arguments['aid'] = 3

        return arguments

    def _entity_recognition(self, query, arguments):
        """Parse query and extract keywords

        This function is called by self.action_info

        Args:
            query: query needs to be parsed
            arguments: info needs to be updated
        """
        tokens = nltk.word_tokenize(query)
        postagger = StanfordPOSTagger(self.modeldir+'/postagger/models/english-bidirectional-distsim.tagger', 
                                self.modeldir+'/postagger/stanford-postagger.jar')
        tags = postagger.tag(tokens)

        entities = nltk.chunk.ne_chunk(tags)
        if 'aid' not in arguments:
            arguments['aid'] = 7
        #print entities

        tuples = []
        trees = []
        for i in entities:
            if isinstance(i,tuple):
                if ((i[1][:2] == 'NN' or i[1][:2] == 'JJ')
                    and i[0].lower() not in self.stopwords
                    and self.stemmer.stem(i[0]) not in self.type_words['movie']
                    and self.stemmer.stem(i[0]) not in self.type_words['article']
                    and self.stemmer.stem(i[0]) not in self.type_words['restaurant']):
                    tuples.append(i[0])
            elif isinstance(i,nltk.tree.Tree):
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
        movie = ['cinema','show','film','picture','cinematograph',
            'videotape','flick','pic','cine','cinematics','photodrama',
            'photoplay','talkie','flicker','DVD','movie']
        article = ['report','announcement','story','account',
            'newscast','headlines','press','communication','talk','word',
            'communique','bulletin','message','dispatch','broadcast',
            'statement','intelligence','disclosure','revelation',
            'gossip','dispatch','news','article']
        restaurant = ['bar','cafeteria','diner','dining','saloon','coffeehouse',
            'canteen','chophouse','drive-in','eatery','grill','lunchroom','inn','food',
            'pizzeria','hideaway','cafe','charcuterie','deli','restaurant']
        for m in movie:
            topic.setdefault('movie',set([]))
            topic['movie'].add(self.stemmer.stem(m))
        for a in article:
            topic.setdefault('article',set([]))
            topic['article'].add(self.stemmer.stem(a))
        for r in restaurant:
            topic.setdefault('restaurant',set([]))
            topic['restaurant'].add(self.stemmer.stem(r))
        return topic

    def _type_recognition(self, query, arguments):
        """Identity the type of the topic: movie, article or restaurant

        This is called by self.action_info

        Args:
            query: query needs to be parsed
            arguments: info needs to be updated

        """
        query = query.translate(string.maketrans("",""),string.punctuation)
        tokens = nltk.word_tokenize(query)
        arguments['aid'] = 8
        first = self.stemmer.stem(tokens[0])
        last = self.stemmer.stem(tokens[-1])
        lastsecond = self.stemmer.stem(tokens[-2]) if len(tokens) > 1 else "toy"
        if (first in self.type_words['article'] or last in self.type_words['article']
            or lastsecond in self.type_words['article']):
            arguments['tid'] = 1
        elif (first in self.type_words['restaurant'] or last in self.type_words['restaurant'] 
            or lastsecond in self.type_words['restaurant']):
            arguments['tid'] = 2
        elif (first in self.type_words['movie'] or last in self.type_words['movie'] 
            or lastsecond in self.type_words['movie']):
            arguments['tid'] = 3
        else:
            arguments['aid'] = 10
