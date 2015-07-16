"""
This module provides:
    a fixed number of actions that weiss supports


Author: Ming Fang <mingf@cs.cmu.edu>
"""
from django.db.models import Q

from weiss.models import Comment, Entity, Type, Types, Action, Step, State
from weiss.utils.switch import switch
from weiss.dialogue.entitySelector import entitySelector
from weiss.flows.states import *
from weiss.flows.factory import getFlowManager

import random
import logging

logger = logging.getLogger(__name__)

def nextRandomEntity(flow, decision):
    """Start next conversation

    decision:
        session: The session contains current context
            next_tid: the type id that the next conversation is going to talk about
            curr_eid: current entity id that is talking about

    Returns:
    """
    next_tid = int(random.uniform(1, 3.5))
    curr_eid = flow.eid
    logger.debug("next ran entity with next_tid: %s, curr_eid: %s" % (next_tid, curr_eid))
    eids = Entity.objects.filter(tid=next_tid).values_list('eid', flat=True)
    new_eid = curr_eid
    while (new_eid == curr_eid):
        new_eid = random.sample(eids, 1)[0]

    flow.eid = new_eid
    logger.debug("next ran entity has decided next eid: %s" % (new_eid))

    """ Handle by Response Generator
    entity = Entity.objects.get(eid=new_eid)

    return "Sure, let's talk about \"%s\"" % entity.name
    """

    flow.transit(State.EntitySelected)
    return

def nextRandomCmt(flow, decision):
    """Give a random comment of given entity

    decision:
        session: The session contains current context
            curr_eid: current entity id that is talking about

    Returns:
    """
    curr_eid = flow.eid
    curr_cid = flow.cid
    logger.debug("next ran cmt with curr_eid: %s" % curr_eid)
    idx = 0
    if curr_eid is None:
        num_cmt = Comment.objects.count()
        idx = random.randint(0, num_cmt - 1)
    else:
        curr_eid = int(curr_eid)
        idxs = Comment.objects.filter(eid=curr_eid).values_list('cid', flat=True)
        if (len(idxs) == 0):
            return "No such comment"
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
    """Give a random positive comment of given entity
        If curr_eid is None, return directly
        If no positive cmt in curr_eid, set curr_cid = None and return
        If there is one cmt found, set curr_cid and return
    decision:
        session: The session contains current context
            curr_eid: the entity id that is talking about
            curr_cid: the current cid

    Returns:
    """
    curr_eid = flow.eid
    curr_cid = flow.cid

    logger.debug("next ran positive cmt with curr_eid: %s, curr_cid: %s" % (curr_eid, curr_cid))

    if curr_eid is None:
        logger.info("No eid given")
        #return "What do you want to talk about?"
        return

    idxs = Comment.objects.filter(Q(eid=curr_eid), Q(sentiment__gt=0)).values_list('cid', flat=True)
    idx = curr_cid
    if (len(idxs) == 0):
        flow.cid = None
        #return "No such comments"
        logger.info("No such comments")
        return
    else:
        while (idx == curr_cid):
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


def nextRandomNegativeCmt(flow, decision):
    """Give a random negative comment of given entity
        If curr_eid is None, return directly
        If no negative cmt in curr_eid, set curr_cid = None and return
        If there is one cmt found, set curr_cid and return

    decision:
        session: The session contains current context
            curr_eid: the entity id that is talking about
            curr_cid: the previous cid

    Returns:
    """
    curr_eid = flow.eid
    curr_cid = flow.cid

    if curr_eid is None:
        logger.info("No eid given")
        return

    logger.debug("next ran negative cmt with curr_eid: %s, curr_cid: %s" % (curr_eid, curr_cid))
    idxs = Comment.objects.filter(Q(eid=curr_eid), Q(sentiment__lt=0)).values_list('cid', flat=True)
    idx = curr_cid
    if (len(idxs) == 0):
        flow.cid = None
        #return "No such comments"
        return
    else:
        while (idx == curr_cid):
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
    """Give a random opposite comment of given entity
        If curr_cid is None, return directly
        If this cmt is positive, call negative cmt executor
        If this cmt is negative, call positive cmt executor
        If this cmt is 0, call positive cmt executor

    decision:
        session: The session contains current context
            curr_sentiment: the value of current sentiment

    Returns:
    """
    comment = flow.comment
    curr_sentiment = None

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
    """Select a type
        If there is tid in decision, set it accordingly
        If there is no tid in decision, talk movies :)
        curr_tid is always set upon return
    """
    tid = decision.get("tid", 3) # imdb by default :)
    flow.type = tid
    flow.transit(State.TypeSelected)
    """Handle by res gen
    type_obj = Types.objects.get(tid=tid)
    return "What %s would you like to talk about?" % type_obj.name
    """
    return

def entitySelection(flow, decision):
    """
    The logic:
        None test for curr_tid
        None test for keywords
        if there are 3 or more keywords:
            get entities that contain all (up to 3) keywords
                contain is defined as (description containing or title containing)
        if no entity meets the requirement:
            try one keyword at a time
        if any entities are found, pass to entitySelector, and we are good
        if no entity found by each one keyword: well, say sorry
    """
    curr_tid = flow.tid
    """
    if decision.has_key("tid"):
        curr_tid = decision["tid"]
        session["curr_tid"] = curr_tid
    """
    if decision.has_key("keywords"):
        # select by first 3 keywords
        keywords = decision["keywords"]
        keywords = keywords.split("#")
        logger.debug(keywords)
        if len(keywords) >= 3:
            keywords = keywords[:3]

        if curr_tid is not None:
            base = Q(tid=curr_tid)
        else:
            base = Q()

        print keywords

        for keyword in keywords:
            q = base & (Q(description__icontains=keyword) | Q(name__icontains=keyword))
        entities = Entity.objects.filter(q)
        flow.entities = entities
        if len(entities) == 1:
            # good, we found only one, go to EntitySelected state with curr_eid set
            #entity = entitySelector(entities, Type(curr_tid))
            flow.transit(State.EntitySelected)
            flow.keep(0)
            return
            #return "Sure, let's talk about \"%s\"" % entity.name
        elif len(entities) > 1:
            # It gave a shitload, go to RangeSelected with state.range set
            flow.transit(State.RangeSelected)
            if curr_tid is not None:
                state.step = Step.TypeSelected
            else:
                state.step = Step.RangeInitiative
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
                    # It gave a shitload, go to RangeSelected with state.range set
                    flow.transit(State.RangeSelected)
                    if curr_tid is not None:
                        state.step = Step.TypeSelected
                    else:
                        state.step = Step.RangeInitiative
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
        num_all = Comment.objects.filter(eid=curr_eid).count()
        flow.sentiment_stats = float(num_pos) / num_all
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
        If the state is in RangeInitiative substep, set curr_tid and return
        If the state is in TypeSelected substep, set curr_eid and return
    """
    assert(isinstance(state, RangeSelected))
    state = flow.state
    for case in switch(state.step):
        if case(Step.RangeInitiative):
            assert(decision.has_key("tid"))
            tid = decision['tid']
            flow.type = tid
            flow.filter(lambda entity : entity.tid == tid.value)
            state.transit(Step.TypeSelected)
        if case(Step.TypeSelected):
            assert(decision.has_key("idx"))
            flow.keep(decision["idx"])
        if case():
            logger.error("No such step in RangeSelected state")

    if len(flow.entities) == 1:
        flow.eid = flow.entities[0].eid
        flow.transit(State.EntitySelected)
        return
    else:
        return









