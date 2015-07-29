"""
This module provides:
    a fixed number of actions that weiss supports


Author: Ming Fang <mingf@cs.cmu.edu>
"""
import random
import logging

from django.db.models import Q

from weiss.models import Comment, Entity, Step, Summary
from weiss.flows.states import *
from weiss.utils.switch import switch
from weiss.dialogue import actionUtil

logger = logging.getLogger(__name__)


def nextRandomEntity(flow, decision):
    """Start next conversation with a random entity

        pick a random entity and set eid in flow
    Args:
        flow: the flow class
        decision: decision made by classifier
    Return:
        Void    Returns:
    """
    next_tid = flow.tid
    curr_eid = flow.eid
    logger.debug("next ran entity with next_tid: %s, curr_eid: %s" % (next_tid, curr_eid))
    eids = Entity.objects.filter(tid=next_tid).values_list('eid', flat=True)
    new_eid = curr_eid
    while new_eid == curr_eid:
        new_eid = random.sample(eids, 1)[0]

    flow.eid = new_eid
    logger.debug("next ran entity has decided next eid: %s" % new_eid)

    """ Handle by Response Generator
    entity = Entity.objects.get(eid=new_eid)

    return "Sure, let's talk about \"%s\"" % entity.name
    """

    flow.transit(State.EntitySelected)
    return


def nextRandomCmt(flow, decision):
    """Pick a random comment
    Args:
        flow: the flow class
        decision: decision made by classifier
    Return:
        Void    Returns:
    """
    curr_eid = flow.eid
    logger.debug("next ran cmt with curr_eid: %s" % curr_eid)
    if curr_eid is None:
        num_cmt = Comment.objects.count()
        idx = random.randint(0, num_cmt - 1)
    else:
        curr_eid = int(curr_eid)
        idxs = Comment.objects.filter(eid=curr_eid).values_list('cid', flat=True)
        if len(idxs) == 0:
            flow.cid = None # no such comment
            return
        idx = random.sample(idxs, 1)[0]
    flow.cid = idx

    """ Handled by Response Generator
    res = None
    try:
        res = Comment.objects.get(cid=idx)
    except Comment.DoesNotExist:
        logger.debug("Object does not exsit. Can not happen!!")
        return nextRandomPositiveCmt(session, decision)

    session['curr_eid'] = res.eid.eid
    """
    logger.debug("next ran cmt has decided to talk about c:%s" % (idx))
    flow.transit(State.CommentSelected)
    return


def nextRandomPositiveCmt(flow, decision):
    """Pick a random positive comment

        If curr_eid is None, return directly
        If no positive cmt in current eid, set flow.cid = None and return
        If there is one cmt found, set flow.cid and return
    Args:
        flow: the flow class
        decision: decision made by classifier
    Return:
        Void
    """
    curr_eid = flow.eid
    curr_cid = flow.cid

    logger.debug("next ran positive cmt with curr_eid: %s, curr_cid: %s" % (curr_eid, curr_cid))

    if curr_eid is None:
        logger.info("No eid given")
        # return "What do you want to talk about?"
        return

    idxs = Comment.objects.filter(Q(eid=curr_eid), Q(sentiment__gt=0)).values_list('cid', flat=True)
    idx = curr_cid
    if len(idxs) == 0:
        flow.cid = None
        # return "No such comments"
        logger.info("No such comments")
        return
    else:
        while idx == curr_cid:
            idx = random.sample(idxs, 1)[0]

    """Handle by Ges Gen
    res = None
    try:
        res = Comment.objects.get(cid=idx)
    except Comment.DoesNotExist:
        logger.debug("Object does not exsit. Can not happen!!")
        return nextRandomPositiveCmt(curr_eid, curr_cid)
    """
    flow.cid = idx
    logger.debug("next ran pos cmt has decided to talk about %s" % idx)
    flow.transit(State.CommentSelected)
    return

def next_positive_summary(flow, decision):
    curr_entity = flow.entity
    if curr_entity is None:
        logger.error("no entity decided")
        return

    try:
        summary = Summary.objects.filter(cid__eid=curr_entity.eid,
                                         cid__sentiment__gt=0).order_by('rank')[flow.next_pos_rank]
    except Summary.DoesNotExist:
        logger.warn("Run out of summary for this entity")
        flow.summary = None
        return
    flow.next_pos_rank += 1
    flow.summary = summary
    flow.comment = summary.cid
    return

