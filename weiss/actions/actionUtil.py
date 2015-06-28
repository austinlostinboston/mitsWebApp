'''
Utility methods for actions
Note that, in practice, it is no need to import any from actions.py.
Just import needed method from actionUtil.py


Author: Ming Fang & Yao Zhou
'''

import datetime

from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User

from weiss.actions import *
from weiss.models import History, Action
from weiss.utils.switch import switch




# initialized lazily by getActions()
# acitons is a dict mapping:  aid -> (acton name, action method)
actions = None

def dispatch(request, query, args):
    aid = args['aid']
    print ("aid:%d" % aid)
    #actioninput = request.POST['actioninput']
    actioninput = ""

    global actions
    if actions is None:
        getActions()
    if not actions.has_key(aid):
        logger.debug("No such aid %s, just throw a random comment" % aid)
        aid = 1 # default 1 for next random comment

    aname, action = actions[aid] # it is a tuple (name, method)
    if query is None:
        query = aname + args['query']
    logger.debug("Dispatch action: %s, %s, %s" % (aid, aname, actioninput))

    initNewLine(request.session, query, aid)

    response = action(request.session, args)

    flushNewLine(request, response)

    return

def confirmAciton(UserName, ActionID):
    print 'confirmAciton called'
    #Find user
    user= User.objects.get(username=UserName)
    #Get last history record of that user
    his= History.objects.filter(userid=user.id).order_by('-hid')[0]
    #Modify ddid
    print str(his.hid) + "," + str(his.userid) + "," + str(his.desired_aid)
    his.desired_aid = ActionID
    #Update database
    his.save()
    return

def sessionToDialog(session):
    keys = session.keys()
    keys = filter(lambda x: type(x) in [unicode, str] and (x[0] == "0" or x[0] == "1"), keys)
    dialog = map(lambda x: (x[0], int(x[1:]), session[x]), keys)
    return sorted(dialog, key=lambda x: x[1])

def getDialogHistory(userid, limit=10):
    '''
    get lines from database for rendering the page
    '''
    tenMinAgo = timezone.now() - datetime.timedelta(minutes=10) # 10 min ago
    lines = History.objects.filter(Q(userid=userid), Q(time__gt=tenMinAgo)).order_by("-time")[:10]
    return lines

def initSession(session):
    default =[u'_auth_user_id', u'_auth_user_backend', u'_auth_user_hash']
    keys = session.keys()
    for key in keys:
        if key not in default:
            del session[key]
    session['aid'] = None
    session['curr_cid'] = None
    session['curr_eid'] = None
    session['curr_tid'] = None
    session['actioninput'] = ""


def getActions():
    '''
    Return action names lists and
    Initialize global varable 'actions' if it is not initialized
    '''
    global actions
    if actions is None:
        possibles = globals().copy()  # get the globally acessible naming as as dict
        # list of (aid, name, method), name is a human readable name, method is the method name
        raw_actions = Action.objects.values_list()
        actions = { aid: (name, possibles[str(method)]) for aid, name, method in raw_actions }
    return [ (aid, name) for aid, (name, method) in actions.items()]



# Weiss records user interactons in terms of line
# A line includes a user query and its corresponding respond
# The relevent methods are initNewLine() and flushNewLine()
#
# initNewLine is called at the time whne new query comes
# flushNewLine is called at the time a response is generated.

def flushNewLine(request, response):
    '''
    flush the new line to database
    '''
    session = request.session
    print session['curr_eid']
    userid = request.user
    print userid
    line = session['line']
    curr_eid = session['curr_eid']
    if curr_eid is None:
        eid = None
    else:
        eid = Entity.objects.get(eid=session['curr_eid'])

    aid = Action.objects.get(aid=line['curr_aid'])
    History.objects.create(query=line['query'],
                           userid=userid,
                           response=response,
                           aid=aid,
                           eid=eid,
                           time=timezone.now())

def initNewLine(session, query, aid):
    '''
    init a new line of the dialog in django session.
    Args:
        session: user session
        query: the user query in plain text
        userid:
        aid: the aciton id that Weiss decided
    '''

    session['line'] = {'query': query, 'curr_aid': aid}