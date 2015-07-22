'''
Provide singleton for Classifier

Author: Ming Fang
'''

from weiss.planner.planner import Planner

_planner = None

def getPlanner():
    global _planner
    if _planner is None:
        _planner = Planner()

    return _planner
