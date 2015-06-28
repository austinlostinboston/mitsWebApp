"""
The fixed number of actions that Weiss supports.
TODO: More edge cases, ex: there is no opposite cmt in the database

Note: There is not need to import any methods dirtectly from here
You probably want something in actionUtil.py

Author: Ming Fang <mingf@cs.cmu.edu>
"""
from django.db.models import Q

from weiss.models import Comment, Entity, Type
from weiss.utils.switch import switch
from weiss.actions.entitySelector import entitySelector
import random
import logging

logger = logging.getLogger(__name__)


def nextRandomEntity(session, args):
    """Start next conversation

    Args:
        session: The session contains current context
            next_tid: the type id that the next conversation is going to talk about
            curr_eid: current entity id that is talking about

    Returns:
        a int that represents next entity id
    """
    print "next random entity"
    #next_tid = int(session['actioninput'] or "3")
    next_tid = int(random.uniform(1, 3.5))
    curr_eid = int(session['curr_eid'] or "0")
    logger.debug("next ran entity with next_tid: %s, curr_eid: %s" % (next_tid, curr_eid))
    eids = Entity.objects.filter(tid=next_tid).values_list('eid', flat=True)
    new_eid = curr_eid
    while (new_eid == curr_eid):
        new_eid = random.sample(eids, 1)[0]

    session['curr_eid'] = new_eid
    logger.debug("next ran entity has decided next eid: %s" % (new_eid))
    #addNewDialog(session, WEISS, new_eid)
    return new_eid

def nextRandomCmt(session, args):
    """Give a random comment of given entity

    Args:
        session: The session contains current context
            curr_eid: current entity id that is talking about

    Returns:
        a dict that represents a new comment
    """

    curr_eid = session['curr_eid']
    curr_cid = session['curr_cid']
    logger.debug("next ran cmt with curr_eid: %s" % curr_eid)
    idx = 0
    if curr_eid is None:
        num_cmt = Comment.objects.count()
        idx = random.randint(0, num_cmt - 1)
    else:
        curr_eid = int(curr_eid)
        idxs = Comment.objects.filter(eid=curr_eid).values_list('cid', flat=True)
        if (len(idxs) == 0):
            #addNewDialog(session, WEISS, "No such comment")
            return "No such comment"
        idx = random.sample(idxs, 1)[0]

    res = None
    try:
        res = Comment.objects.get(cid=idx)
    except Comment.DoesNotExist:
        logger.debug("Object does not exsit. Can not happen!!")
        return nextRandomPositiveCmt(session, args)

    session['curr_cid'] = idx
    session['curr_eid'] = res.eid.eid
    logger.debug("next ran cmt has decided to talk about e:%s, c:%s" % (res.eid, res.cid))
    #addNewDialog(session, WEISS, res.body)
    return res.body


def nextRandomPositiveCmt(session, args):
    """Give a random positive comment of given entity

    Args:
        session: The session contains current context
            curr_eid: the entity id that is talking about
            curr_cid: the current cid

    Returns:
        a comment body
    """
    curr_eid = session['curr_eid']
    curr_cid = session['curr_cid']

    logger.debug("next ran positive cmt with curr_eid: %s, curr_cid: %s" % (curr_eid, curr_cid))

    if curr_eid is None:
        return "What do you want to talk about?"

    idxs = Comment.objects.filter(Q(eid=curr_eid), Q(sentiment__gt=0)).values_list('cid', flat=True)
    idx = curr_cid
    if (len(idxs) == 0):
        return "No such comments"
    else:
        while (idx == curr_cid):
            idx = random.sample(idxs, 1)[0]

    res = None
    try:
        res = Comment.objects.get(cid=idx)
    except Comment.DoesNotExist:
        logger.debug("Object does not exsit. Can not happen!!")
        return nextRandomPositiveCmt(curr_eid, curr_cid)

    session['curr_cid'] = idx
    logger.debug("next ran pos cmt has decided to talk about %s" % res.cid)
    #addNewDialog(session, WEISS, res.body)
    return res.body


