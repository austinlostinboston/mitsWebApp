'''
Provide singleton for flowManager

Author: Ming Fang
'''

from weiss.flows.flowManager import FlowManager

_instance = None

def getFlowManager():
    global _instance
    if _instance is None:
        _instance = FlowManager()

    return _instance

