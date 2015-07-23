class InitResponse(object):
    """
    unregister user will be assign one flow id
    register user will use user id as flow id
    """
    def __init__(self, fid):
        self.fid = fid


class QueryResponse(object):

    def __init__(self, response):
        self.response = response


class CloseResponse(object):

    def __init__(self, status):
        self.status = status


