"""
This file contains requests for different API

Author: Ming Fang
"""
class QueryRequest(object):

    def __init__(self, query):
        self.query = query

    def __str__(self):
        return "query: %s" % self.query

class CloseRequest(object):

    def __init__(self, fid):
        self.fid = fid

    def __str__(self):
        return "fid : %s" % self.fid