def nextRandomNegativeCmt(session, args):
    """Give a random negative comment of given entity

    Args:
        session: The session contains current context
            curr_eid: the entity id that is talking about
            curr_cid: the previous cid

    Returns:
        a dict that represents a new comment
    """
    curr_eid = session['curr_eid']
    curr_cid = session['curr_cid']

    if curr_eid is None:
        return "What do you want to talk about?"

    logger.debug("next ran negative cmt with curr_eid: %s, curr_cid: %s" % (curr_eid, curr_cid))
    idxs = Comment.objects.filter(Q(eid=curr_eid), Q(sentiment__lt=0)).values_list('cid', flat=True)
    idx = curr_cid
    if (len(idxs) == 0):
        #addNewDialog(session, WEISS, "No such comments")
        return "No such comments"
    else:
        while (idx == curr_cid):
            idx = random.sample(idxs, 1)[0]

    res = None
    try:
        res = Comment.objects.get(cid=idx)
    except Comment.DoesNotExist:
        logger.debug("Object does not exsit. Can not happen!!")
        return nextRandomPositiveCmt(session, args)

    session['curr_cid'] = idx
    logger.debug("next ran neg cmt has decided to talk about %s" % res.cid)
    #addNewDialog(session, WEISS, res.body)
    return res.body



def nextRandomOppositeCmt(session, args):
    """Give a random opposite comment of given entity

    Args:
        session: The session contains current context
            curr_sentiment: the value of current sentiment

    Returns:
        a dict that represents a new comment
    """

    curr_cid = session['curr_cid']
    curr_sentiment = None

    if curr_cid is None:
        return "What do you want to talk about?"
    else:
        curr_cmt = Comment.objects.get(cid=curr_cid)
        curr_sentiment = curr_cmt.sentiment

    logger.debug("next ran oppo cmt with curr_sentiment: %s" % curr_sentiment)
    if curr_sentiment > 0:
        return nextRandomNegativeCmt(session, args)
    elif curr_sentiment < 0:
        return nextRandomPositiveCmt(session, args)
    else:
        logger.debug("Weiss does not talk about 0 sentiment comment, but Weiss would give one")
        return nextRandomPositiveCmt(session, args)

def typeSelection(session, args):
    tid = args.get("tid", 3) # imdb by default :)
    session['curr_tid'] = tid
    type_obj = Type.objects.get(tid=tid)
    return "What %s would you like to talk about?" % type_obj.name

"""
FIXME: deprecated
def entitySelectionByTitle(session, args):
    curr_tid = session["curr_tid"] or 3 # file by default
    if args.has_key("keyword"):
        keyword = args["keyword"]
        query = Q(tid=curr_tid, name__icontains=keyword)
        entities = Entity.objects.filter(query)
        if len(entities) == 0:
            return "No such entity."
        entity = entitySelector(entities, curr_tid)
        session["curr_eid"] = entity.eid
        return "Sure, let's talk about %s" % entity.name
    else:
        # TODO: handle this case
        return "What would you like to talk about?"


def entitySelectionByDescription(session, args):
    curr_tid = session["curr_tid"] or 3 # file by default
    if args.has_key("keyword"):
        keyword = args["keyword"]
        query = Q(tid=curr_tid, description__icontains=keyword)
        entities = Entity.objects.filter(query)
        if len(entities) == 0:
            return "No such entity."
        entity = entitySelector(entities, curr_tid)
        session["curr_eid"] = entity.eid
        return "Sure, let's talk about %s" % entity.name
    else:
        # TODO: handle this case
        return "What would you like to talk about?"
"""

def entitySelection(session, args):
    curr_tid = session["curr_tid"] or 3 # file by default
    if args.has_key("keywords"):
        user_query = args["keywords"]
        q = Q(tid=curr_tid, description__icontains=user_query) | Q(tid=curr_tid, name__icontains=user_query)
        entities = Entity.objects.filter(q)
        if len(entities) == 0:
            return "No such entity."
        entity = entitySelector(entities, curr_tid, user_query)
        session["curr_eid"] = entity.eid
        return "Sure, let's talk about %s" % entity.name
    else:
        # TODO: handle this case
        return "What would you like to talk about?"


def sentimentStats(session, args):
    curr_eid = session['curr_eid']
    if curr_eid is None:
        return "What would you like to talk about?"
    else:
        query = Q(eid=curr_eid, sentiment__gt=0)
        num_pos = Comment.objects.filter(query).count()
        num_all = Comment.objects.filter(eid=curr_eid).count()
        percent = float(num_pos) / num_all
        if percent > .9:
            return "Almost everyone thought it was good."
        elif percent > .65:
            return "Most of the people thought it was good."
        elif percent > .35:
            return "It was an even split between positive and negative reviews."
        elif percent > .1:
            return "Most of the people thought it wasn't good."
        else:
            return "Almost everyone thought it was bad."



