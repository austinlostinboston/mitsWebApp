## Import builtins
import random

## Import from weiss
from weiss.flows.factory import getFlowManager
from weiss.models import Action, Type, Types, State, Comment, Entity
from django.db.models import Q

def responseHandler(request):
    ## Set response
    response = 'Empty response: We are experiencing problems, sorry!'

    ## Grab information from request
    session = request.session
    userid = request.user
    state = getFlowManager().lookUp(userid)
    state = State(state)

    ## Get id's from session
    aid = session['aid']
    eid = session['curr_eid']
    cid = session['curr_cid']
    tid = session['curr_tid']

    ## Get id names from enumerated models
    aid_name = Action(aid).name
    if tid is not None:
        tid_name = Type(tid).name
    else:
        tid_name = "none"

    ## Handle the different actions
    if aid_name == "NextRandomComment":
        comment_ob = selectComment(cid, eid, tid)
        response = "One person said \" %s \"" % (comment_ob.body)

    elif aid_name == "NextPositiveComment":
        comment_ob = selectComment(cid, eid, tid, sentiment='+')
        response = "One person said \" %s \"" % (comment_ob.body)

    elif aid_name == "NextNegativeComment":
        comment_ob = selectComment(cid, eid, tid, sentiment='-')
        response = "One person said \" %s \"" % (comment_ob.body)

    elif aid_name == "NextRandomEntity":
        entity_ob = selectEntity(eid, tid)
        resonse = "With such little information, I'll pick to talk about %s." % (entity_ob.name) 

    elif aid_name == "SentimentStats":
        resonse = "Stats will go here."

    elif aid_name == "EntitySelection":
        entity_ob = selectEntity(eid, tid)
        response = "Absoultely, let's talk about %s." % (entity_ob.name)

    elif aid_name == "TypeSelection":
        type_ob = selectType(tid)
        response = "It sounds like you want to talk about %s." % (type_ob.name)

    elif aid_name == "Greeting":
        ## Hnadled elsewhere
        pass

    elif aid_name == "EntityComfirmation":
        ## Not implemented yet
        pass

    elif aid_name == "UnknownAction":
        response = "Sorry, could you not be a bimbo. Ask a better question."

    else:
        print "You unlocked the secrets of the universe!!"

    return response

    
    
def selectType(tid):
    '''
    Returns a type object from database
    '''
    return Type.objects.get(tid=tid)



def selectEntity(eid, tid):
    '''
    Returns random/specified entity object from database.
    '''
    if eid is None:
        if tid is None:
            eids = Entity.objects.all().values_list('eid', flat=True)
        else:
            eids = Entity.objects.filter(tid=tid).values_list('eid', flat=True)
        entity = random.sample(eids,1)[0]
    else:
        entity = eid

    return Entity.objects.get(eid=entity)



def selectComment(cid, eid, tid, sentiment="="):
    '''
    Returns a comment based on tid, eid, tid, and sentimnet (+/-/=)
    '''
    q = Q(tid=tid)

    if cid is None:
        if eid is not None:
            pass
        else:
            q = & Q(eid=eid)
        if sentiment == "=":
            q = & Q(sentiment=0)
        elif sentiment == "+":
            q = & Q(sentiment__gt=0)
        elif sentiment == "-":
            q = & Q(sentiment__lt=0)
        else:
            pass

        cids = Comment.objects.filter(q).values_list('cid', flat=True)
        comment = random.sample(cids,1)[0]
    else:
        comment = cid

    return Comment.objects.get(cid=comment)

