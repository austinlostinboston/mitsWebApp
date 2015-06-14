from weiss.model import Comment, Entity, Type
import random
import logging

logger = logging.getLogger(__name__)

def nextRandomEntity(next_tid, curr_eid):
    """Start next conversation

    Args:
        next_tid: the type id that the next conversation is going to talk about
        curr_eid: current entity id that is talking about

    Returns:
        a int that represents next entity id
    """

    logger.DEBUG("next ran entity with next_tid: %s, curr_eid: %s" % (next_tid, curr_eid))
    eids = Entity.objects.filter(tid=next_tid).values_list('eid', flat=True)
    new_eid = curr_eid
    while (new_eid == curr_eid):
        new_eid = random.sample(eids)
    return new_eid

def nextRandomCmt(curr_eid):
    """Give a random comment of given entity

    Args:
        curr_eid: current entity id that is talking about

    Returns:
        a dict that represents a new comment
    """
    logger.DEBUG("next ran  cmt with curr_eid: %s" % curr_eid)
    idx = 0
    if (curr_eid is None)
        num_cmt = Comment.objects.count()
        idx = random.randint(0, num_cmt - 1)
    else:
        idxs = Comment.objects.filter(eid=curr_eid).values_list('cid', flat=True)
        idx = random.sample(idxs)

    return Comment.objects.all()[idx]

def nextRandomPositiveCmt(curr_eid, curr_cid):
    """Give a random positive comment of given entity

    Args:
        curr_eid: the entity id that is talking about
        curr_cid: the previous cid

    Returns:
        a dict that represents a new comment
    """
    logger.DEBUG("next ran positive cmt with curr_eid: %s, curr_cid: %s" % (curr_eid, curr_cid))
    idxs = Comment.objects.filter(sentiment__gt=0).values_list('cid', flat=True)
    idx = curr_cid
    while (idx == curr_cir):
        idx = random.sample(idxs, 1)

    res = None
    try:
        res = Comment.objects.get(cid=idx)
    except ObjectDoesNotExist:
        logger.DEBUG("Object does not exsit. Can not happen!!")
        return nextRandomPositiveCmt(curr_eid, curr_cid)
    return res

def nextRandomNegativeCmt(curr_eid, curr_cid):
    """Give a random negative comment of given entity

    Args:
        curr_eid: the entity id that is talking about
        curr_cid: the previous cid

    Returns:
        a dict that represents a new comment
    """

    logger.DEBUG("next ran negative cmt with curr_eid: %s, curr_cid: %s" % (curr_eid, curr_cid))
    idxs = Comment.objects.filter(sentiment__lt=0).values_list('cid', flat=True)
    idx = curr_cid
    while (idx == curr_cir):
        idx = random.sample(idxs, 1)

    res = None
    try:
        res = Comment.objects.get(cid=idx)
    except ObjectDoesNotExist:
        logger.DEBUG("Object does not exsit. Can not happen!!")
        return nextRandomPositiveCmt(curr_eid, curr_cid)
    return res


def nextRandomOppositeCmt(curr_sentiment):
    """Give a random opposite comment of given entity

    Args:
        curr_sentiment: the value of current sentiment

    Returns:
        a dict that represents a new comment
    """

    logger.DEBUG("next ran oppo cmt with curr_sentiment: %s" % curr_sentiment)
    if (curr_sentiment > 0):
        return nextRandomNegativeCmt(curr_cmt)
    else if (curr_sentiment < 0):
        return nextRandomPositiveCmt(curr_cmt)
    else:
        logger.DEBUG("Weiss does not talk about 0 sentiment comment, but Weiss would give one")
        return nextRandomPositiveCmt(curr_cmt)