def next_negative_summary(flow, decision):
    curr_entity = flow.entity
    if curr_entity is None:
        logger.error("no entity decided")
        return

    try:
        summary = Summary.objects.filter(cid__eid=curr_entity.eid,
                                         cid__sentiment__lt=0).order_by('rank')[flow.next_neg_rank]
    except Summary.DoesNotExist:
        flow.summary = None
        logger.warn("Run out of summary for this entity")
        return
    flow.next_neg_rank += 1
    flow.summary = summary
    flow.comment = summary.cid
    return

def next_opposite_summary(flow, decision):
    curr_comment = flow.comment

    if curr_comment is None:
        logger.error("No comment decided")
        return

    if curr_comment.sentiment > 0:
        return next_negative_summary(flow, decision)
    else:
        return next_positive_summary(flow, decision)

def next_summary(flow, decision):

    curr_comment = flow.comment

    if curr_comment is None:
        return next_positive_summary(flow, decision)
    if curr_comment.sentiment > 0:
        return next_positive_summary(flow, decision)
    else:
        return next_negative_summary(flow, decision)


def nextRandomNegativeCmt(flow, decision):
    """Pick a random negative comment

        If curr_eid is None, return directly
        If no negative cmt in curr_eid, set curr_cid = None and return
        If there is one cmt found, set curr_cid and return
    Args:
        flow: the flow class
        decision: decision made by classifier
    Return:
        Void
    """
    curr_eid = flow.eid
    curr_cid = flow.cid

    if curr_eid is None:
        logger.info("No eid given")
        return

    logger.debug("next ran negative cmt with curr_eid: %s, curr_cid: %s" % (curr_eid, curr_cid))
    idxs = Comment.objects.filter(Q(eid=curr_eid), Q(sentiment__lt=0)).values_list('cid', flat=True)
    idx = curr_cid
    if len(idxs) == 0:
        flow.cid = None
        # return "No such comments"
        return
    else:
        while idx == curr_cid:
            idx = random.sample(idxs, 1)[0]

    """Handle by res gen
    res = None
    try:
        res = Comment.objects.get(cid=idx)
    except Comment.DoesNotExist:
        logger.debug("Object does not exsit. Can not happen!!")
        return nextRandomPositiveCmt(session, decision)
    """
    flow.cid = idx
    logger.debug("next ran neg cmt has decided to talk about %s" % idx)
    flow.transit(State.CommentSelected)
    return


def nextRandomOppositeCmt(flow, decision):
    """Pick a random comment with opposite sentiment

        If flow.cid is None, return directly
        If this cmt is positive, call negative cmt executor
        If this cmt is negative, call positive cmt executor
        If this cmt is neutral, call positive cmt executor
    Args:
        flow: the flow class
        decision: decision made by classifier
    Return:
        Void
    """
    comment = flow.comment

    if comment is None:
        return
    else:
        curr_sentiment = comment.sentiment

    logger.debug("next ran oppo cmt with curr_sentiment: %s" % curr_sentiment)
    if curr_sentiment > 0:
        return nextRandomNegativeCmt(flow, decision)
    elif curr_sentiment < 0:
        return nextRandomPositiveCmt(flow, decision)
    else:
        logger.debug("Weiss does not talk about 0 sentiment comment, but Weiss would give one")
        return nextRandomPositiveCmt(flow, decision)


def typeSelection(flow, decision):
    """Pick a type
        set flow.tid

        If there is tid in decision, set it accordingly
        curr_tid is always set upon return
    Args:
        flow: the flow class
        decision: decision made by classifier
    Return:
        Void
    """
    assert("tid" in decision)
    flow.type = decision["tid"]
    flow.transit(State.TypeSelected)
    """Handle by res gen
    type_obj = Types.objects.get(tid=tid)
    return "What %s would you like to talk about?" % type_obj.name
    """
    return


