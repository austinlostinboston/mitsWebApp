'''
Utility methods for queries
A resolver of user query. 
First step: take query as input, use classifier to map query to action
Second step: use actionUtil to generate resonse.

Author: Yao Zhou
'''

import os
import logging
import pickle

# Web import
from weiss.actions import *
from weiss.actionUtil import *
from weiss.models import History, Action
from django.shortcuts import render
from webapps.settings import BASE_DIR

#from django.template.context_processors import csrf

from liblinearutil import *
from feature import convert_query


def queryResolve(request):
    #Extract Add user query
    query = str(request.POST.get('queryinput', False))
    print ("query:%s" % query)
    # Load the trained model, which is in the same directory as this script
    m = load_model(os.path.abspath(BASE_DIR + "/weiss/%s" % 'model'))
    # Load feature file, which is also in the same directory
    infile = open(os.path.abspath(BASE_DIR + "/weiss/%s" % 'features'))
    feature_list = pickle.load(infile)
    # Class labels
    y = [1,2,3,4,5]
    # Convert query
    x = convert_query(query, feature_list, 'test')
    # Do the prediction
    p_label, p_val = predict(y, x, m, '-b 0')

    # p_label : real No of action in database
    # p_val : the possibility of each action

    dispatchFromQuery(request, query, int(p_label[0]))
    return


