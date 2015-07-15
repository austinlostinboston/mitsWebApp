"""
This module provides:
    a enum for actions
    a fixed number of actions that weiss supports


Author: Ming Fang <mingf@cs.cmu.edu>
"""
from django.db.models import Q

from weiss.models import Comment, Entity, Type, Types, Action, Step
from weiss.utils.switch import switch
from weiss.dialogue.entitySelector import entitySelector
from weiss.flows.states import *
from weiss.flows.factor import getFlowManager

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
        response
    """
    next_tid = int(random.uniform(1, 3.5))
    curr_eid = int(session['curr_eid'] or "0")
    logger.debug("next ran entity with next_tid: %s, curr_eid: %s" % (next_tid, curr_eid))
    eids = Entity.objects.filter(tid=next_tid).values_list('eid', flat=True)
    new_eid = curr_eid
    while (new_eid == curr_eid):
        new_eid = random.sample(eids, 1)[0]

    session['curr_eid'] = new_eid
    logger.debug("next ran entity has decided next eid: %s" % (new_eid))
    entity = Entity.objects.get(eid=new_eid)

    return "Sure, let's talk about \"%s\"" % entity.name

def nextRandomCmt(session, args):
    """Give a random comment of given entity

    Args:
        session: The session contains current context
            curr_eid: current entity id that is talking about

    Returns:
        response
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
    return res.body


def nextRandomPositiveCmt(session, args):
    """Give a random positive comment of given entity

    Args:
        session: The session contains current context
            curr_eid: the entity id that is talking about
            curr_cid: the current cid

    Returns:
        response
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
    return res.body


def nextRandomNegativeCmt(session, args):
    """Give a random negative comment of given entity

    Args:
        session: The session contains current context
            curr_eid: the entity id that is talking about
            curr_cid: the previous cid

    Returns:
        response
    """
    curr_eid = session['curr_eid']
    curr_cid = session['curr_cid']

    if curr_eid is None:
        return "What do you want to talk about?"

    logger.debug("next ran negative cmt with curr_eid: %s, curr_cid: %s" % (curr_eid, curr_cid))
    idxs = Comment.objects.filter(Q(eid=curr_eid), Q(sentiment__lt=0)).values_list('cid', flat=True)
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
        return nextRandomPositiveCmt(session, args)

    session['curr_cid'] = idx
    logger.debug("next ran neg cmt has decided to talk about %s" % res.cid)
    return res.body



def nextRandomOppositeCmt(session, args):
    """Give a random opposite comment of given entity

    Args:
        session: The session contains current context
            curr_sentiment: the value of current sentiment

    Returns:
        response
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
    type_obj = Types.objects.get(tid=tid)
    return "What %s would you like to talk about?" % type_obj.name


def entitySelection(session, args):
    """
    The logic:
        if no current tid, we talk about film
        if no keywords, ask what to talk about
        if there are 3 or more keywords:
            get entities that contain all (up to 3) keywords
                contain is defined as (description containing or title containing)
        if no entity meets the requirement:
            try one keyword at a time
        if any entities are found, pass to entitySelector, and we are good
        if no entity found by each one keyword: well, say sorry
    """
    curr_tid = session["curr_tid"] or 3 # film by default
    if args.has_key("tid"):
        curr_tid = args["tid"]
        session["curr_tid"] = curr_tid

    if args.has_key("keywords"):
        # select by first 3 keywords
        keywords = args["keywords"]
        keywords = keywords.split("#")
        logger.debug(keywords)
        if len(keywords) >= 3:
            keywords = keywords[:3]
        q = Q(tid=curr_tid)
        for keyword in keywords:
            q = q & (Q(description__icontains=keyword) | Q(name__icontains=keyword))
        entities = Entity.objects.filter(q)
        if len(entities) > 0:
            # good, we found some
            entity = entitySelector(entities, Type(curr_tid))
            session["curr_eid"] = entity.eid
            return "Sure, let's talk about \"%s\"" % entity.name
        else:
            # if there is no such entity, we loose the requirement
            keywords = args["keywords"].split("#")
            keywords.reverse()
            while len(keywords) > 0:
                keyword = keywords.pop()
                q = Q(tid=curr_tid, description__icontains=keyword) | Q(tid=curr_tid, name__icontains=keyword)
                entities = Entity.objects.filter(q)
                if len(entities) > 0:
                    entity = entitySelector(entities, Type(curr_tid))
                    session["curr_eid"] = entity.eid
                    return "Sure, let's talk about \"%s\"" % entity.name
            return "Sorry, I could not find a relevent entity to talk about."
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

def greeting(session, args):
    '''dummy'''
    return "Hi, I'm Weiss"

def unknownAction(session, args):
    '''dummy'''
    return "Sorry, I cannot handle this question."

def entityConfirmation(request, args):
    fmgr = getFlowManager()
    state = fmgr.lookUp(request.user)
    session = request.session
    assert(isinstance(state, RangeSelected))
    for case in switch(state.step):
        if case(Step.RangeInitiative):
            assert(args.has_key("tid"))
            tid = args['tid']
            session["curr_tid"] = tid.value
            state.filter(lambda entity : entity.tid == tid.value)
            state.transit(Step.TypeSelected)
        if case(Step.TypeSelected):
            assert(args.has_key("idx"))
            state.keep(args["idx"])
        if case():
            logger.error("No such step in RangeSelected state")

    if state.size() == 1:
        session['curr_eid'] = state.range[0].eid
        fmgr.transit(request, State.EntitySelected)
        return
    else:
        return









