import logging
import logging
from weiss.actions import *
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from weiss.classifier import actionMapping


actions = [nextRandomEntity,
           nextRandomCmt,
           nextRandomPositiveCmt,
           nextRandomNegativeCmt,
           nextRandomOppositeCmt,
           ]

action_list = {}
action_list["1"] = "Next Random Comment"
action_list["2"] = "Opposite Comment"
action_list["3"] = "Positive Comment"
action_list["4"] = "Negative Comment"
action_list["5"] = "Next Entity"

def addNewDialog(session, speaker, body):
    did = session['next_did']
    session['%s%s' % (speaker, did)] = body
    session['next_did'] += 1

def queryResolve(request):
    #Extract Add user query
    query = str(request.POST['queryinput'])
    addNewDialog(request.session, USER, query)
    
    logger.debug("Resolve query: %s" % (query))

    #Classify Action id based on input query
    actionID = actionMapping(query)
    addNewDialog(request.session, WEISS, "Action:%s" % action_list[str(actionID)])

    #Resolve Action
    action = actions[int(actionID)]
    action(request.session)
    
    #Send back response
    logger.debug("Session: %s" % (request.session.keys()))
    c = {}
    c.update(csrf(request))
    c['dialog'] = sessionToDialog(request.session)
    logger.debug(c)
    return render_to_response("weiss/index.html", c)


def sessionToDialog(session):
    keys = session.keys()
    keys = filter(lambda x: type(x) in [unicode, str] and (x[0] == "0" or x[0] == "1"), keys)
    dialog = map(lambda x: (x[0], int(x[1:]), session[x]), keys)
    return sorted(dialog, key=lambda x: x[1])

def initDialogSession(session):
    default =[u'_auth_user_id', u'_auth_user_backend', u'_auth_user_hash']
    keys = session.keys()
    for key in keys:
        if key not in default:
            del session[key]
    session['aid'] = None
    session['curr_cid'] = None
    session['curr_eid'] = None
    session['curr_tid'] = None
    session['queryinput'] = ""
    session['next_did'] = 0

