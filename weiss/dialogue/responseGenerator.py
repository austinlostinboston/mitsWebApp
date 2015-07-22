## Import builtins
import random
import os

# Import from weiss
from weiss.models import Action, Types, Comment, Entity
from django.db.models import Q
from bs4 import BeautifulSoup


def responseHandler(flow):
<<<<<<< HEAD
<<<<<<< HEAD
=======
    ## Get directory
    cur_dir = os.path.dirname(__file__)
>>>>>>> ac51fe6... response gen working minimally

    ## read responses.xml to memory
    soup = BeautifulSoup(open(cur_dir + '/responses.xml'))

    ## Set response
=======
    # Set response
>>>>>>> 7991b98...  a lot syntax change
    response = 'Empty response: We are experiencing problems, sorry!'

    # Grab information from flow
    userid = flow.user
    state = flow.state
    sid = state.sid.value
    action = flow.action
    aid = action.value

    ## 
    cid = flow.cid
    eid = flow.eid
    tid = flow.tid
    entities = flow.entities

<<<<<<< HEAD
    ## Text variables
    type_name = flow.type.name
    entity_name = flow.entity
    comment_body = flow.comment
=======
    # Handle the different actions
    if action is Action.NextRandomComment:
        comment_ob = selectComment(cid, eid, tid)
        response = "One person said \" %s \"" % (comment_ob.body)
>>>>>>> 7991b98...  a lot syntax change

    if entities is None:
        num_entities = str(None)
    else:
        num_entities = str(len(entities))

    print "===================================================="
    print "--------------  Response Generator  ----------------"
    print "--  Flow State"
    print "--------------"
    print "--  User ID: " + str(userid)
    print "--    State: " + str(state)
    if (state.sid is State.RangeSelected):
        print "--     Step: " + state.step.name
    print "--   Action: " + str(action)
    print "--------------"
    print "--      TID: " + str(tid)
    print "--      EID: " + str(eid)
    print "--      CID: " + str(cid)
    print "--  Num Ent: " + num_entities
    print "--------------"
    print "--     Type: " + str(type_name)
    print "--   Entity: " + str(entity_name)

<<<<<<< HEAD
<<<<<<< HEAD
    

    # ## Handle the different actions
    # if action is Action.NextRandomComment:
    #     #comment_ob = selectComment(flow, cid, eid, tid)
    #     response = "One person said \" %s \"" % (comment_ob.body)
=======
    elif action is Action.NextRandomEntity:
        entity_ob = selectEntity(eid, tid)
        response = "With such little information, I'll pick to talk about %s." % (entity_ob.name)

    elif action is Action.SentimentStats:
        response = "Stats will go here."
>>>>>>> 7991b98...  a lot syntax change


    # if action is Action.NextPositiveComment:
    #     #comment_ob = selectComment(flow, cid, eid, tid, sentiment='+')
    #     response = "One person said \" %s \"" % (comment_ob.body)

<<<<<<< HEAD

    # if action is Action.NextNegativeComment:
    #     #comment_ob = selectComment(flow, cid, eid, tid, sentiment='-')
    #     response = "One person said \" %s \"" % (comment_ob.body)
=======
    elif action is Action.Greeting:
        # Hnadled elsewhere
        pass

    elif action is Action.EntityConfirmation:
        # Not implemented yet
        pass
>>>>>>> 7991b98...  a lot syntax change


    # if action is Action.NextRandomEntity:
    #     #entity_ob = selectEntity(flow, eid, tid)
    #     response = "With such little information, I guess we'll just talk about %s." % (entity_ob.name)


    # if action is Action.SentimentStats and eid is not None:
    #     response = "Stats about " + str(eid) + " will go here."
    # else:
    #     response = "You need to first tell what you would like to hear stats about."

<<<<<<< HEAD

    # if action is Action.EntitySelection and str(state) is 'RangeSelected':
    #     response = "There are " + num_entities + " possible matching " + pluralType(type_name) + ". " \
    #         "They are..." 
    #     for entity in entities:
    #         response += ", " + entity.name
    # else:
    #     #entity_ob = selectEntity(flow, eid, tid)
    #     response = "Absolutely, let's talk about %s." % entity_name


    # if action is Action.TypeSelection:
    #     #type_ob = selectType(flow, tid)
    #     response = "It sounds like you want to talk about %s." % type_name

    # if action is Action.Greeting:
    #     ## Handled elsewhere
    #     pass

    # if action is Action.EntityConfirmation:
    #     ## Not implemented yet
    #     pass

    # if action is Action.UnknownAction:
    #     response = "Sorry, could you not be a bimbo and ask a better question."
=======
    rsp_id = str("%02d" % (sid)) + "." + str("%02d" % (aid)) + ".01"
    print "[Response ID]: " + str(rsp_id)
    response = soup.find('message',{'id':rsp_id}).text
>>>>>>> ac51fe6... response gen working minimally

    if "[" in response and "]" in response:
        if "[type]" in response:
            response = response.replace("[type]", type_name.lower())
        if "[types]" in response:
            response = response.replace("[type]", pluralType(type_name.lower()))

    print "[RESPONSE] " + response

    return response


def pluralType(type_ins):
    type_name = str(type_ins).split('.')[1]
    if type_name[-1] != "s":
        type_name += "s"

    return type_name
<<<<<<< HEAD
=======
def selectType(tid):
    """
    Returns a type object from database
    """
    return Types.objects.get(tid=tid)


def selectEntity(eid, tid):
    """
    Returns random/specified entity object from database.
    """
    if eid is None:
        if tid is None:
            eids = Entity.objects.all().values_list('eid', flat=True)
        else:
            eids = Entity.objects.filter(tid=tid).values_list('eid', flat=True)
        entity = random.sample(eids, 1)[0]
    else:
        entity = eid

    return Entity.objects.get(eid=entity)


def selectComment(cid, eid, tid, sentiment="="):
    """
    Returns a comment based on tid, eid, tid, and sentimnet (+/-/=)
    """
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
        comment = random.sample(cids, 1)[0]
    else:
        comment = cid

    return Comment.objects.get(cid=comment)
>>>>>>> 7991b98...  a lot syntax change
=======

>>>>>>> ac51fe6... response gen working minimally
