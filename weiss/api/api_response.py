class APIResponse(object):
    """
    unregister user will be assign one flow id
    register user will use user id as flow id
    """
    def __init__(self, fid, response):
        self.fid = fid
        self.response = response
