from django.test import TestCase

from weiss.planner.factory import getClassifier
from weiss.flows.factory import getFlowManager
from weiss.tests.testUtils import *
from weiss.models import State

from webapps.settings import BASE_DIR


class Case(object):

    def __init__(self, line):
        self.query = line[0]
        self.curr_sid = int(line[1])
        self.expected_aid = int(line[2])
        if (self.expected_aid == 8):
            self.expected_tid = int(line[3])
        else:
            self.expected_tid = None
        self.classifier = getClassifier()
        self.fmgr = getFlowManager()
        self.curr_state = self.fmgr.createState(1, State(self.curr_sid)) # 1 for a dummy user id
        self.actual = None
        self.isDone = False

    def run(self):
        self.actual = self.classifier.action_info(self.query, self.curr_state)
        self.isDone = True

    def __str__(self):
        if self.check():
            return  "query: %s\ncurr_state: %s\nexpected_aid: %s, expected_tid: %s\nactual: %s\n" %   \
                    (self.query, self.curr_state, self.expected_aid, self.expected_tid, self.actual) \
                    + PASSED + "\n"
        else:
            return  "query: %s\ncurr_state: %s\nexpected_aid: %s, expected_tid: %s\nactual: %s\n" %   \
                    (self.query, self.curr_state, self.expected_aid, self.expected_tid, self.actual) \
                    + FAILED + "\n"


    def check(self):
        if self.isDone is True:
            if (self.expected_aid == 8):
                if 'tid' not in self.actual:
                    return False
                else:
                    return self.actual['aid'] == self.expected_aid and self.actual['tid'] == self.expected_tid
            else:
                return self.actual['aid'] == self.expected_aid
        else:
            self.run()
            #print self
            return self.check()

def CaseFactory(line):
    if line.startswith("#") or line == "\n":
        return None
    line = line.split('#')
    return Case(line)

def readCases():
    tfile = BASE_DIR + "/weiss/tests/test_input.txt"
    with open(tfile, 'r') as f:
        cases = map(CaseFactory, f.readlines())
        cases = filter(lambda x : x is not None, cases)
    return cases



class ClassifierTestCase(TestCase):
    def setUp(self):
        self.classifier = getClassifier()
        self.cases = readCases()

    def test_classifier(self):
        numCases = len(self.cases)
        numPass = 0
        numFail = 0
        for case in self.cases:
            try:
                self.assertTrue(case.check())
                numPass = numPass + 1
            except AssertionError, e:
                numFail = numFail + 1
            finally:
                print case
        print "Summary:  Passed: %s, Failed: %s, All: %s" % (numPass, numFail, numCases)




