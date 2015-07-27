## Import builtins
import random
import os
import re

# Import from weiss
from weiss.models import Action, Types, Comment, Entity
from django.db.models import Q
from bs4 import BeautifulSoup

<<<<<<< HEAD

def responseHandler(flow):
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
def responseHandler(flow, test=False):
>>>>>>> 63918f7... continuing adding to response generator
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

<<<<<<< HEAD
    # Grab information from flow
    userid = flow.user
=======
    ## Grab information from flow
    user = flow.user  # a str, None for unregistered user
    user_id = flow.user_id  # a int
>>>>>>> adbee11... seperate user id and user name
    state = flow.state
    sid = state.sid.value
    action = flow.action
    aid = action.value

    ## id's
    cid = flow.cid
    eid = flow.eid
    tid = flow.tid
    entities = flow.entities

<<<<<<< HEAD
    ## Text variables
<<<<<<< HEAD
    type = flow.type
    entity_name = flow.entity
    comment_body = flow.comment
=======
    # Handle the different actions
    if action is Action.NextRandomComment:
        comment_ob = selectComment(cid, eid, tid)
        response = "One person said \" %s \"" % (comment_ob.body)
>>>>>>> 7991b98...  a lot syntax change
=======
    entity_object = flow.entity
    comment_object = flow.comment
    sent_stats = flow.sentiment_stats

    ## Handle when entity is none or present
    if entity_object:
        entity_name = entity_object.name
    else:
        entity_name = None

    ## Handle when comment is none or present
    if comment_object:
        comment_body = comment_object.body
    else:
        comment_body = None
    
>>>>>>> 26ca79b... unset test option in response generator. added responses.

    if entities is None:
        num_entities = str(None)
    else:
        num_entities = str(len(entities))

    ## Change message used for tests
    if test:
        rsp_id = str("%02d" % (sid)) + "." + str("%02d" % (aid)) + ".test"
    else:
        rsp_id = str("%02d" % (sid)) + "." + str("%02d" % (aid)) + ".01"

    ## prints out current flow object
    print flow 

<<<<<<< HEAD
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
=======
>>>>>>> 63918f7... continuing adding to response generator
    print "[Response ID]: " + str(rsp_id)
    response = soup.find('message',{'id':rsp_id}).text
>>>>>>> ac51fe6... response gen working minimally

    if "[" in response and "]" in response:
        ## Types
        if "[type]" in response:
            response = response.replace("[type]", flow.type.name.lower())
        if "[types]" in response:
            response = response.replace("[types]", pluralType(flow.type.name.lower()))

        ## Entities
        if "[num_entities]" in response:
            response = response.replace("[num_entities]", str(num_entities))
        if "[entity]" in response:
            response = response.replace("[entity]", str(entity_name))

        regex = re.compile(r'\[list\-(\d+)\]')
        
        if regex.search(response) is not None:
            ent_list_length = regex.findall(response)[0]

            if len(entities) >= ent_list_length:
                list_entities = ent_list_length
            else:
                list_entities = len(entities)

            str_ent_list = ''
            for entity in entities[:int(ent_list_length)]:
                str_ent_list += entity.name + ", "
                print str_ent_list
            response = response.replace("[list-" + str(ent_list_length) + "]", str_ent_list)
            response = response.replace("[list-entities]", str(list_entities))

        ## Comments
        if "[body]" in response:
            response = response.replace("[body]", comment_body)

        ## Sentiment
        response = placeSentiment(response, sent_stats)

    print "[RESPONSE] " + response

    return response


def pluralType(type_ins):
    type_name = type_ins
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

<<<<<<< HEAD
>>>>>>> ac51fe6... response gen working minimally
=======
def placeSentiment(response, sentiment_stats):
    if sentiment_stats:
        total = sentiment_stats.num_all
        pos = sentiment_stats.num_pos
        neu = sentiment_stats.num_neu
        neg = total - (pos + neu)
        percent = float('%.2f' % (pos / (total * 1.00)))
        popular = None
        if percent > 0.9 and percent < 1.00:
            popular = "very popular."
        elif percent > 0.65 and percent < 0.89:
            popular = "liked by most"
        elif percent > 0.35 and percent < 0.64:
            popular =  "is an even split among reviewers."
        elif percent > 0.1 and percent < 0.34:
            popular = "not liked by many"
        else: 
            popular = "basically hated by everyone"

        response = response.replace("[popularity]", popular)
        response = response.replace("[percent]", str(int(percent*100)) + '%')

        return response

    else:
        return response

>>>>>>> 43d73d1... added to response generator
