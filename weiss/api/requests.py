class QueryRequest(object):

    def __init__(self, fid, query):
        self.fid = fid
        self.query = query

class CloseRequest(object):

    def __init__(self, fid):
        self.fid = fid
