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
    if flow.type:
        type_name = flow.type.name.lower()
    else:
        type_name = None
    types = flow.types

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
    summary = flow.summary

    if summary:
        summary_body = summary.body
        print "[summary]" + summary_body
    else:
        summary_body = None

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
    
<<<<<<< HEAD
>>>>>>> 26ca79b... unset test option in response generator. added responses.

=======
    ## Grabs num of entities
>>>>>>> c7bfd37... added a type range response
    if entities is None:
        num_entities = 0
    else:
        num_entities = len(entities)

    ## Grabs number of types in entity list
    if types is None:
        num_types = 1
    else:
        num_types = len(types)

    ## Set type of range in flow
    if num_types > 1:
        range_type = 'type'
        rid = '.t'
    elif num_entities > 1:
        range_type = 'entity'
        rid = '.e'
    else:
        range_type = None
        rid = ''

    ## Change message used for tests
    if test:
        rsp_id = str("%02d" % (sid)) + "." + str("%02d" % (aid)) + ".test"
    else:

        mid = str("%02d" % (random.randint(1,3)))
        rsp_id = str("%02d" % (sid)) + "." + str("%02d" % (aid)) + "." + mid + rid

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
<<<<<<< HEAD
    response = soup.find('message',{'id':rsp_id}).text
>>>>>>> ac51fe6... response gen working minimally
=======
    response = soup.find('message', {'id': rsp_id}).text
>>>>>>> e4cf556... minor syntac change

    ## Create dictionary of any needed parts for the message
    msgParts = {}
    msgParts['type'] = type_name
    if range_type == 'type':
        msgParts['types'] = typeList(types)
    if range_type == 'entity':
        msgParts['types'] = pluralType(type_name)
    if range_type is None:
        msgParts['types'] = pluralType(type_name)
    msgParts['num_entities'] = str(num_entities)
    msgParts['entity'] = str(entity_name)

    if summary_body:
        msgParts['summary'] = buildSummary(summary_body, 3)
    else:
        msgParts['summary'] = comment_body

    if num_entities > 5:
        msgParts['list_entities'] = str(5)
    else:
        msgParts['list_entities'] = num_entities

    msgParts['list_5'] = listify(entities, 5)

    ## Sentiment
    placeSentiment(sent_stats, msgParts)

    response = buildResponse(response, msgParts)
    

    print "[RESPONSE] " + response.encode('utf8')

    return response


def buildResponse(response, msgParts):
    ## Extract only characters between [ and ]
    regex = re.compile(r'\[(\w+)\]')

    ## Only extract contents when the parse symbol is present
    if regex.search(response) is not None:

        ## Extract parts of response that need replaced
        replacers = regex.findall(response)
        print "[replacers]" + str(replacers)

        for part in replacers:
            print msgParts[str(part)]
            print "[" + str(part) + "]"
            response = response.replace("[" + str(part) + "]", msgParts[str(part)])

    return response


def listify(str_list, length):
    if str_list:
        text_list = ''
        first_n = str_list[0:length]
        for i, item in enumerate(first_n):
            if i < len(first_n) - 1:
                text_list += str(i+1) + ". " + item.name + ", "
            else:
                text_list += "and " + str(i+1) + ". " + item.name

        return unicode(text_list)
    else:
        return str(None)

def pluralType(type_ins):
    if type_ins:
        type_name = type_ins.lower()
        if type_name[-1] != "s":
            type_name += "s"
        if type_name == 'news':
            type_name = 'news articles'

        return type_name
    else:
        return str(None)

<<<<<<< HEAD
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
=======

def placeSentiment(sentiment_stats, msgParts):
>>>>>>> f55e7d7... refactored response generator. Stable with a few issues.
    if sentiment_stats:
        percent = float(sentiment_stats.num_pos) / sentiment_stats.num_all
        if percent > .9:
            popular = "very popular"
        elif percent > .65:
            popular = "liked by most"
        elif percent > .35:
            popular = "is an even split among reviewers"
        elif percent > .1:
            popular = "not liked by many"
        else:
            popular = "basically hated by everyone"

<<<<<<< HEAD
        msgParts['popularity'] = popular
        msgParts['percent'] = str(int(percent*100)) + '%'
=======
        response = response.replace("[popularity]", popular)
        percent_str = "%.0f%%" % (percent * 100)
        response = response.replace("[percent]", percent_str)
>>>>>>> fec3f15... refine sentiment logic for res gen

        # response = response.replace("[popularity]", popular)
        # response = response.replace("[percent]", str(int(percent*100)) + '%')

        # return response

<<<<<<< HEAD
>>>>>>> 43d73d1... added to response generator
=======

def typeList(types):
    type_list = ''
    for i, type_ob in enumerate(types):
        type_list += pluralType(type_ob.name)
        if (i + 1) == (len(types) - 1):
            type_list += ' or '
        if (i + 1) == len(types):
            pass
        if (i + 1) < (len(types) - 1):
            type_list += ', '

    return type_list
<<<<<<< HEAD
>>>>>>> c7bfd37... added a type range response
=======


def buildSummary(summary_body, sentence_num):
    regex = re.compile(r'\d+\#')

    ## Check to see if body is summary or just comment.
    if regex.search(summary_body) is not None:

        print "[summar] " + summary_body 
        if summary_body:
            sentences = summary_body.split("\n")
            ranked_sentences = []
            sum_str = ''

            for sentence in sentences:
                rank_sent = sentence.split('#')
                ranked_sentences.append([int(rank_sent[0]),rank_sent[1]])

            ranked_sentences = sorted(ranked_sentences)
            print ranked_sentences

            for sent in ranked_sentences[0:sentence_num]:
                print sent
                sum_str += sent[1] + " "

            return sum_str
        else:
            return str(None)
    else:
<<<<<<< HEAD
        return str(None)
>>>>>>> f55e7d7... refactored response generator. Stable with a few issues.
=======
        return summary_body
>>>>>>> 8982d58... fixed a few issues with response generator and added number lists
