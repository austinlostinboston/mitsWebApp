"""
    Copyright 2015 Austin Ankney, Ming Fang, Wenjun Wang and Yao Zhou

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
## Import builtins
import random
import os
import re

## Import from weiss
from weiss.models import Action, Type, Types, State, Comment, Entity
from django.db.models import Q
from bs4 import BeautifulSoup

def responseHandler(flow, test=False):
    ## Get directory
    cur_dir = os.path.dirname(__file__)

    ## read responses.xml to memory
    soup = BeautifulSoup(open(cur_dir + '/responses.xml'))

    ## Set response
    response = 'Empty response: We are experiencing problems, sorry!'

    ## Grab information from flow
    user = flow.user  # a str, None for unregistered user
    user_id = flow.user_id  # a int
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
        if flow.type.name.lower() == 'news':
            type_name = 'news article'
        else:
            type_name = flow.type.name.lower()
    else:
        type_name = None
    types = flow.types

    ## Text variables
    entity_object = flow.entity
    comment_object = flow.comment
    sent_stats = flow.sentiment_stats
    summary = flow.summary

    if summary:
        summary_body = summary.body
        # print "[summary]" + summary_body
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
    
    ## Grabs num of entities
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

    print "[Response ID]: " + str(rsp_id)
    response = soup.find('message', {'id': rsp_id}).text

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
            #print msgParts[str(part)]
            #print "[" + str(part) + "]"
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


def placeSentiment(sentiment_stats, msgParts):
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

        msgParts['popularity'] = popular
        msgParts['percent'] = str(int(percent*100)) + '%'

        # response = response.replace("[popularity]", popular)
        # response = response.replace("[percent]", str(int(percent*100)) + '%')

        # return response


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


def buildSummary(summary_body, sentence_num):
    regex = re.compile(r'\d+\#')

    ## Check to see if body is summary or just comment.
    if regex.search(summary_body) is not None:

        # print "[summar] " + summary_body
        if summary_body:
            sentences = summary_body.split("\n")
            ranked_sentences = []
            sum_str = ''

            for sentence in sentences:
                rank_sent = sentence.split('#')
                ranked_sentences.append([int(rank_sent[0]),rank_sent[1]])

            ranked_sentences = sorted(ranked_sentences)
            # print ranked_sentences

            for sent in ranked_sentences[0:sentence_num]:
                # print sent
                sum_str += sent[1] + " "

            return sum_str
        else:
            return str(None)
    else:
        return summary_body
