"""
The fixed actions that Weiss supports.
TODO: More edge cases, ex: there is no opposite cmt in the database

Author: Ming Fangi <mingf@cs.cmu.edu>
"""
from weiss.models import Comment, Entity, Type
import random
import logging

logger = logging.getLogger(__name__)

USER = 0
WEISS = 1

def nextRandomEntity(session):
    """Start next conversation

    Args:
        session: The session contains current context
            next_tid: the type id that the next conversation is going to talk about
            curr_eid: current entity id that is talking about

    Returns:
        a int that represents next entity id
    """
    next_tid = int(session['actioninput'] or "3")
    curr_eid = int(session['curr_eid'] or "0")
    logger.debug("next ran entity with next_tid: %s, curr_eid: %s" % (next_tid, curr_eid))
    eids = Entity.objects.filter(tid=next_tid).values_list('eid', flat=True)
    new_eid = curr_eid
    while (new_eid == curr_eid):
        new_eid = random.sample(eids, 1)[0]

    session['curr_eid'] = new_eid
    logger.debug("next ran entity has decided next eid: %s" % (new_eid))
    addNewDialog(session, WEISS, new_eid)
    return new_eid

def nextRandomCmt(session):
    """Give a random comment of given entity

    Args:
        session: The session contains current context
            curr_eid: current entity id that is talking about

    Returns:
        a dict that represents a new comment
    """

    curr_eid = session['curr_eid']

    logger.debug("next ran  cmt with curr_eid: %s" % curr_eid)
    idx = 0
    if curr_eid is None:
        num_cmt = Comment.objects.count()
        idx = random.randint(0, num_cmt - 1)
    else:
        curr_eid = int(curr_eid)
        idxs = Comment.objects.filter(eid=curr_eid).values_list('cid', flat=True)
        if (len(idxs) == 0):
            addNewDialog(session, WEISS, "No such comment")
            return
        idx = random.sample(idxs, 1)[0]

    res = None
    try:
        res = Comment.objects.get(cid=idx)
    except Comment.DoesNotExist:
        logger.debug("Object does not exsit. Can not happen!!")
        return nextRandomPositiveCmt(curr_eid, curr_cid)

    session['curr_cid'] = idx
    logger.debug("next ran cmt has decided to talk about %s" % res.cid)
    addNewDialog(session, WEISS, res.body)



def nextRandomPositiveCmt(session):
    """Give a random positive comment of given entity

    Args:
        session: The session contains current context
            curr_eid: the entity id that is talking about
            curr_cid: the current cid

    Returns:
        a dict that represents a new comment
    """

    curr_eid = session['curr_eid']
    curr_cid = session['curr_cid']

    logger.debug("next ran positive cmt with curr_eid: %s, curr_cid: %s" % (curr_eid, curr_cid))
    idxs = Comment.objects.filter(sentiment__gt=0).values_list('cid', flat=True)
    idx = curr_cid
    if (len(idxs) == 0):
        addNewDialog(session, WEISS, "No such comments")
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
    addNewDialog(session, WEISS, res.body)


def nextRandomNegativeCmt(session):
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

    logger.debug("next ran negative cmt with curr_eid: %s, curr_cid: %s" % (curr_eid, curr_cid))
    idxs = Comment.objects.filter(sentiment__lt=0).values_list('cid', flat=True)
    idx = curr_cid
    if (len(idxs) == 0):
        addNewDialog(session, WEISS, "No such comments")
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
    logger.debug("next ran neg cmt has decided to talk about %s" % res.cid)
    addNewDialog(session, WEISS, res.body)



def nextRandomOppositeCmt(session):
    """Give a random opposite comment of given entity

    Args:
        session: The session contains current context
            curr_sentiment: the value of current sentiment

    Returns:
        a dict that represents a new comment
    """

    curr_cid = session['curr_cid']
    curr_sentiment = None

    if curr_cid is not None:
        curr_cmt = Comment.objects.get(cid=curr_cid)
        curr_sentiment = curr_cmt.sentiment

    logger.debug("next ran oppo cmt with curr_sentiment: %s" % curr_sentiment)
    if curr_sentiment > 0:
        return nextRandomNegativeCmt(session)
    elif curr_sentiment < 0:
        return nextRandomPositiveCmt(session)
    else:
        logger.debug("Weiss does not talk about 0 sentiment comment, but Weiss would give one")
        return nextRandomPositiveCmt(session)


def addNewDialog(session, speaker, body):
    did = session['next_did']
    session['%s%s' % (speaker, did)] = body
    session['next_did'] += 1


