import logging
from weiss.actions import *
from django.shortcuts import render_to_response
#from django.template.context_processors import csrf



actions = [nextRandomEntity,
           nextRandomCmt,
           nextRandomPositiveCmt,
           nextRandomNegativeCmt,
           nextRandomOppositeCmt,
           ]

def dispatch(request):

    aid = int(request.POST['aid'])
    actioninput = request.POST['actioninput']
    action = actions[aid]
    logger.debug("Dispatch action: %s, %s, %s" % (aid, action, actioninput))

    addNewDialog(request.session, USER, action.__name__)
    action(request.session)

    logger.debug("Session: %s" % (request.session.keys()))
    c = {}
    #c.update(csrf(request))
    c['dialog'] = sessionToDialog(request.session)
    logger.debug(c)
    return render_to_response("weiss/actionboard.html", c)


def sessionToDialog(session):
    keys = session.keys()
    keys = filter(lambda x: type(x) in [unicode, str] and (x[0] == "0" or x[0] == "1"), keys)
    dialog = map(lambda x: (x[0], int(x[1:]), session[x]), keys)
    return sorted(dialog, key=lambda x: x[1])


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
    session['next_did'] = 0



