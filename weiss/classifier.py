import nltk
import sys
import math
import os

from webapps.settings import BASE_DIR

def stemming(sentences):
	"""	
		Input:  a list of cleaned sentences (i.e. stop words removed)
		Output: a list of sentenses with tokens stemed,
	"""
	porter = nltk.PorterStemmer()
	stemedSentences = []
	for i in xrange(0,len(sentences)):
		#print "Processing sentence: ", sentence
		tokens = nltk.word_tokenize(sentences[i])
		stemedTokens = [porter.stem(t) for t in tokens]
		stemedSentences += [' '.join(stemedTokens)]
	return stemedSentences

def stopword_removal(sentence):
	stopwords = set(["comment","opinion","view","review","can","give","me","you","i","tell"])
	clean_sentence = []
	tokens = nltk.word_tokenize(sentence)
	for i in xrange(0,len(tokens)):
		if (tokens[i].strip("s")).lower() in stopwords:
			tokens[i] = ''
	clean_sentence += [' '.join(tokens).strip()]
	return clean_sentence

def naive_train(train):
	counts = {}
	vocab = set()
	for line in open(os.path.abspath(BASE_DIR + "/weiss/%s" % train)):
		tag,body = line.split("\t")
		counts.setdefault(tag,0)
		counts.setdefault("all",0)
		counts[tag] += 1
		counts["all"] += 1

		tokens = nltk.word_tokenize(body)

		for t in tokens:
			counts.setdefault(tag+","+t,0)
			counts[tag+","+t] += 1
			vocab.add(t)
		counts.setdefault(tag+",*",0)
		counts[tag+",*"] += len(tokens)
	counts["vocab"] = len(vocab)
	#print str(len(vocab))
	#print counts

	return counts

def naive_classify(query,counts):
	actions = ["1","2","3","4","5"]
	probabilities = []
	for a in actions:
		result = math.log((counts[a]+1.0)/(len(actions)+counts["all"]+0.0))
		tokens = nltk.word_tokenize(query)
		for t in tokens:
			if a+","+t not in counts:
				count = 0
			else:
				count = counts[a+","+t]
			result += math.log((1.0+count)/(counts["vocab"]+counts[a+",*"]+0.0))
		probabilities.append(result)
	return actions[probabilities.index(max(probabilities))]


def actionMapping(query):
	trainfile = "training"

	counts = naive_train(trainfile)

	action = naive_classify(query,counts)

	return action