def entitySelection(flow, decision):
    """Pick entities based on keywords

        None test for keywords

        if there are 3 or more keywords:
            get entities that contain all (up to 3) keywords
                contain is defined as (description containing or title containing)
        if no entity meets the requirement:
            try one keyword at a time
        if any entities are found, pass to entitySelector, and we are good
        if no entity found by each one keyword: well, say sorry

        pick a random entity and set eid in flow
    Args:
        flow: the flow class
        decision: decision made by classifier
    Return:
        Void
    """
    curr_tid = flow.tid
    logger.debug("curr tid : %s" % curr_tid)
    """
    if decision.has_key("tid"):
        curr_tid = decision["tid"]
        session["curr_tid"] = curr_tid
    """
    if "keywords" in decision:
        # select by first 3 keywords
        keywords = decision["keywords"]

        logger.debug(keywords)
        if len(keywords) >= 3:
            keywords = keywords[:3]

        if curr_tid is not None:
            base = Q(tid=curr_tid)
        else:
            base = Q()

        for keyword in keywords:
            q = base & (Q(description__icontains=keyword) | Q(name__icontains=keyword))
        entities = Entity.objects.filter(q)
        flow.entities = entities
        if len(entities) == 1:
            # good, we found only one, go to EntitySelected state with curr_eid set
            flow.transit(State.EntitySelected)
            flow.keep(0)  # only one, just keep it
            return
            # return "Sure, let's talk about \"%s\"" % entity.name
        elif len(entities) > 1:
            # It gave a shitload, go to RangeSelected with state.entities set
            flow.transit(State.RangeSelected)
            if curr_tid is not None:
                flow.state.step = Step.TypeSelected
            else:
                type_range = actionUtil.get_type_range(entities)
                if len(type_range) == 1:
                    flow.state.step = Step.TypeSelected
                    flow.rank()
                    flow.type = type_range[0]
                else:
                    assert len(type_range) > 1
                    flow.state.step = Step.RangeInitiative
                    flow.types = type_range
            return
        else:
            # if there is no such entity, we loosen the requirement
            keywords = decision["keywords"].split("#")
            keywords.reverse()
            while len(keywords) > 0:
                keyword = keywords.pop()
                q = (base & Q(description__icontains=keyword)) | (base & Q(name__icontains=keyword))
                entities = Entity.objects.filter(q)
                flow.entities = entities
                if len(entities) == 1:
                    # good, we found only one, go to EntitySelected with curr_eid set
                    flow.transit(State.EntitySelected)
                    flow.keep(0)
                    return
                elif len(entities) > 1:
                    # It gave a shitload, go to RangeSelected with state.entities set
                    flow.transit(State.RangeSelected)
                    if curr_tid is not None:
                        flow.state.step = Step.TypeSelected
                    else:
                        type_range = actionUtil.get_type_range(entities)
                        if len(type_range) == 1:
                            flow.rank()
                            flow.state.step = Step.TypeSelected
                            flow.type = type_range[0]
                        else:
                            assert len(type_range) > 1
                            flow.state.step = Step.RangeInitiative
                            flow.types = type_range
                    return
        # either no keyword is given or no entity matched
        # TODO: handle these cases
        return


def sentimentStats(flow, decision):
    """Give an overall review for an entity
        If curr_eid is None, set 'cur_percent' to None
        If curr_eid is not None, set a 'cur_percent' field in session to be a float of num_pos/num_all
    """
    curr_eid = flow.eid
    if curr_eid is None:
        flow.sentiment_stats = None
        return
    else:
        query = Q(eid=curr_eid, sentiment__gt=0)
        num_pos = Comment.objects.filter(query).count()
        query = Q(eid=curr_eid, sentiment=0)
        num_neu = Comment.objects.filter(query).count()
        num_all = Comment.objects.filter(eid=curr_eid).count()
        flow.sentiment_stats = num_pos, num_neu, num_all
        """Handle by res gen
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
        """


def greeting(flow, decision):
    '''dummy'''
    return "Hi, I'm Weiss"


def unknownAction(flow, decision):
    '''dummy'''
    return "Sorry, I cannot handle this question."


def entityConfirmation(flow, decision):
    """Narrow down the target list
        If the state is in RangeInitiative substep, set tid and return
        If the state is in TypeSelected substep, set eid and return
    """
    state = flow.state
    assert (isinstance(state, RangeSelected))
    state = flow.state
    for case in switch(state.step):
        if case(Step.RangeInitiative):
            assert "tid" in decision
            tid = decision['tid']
            flow.type = tid
            flow.filter(lambda entity: entity.tid.tid == tid.value)
            flow.rank()
            state.step = Step.TypeSelected
        elif case(Step.TypeSelected):
            assert "idx" in decision
            flow.keep(decision["idx"])
        elif case():
            logger.error("No such step in RangeSelected state")

    if len(flow.entities) == 1:
        flow.eid = flow.entities[0].eid
        flow.transit(State.EntitySelected)
        return
    else:
        return
