'''
Provide singleton for Classifier

Author: Ming Fang
'''

from weiss.classifier.classifier import Classifier

_instance = None

def getClassifier():
    global _instance
    if _instance is None:
        _instance = Classifier()
    return _instance

