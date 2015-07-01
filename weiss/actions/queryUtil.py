'''
Utility methods for queries
A resolver of user query.
First step: take query as input, use classifier to map query to action
Second step: use actionUtil to generate resonse.

Author: Yao Zhou, Ming Fang
'''

import os
import logging
import pickle

# Web import
from weiss.models import History, Action
from django.shortcuts import render
from webapps.settings import BASE_DIR

from weiss.classifier.factory import getClassifier
from weiss.actions.actionUtil import dispatch


def queryResolve(request):
    classifier = getClassifier()
    #Extract Add user query
    query = str(request.POST.get('queryinput', False))
    print ("query:%s" % query)

    curr_state = request.session['curr_state']

    args = classifier.action_info(query, curr_state)

    dispatch(request, query, args)
    return


