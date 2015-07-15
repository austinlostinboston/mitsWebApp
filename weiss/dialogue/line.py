
class Line(object):
'''
Request:
State: Specifies the point in the conversation that the user is in. Five states
    1 - System initiative, when the conversation first begins
    2 - 
    3 - 
    4 - 
    5 - 
'''
    def __init__(self, request, state):
        self.session = request.session
        self.state = state
        self.tid = _getTID()
        self.eid = _getEID()
        self.aid = _getAID()


    def _getTID():
        return self.session['curr_tid']

    def _getEID():
        return self.sessino['curr_eid']

    def _getAID():
        return self.session['curr_aid']

  