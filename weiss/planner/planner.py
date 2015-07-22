from weiss.planner.classifier import Classifier
from weiss.planner.parser import Parser




class Planner(object):

    def __init__(self):
        self._classifier = Classifier()
        self._parser = Parser()

    @property
    def classifier(self):
        return self._classifier

    @property
    def parser(self):
        return self._parser

    def plan(self, query, flow):
        return self.classifier.action_info(query, flow)

