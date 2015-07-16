## Import builtins
import random

## Import from weiss
from weiss.models import Action, Type, Types, State, Comment, Entity
from django.db.models import Q

def responseHandler(flow):
    ## Set response
    response = 'Empty response: We are experiencing problems, sorry!'

    ## Grab information from flow
    userid = flow.user
    state = flow.state
    action = flow.action

    cid = flow.cid
    eid = flow.eid
    tid = flow.tid

    ## Handle the different actions
    if action is Action.NextRandomComment:
        comment_ob = selectComment(cid, eid, tid)
        response = "One person said \" %s \"" % (comment_ob.body)

    elif action is Action.NextPositiveComment:
        comment_ob = selectComment(cid, eid, tid, sentiment='+')
        response = "One person said \" %s \"" % (comment_ob.body)

    elif action is Action.NextNegativeComment:
        comment_ob = selectComment(cid, eid, tid, sentiment='-')
        response = "One person said \" %s \"" % (comment_ob.body)

    elif action is Action.NextRandomEntity:
        entity_ob = selectEntity(eid, tid)
        resonse = "With such little information, I'll pick to talk about %s." % (entity_ob.name)

    elif action is Action.SentimentStats:
        resonse = "Stats will go here."

    elif action is Action.EntitySelection:
        entity_ob = selectEntity(eid, tid)
        response = "Absoultely, let's talk about %s." % (entity_ob.name)

    elif action is Action.TypeSelection:
        type_ob = selectType(tid)
        response = "It sounds like you want to talk about %s." % (type_ob.name)

    elif action is Action.Greeting:
        ## Hnadled elsewhere
        pass

    elif action is Action.EntityConfirmation:
        ## Not implemented yet
        pass

    elif action is Action.UnknownAction:
        response = "Sorry, could you not be a bimbo. Ask a better question."

    else:
        print "You unlocked the secrets of the universe!!"

    return response



def selectType(tid):
    '''
    Returns a type object from database
    '''
    return Types.objects.get(tid=tid)



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
            q = q & Q(eid=eid)
        if sentiment == "=":
            q = q & Q(sentiment=0)
        elif sentiment == "+":
            q = q & Q(sentiment__gt=0)
        elif sentiment == "-":
            q = q & Q(sentiment__lt=0)
        else:
            pass

        cids = Comment.objects.filter(q).values_list('cid', flat=True)
        comment = random.sample(cids,1)[0]
    else:
        comment = cid

    return Comment.objects.get(cid=comment)

