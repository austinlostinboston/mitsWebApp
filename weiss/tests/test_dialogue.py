from django.test import TestCase
from weiss.classifier.factory import getClassifier
from weiss.flows.factory import getFlowManager
from weiss.tests.testUtils import *
from webapps.settings import BASE_DIR


class Case(object):

    def __init__(self, line):
        self.ID = int(line[0])
        self.query = line[1]
        self.curr_sid = int(line[2])
        self.expected = int(line[3])
        self.classifier = getClassifier()
        self.fmgr = getFlowManager()
        self.curr_state = self.fmgr.lookUp(self.curr_sid)
        self.actual = None
        self.isDone = False

    def run(self):
        self.actual = self.classifier.action_info(self.query, self.curr_state)
        self.isDone = True

    def __str__(self):
        if self.check():
            return PASSED + " ID: %s, query: %s, curr_state: %s, expected: %s, actual: %s" % (self.ID, self.query, self.curr_state, self.expected, self.actual)
        else:
            return FAILED + " ID: %s, query: %s, curr_state: %s, expected: %s, actual: %s" % (self.ID, self.query, self.curr_state, self.expected, self.actual)


    def check(self):
        if self.isDone is True:
            return self.actual['aid'] == self.expected
        else:
            self.run()
            #print self
            return self.check()

def CaseFactory(line):
    line = line.split('#')
    return Case(line)

def readCases():
    tfile = BASE_DIR + "/weiss/tests/test_input.txt"
    with open(tfile, 'r') as f:
        cases = map(CaseFactory, f.readlines()[20:])  # skip first 20 lines
    return cases



class StateTestCase(TestCase):
    def setUp(self):
        self.classifier = getClassifier()
        self.cases = readCases()

    def test_classifier(self):
        for case in self.cases:
            try:
                self.assertTrue(case.check())
            except AssertionError, e:
                pass
            finally:
                print case




