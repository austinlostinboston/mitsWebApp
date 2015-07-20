## Import builtins
import random

## Import from weiss
from weiss.models import Action, Type, Types, State, Comment, Entity
from django.db.models import Q
from bs4 import BeautifulSoup

def responseHandler(flow):

    ## read responses.xml to memory
    soup = BeautifulSoup(open('responses.xml'))

    ## Set response
    response = 'Empty response: We are experiencing problems, sorry!'

    ## Grab information from flow
    userid = flow.user
    state = flow.state
    action = flow.action

    ## 
    cid = flow.cid
    eid = flow.eid
    tid = flow.tid
    entities = flow.entities

    ## Text variables
    type_name = flow.type
    entity_name = flow.entity
    comment_body = flow.comment

    if entities is None:
        num_entities = str(None)
    else:
        num_entities = str(len(entities))

    print "===================================================="
    print "--------------  Response Generator  ----------------"
    print "--  Flow State"
    print "------------"
    print "--  User ID: " + str(userid)
    print "--    State: " + str(state)
    print "--   Action: " + str(action)
    print "------------"
    print "--      TID: " + str(tid)
    print "--      EID: " + str(eid)
    print "--      CID: " + str(cid)
    print "--  Num Ent: " + num_entities
    print "------------"
    print "--     Type: " + str(type_name)
    print "--   Entity: " + str(entity_name)

    

    # ## Handle the different actions
    # if action is Action.NextRandomComment:
    #     #comment_ob = selectComment(flow, cid, eid, tid)
    #     response = "One person said \" %s \"" % (comment_ob.body)


    # if action is Action.NextPositiveComment:
    #     #comment_ob = selectComment(flow, cid, eid, tid, sentiment='+')
    #     response = "One person said \" %s \"" % (comment_ob.body)


    # if action is Action.NextNegativeComment:
    #     #comment_ob = selectComment(flow, cid, eid, tid, sentiment='-')
    #     response = "One person said \" %s \"" % (comment_ob.body)


    # if action is Action.NextRandomEntity:
    #     #entity_ob = selectEntity(flow, eid, tid)
    #     response = "With such little information, I guess we'll just talk about %s." % (entity_ob.name)


    # if action is Action.SentimentStats and eid is not None:
    #     response = "Stats about " + str(eid) + " will go here."
    # else:
    #     response = "You need to first tell what you would like to hear stats about."


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


    print "[RESPONSE] " + response

    return response


def pluralType(type_ins):
    type_name = str(type_ins).split('.')[1]
    if type_name[-1] != "s":
        type_name += "s"

    return type_name