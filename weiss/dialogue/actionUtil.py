'''
Utility methods for actions
Note that, in practice, it is no need to import any from actions.py.
Just import needed method from actionUtil.py


Author: Ming Fang
'''

import datetime
import HTMLParser

from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User

from weiss import models
from weiss.utils.switch import switch
from weiss.dialogue.actions import *  # for action methods
from weiss.flows.factory import getFlowManager

parser = HTMLParser.HTMLParser() # html parser

def confirmAciton(UserName, ActionID):
    print 'confirmAciton called'
    #Find user
    user = User.objects.get(username=UserName)
    #Get last history record of that user
    his = models.History.objects.filter(userid=user.id).order_by('-hid')[0]
    #Modify ddid
    print str(his.hid) + "," + str(his.userid) + "," + str(his.desired_aid)
    his.desired_aid = ActionID
    #Update database
    his.save()
    return

def getDialogHistory(userid, limit=10):
    '''
    get lines from database for rendering the page
    '''
    tenMinAgo = timezone.now() - datetime.timedelta(minutes=10) # 10 min ago
    lines = models.History.objects.filter(Q(userid=userid), Q(time__gt=tenMinAgo)).order_by("-time")[:10]
    if len(lines) == 0:
        lines = models.History.objects.filter(Q(userid=userid)).order_by("-time")[:1]
    for line in lines:
        line.response = parser.unescape(line.response)
    return lines

def initSession(request):
    session = request.session
    session['aid'] = None
    session['curr_cid'] = None
    session['curr_eid'] = None
    session['curr_tid'] = None
    session['actioninput'] = ""
    fmgr = getFlowManager()
    fmgr.register(request.user)
    line = models.History.objects.filter(Q(userid=request.user)).order_by("-time")[:1]
    if len(line) > 0 and line[0].aid.aid == 9: # the previous record is not a greeting
        return
    initNewLine(session, '', 9) # greeting aid and meaningless user query
    flushNewLine(request, "Hi I'm Weiss. What would you like to talk about, movies? news? or restaurants?")


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

    aid = models.Actions.objects.get(aid=line['curr_aid'])
    models.History.objects.create(query=line['query'],
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

    session['line'] = {'query': query, 'curr_aid': aid.value}
