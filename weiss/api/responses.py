"""
This file contains responses for different API

Author: Ming Fang
"""

class InitResponse(object):
    """
    unregister user will be assign one flow id
    register user will use user id as flow id
    """
    def __init__(self, fid, response):
        self.fid = fid
        self.response = response


class QueryResponse(object):

    def __init__(self, response):
        self.response = response


class CloseResponse(object):

    def __init__(self, status):
        self.status = status


