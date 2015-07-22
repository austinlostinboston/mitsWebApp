from django.shortcuts import render, redirect
from django.http import HttpResponse

# Django auth
from django.contrib.auth.decorators import login_required

# Handles login
from django.contrib.auth.models import User

from rest_framework.decorators import api_view

# Imports model objects to access database
from weiss.models import Comment, Entity, Type, MiniEntity, Evaluation, Method, History, Action
from django.db.models import Q, Max, Min

# Import django forms
from weiss.forms import RegistrationForm

# Python imports
import random
import os
import logging
import ast

# Import from personal moduls
from weiss.commentChooser import pageRankComment
from weiss.dialogue.actionUtil import initSession, getDialogHistory, confirmAciton
from weiss.dialogue.factory import getDialogueManager
from webapps.settings import BASE_DIR

logger = logging.getLogger(__name__)

# Create your views here.
@login_required
def homepage(request):
    context = {}
    dmgr = getDialogueManager()
    if request.method == 'POST':
        dmgr.handle(request)
    else:
        initSession(request)

    context['actions'] = [(action.value, action.name) for action in Action]
    context['dialog'] = getDialogHistory(request.user)
    return render(request, 'weiss/index.html', context)


@login_required
def confirmaction(request, aid):
    User = request.user
    logger.debug('aid:' + str(aid))
    logger.debug('user:' + str(User))
    confirmAciton(User, aid)
    context = {}
    context['actions'] = Action
    context['dialog'] = getDialogHistory(request.user)
    context['msg'] = 'thanks for you feedback'
    return render(request, 'weiss/index.html', context)
    # return redirect('')


@login_required
def verbalresponse(request):
    # Try to get query
    hid = request.GET['hid']
    try:
        history = History.objects.filter(hid=hid)[0]
    except IndexError:
        history = None

    if history is None:
        context = {}
        context['dialog'] = getDialogHistory(request.user)
        return render(request, 'weiss/index.html', context)

    response = history.response

    if request.method == 'GET':
        # Write text to file
        audio_file_path = os.path.abspath(BASE_DIR + ("/weiss/audio/%s.wav" % (request.user)))

        conv = ('flite -voice awb -t "%s" -o "%s"' % (response, audio_file_path))
        logger.debug("command:" + conv)
        os.system(conv)
        # response = commands.getoutput(conv)

        # Get query from request
        response = HttpResponse()
        f = open(audio_file_path, 'rb')
        response['Content-Type'] = 'audio/x-wav'
        response.write(f.read())
        f.close()
    return response


@login_required
def actionboard(request):
    logger.debug("%s" % (request))

    context = {}

    if request.method == 'POST':
        args = {}
        args['aid'] = int(request.POST['aid'])
        args['keywords'] = request.POST['queryinput']
        getDialogueManager().dispatch(request, None, args)
    else:
        initSession(request)

    context['actions'] = [(action.value, action.name) for action in Action]
    context['dialog'] = getDialogHistory(request.user)
    return render(request, 'weiss/actionboard.html', context)


def register(request):
    context = {}
    webpage = 'weiss/register.html'

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'weiss/register.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates form.
    if not form.is_valid():
        return render(request, 'weiss/register.html', context)

    # List of allowed usernames
    whitelist = ['aankney', 'mingf', 'wenjunw', 'yaozhou', 'awb']

    if request.method == 'POST':
        username = request.POST['username']
        if username in whitelist:
            # Adds account to User's model
            new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                                password=form.cleaned_data['password1'],
                                                first_name=form.cleaned_data['first_name'],
                                                last_name=form.cleaned_data['last_name'],
                                                email=form.cleaned_data['email'])
            # Make the user in active so they can't log in until they click on the email
            new_user.save()

            return render(request, 'weiss/index.html', context)
        else:
            context['errors'] = "Sorry, you're not on our preappoved list. Try back later."

    return render(request, webpage, context)


@login_required
def dashboard(request):
    context = {}

    # Choose 10 random records to show
    num_entities = Entity.objects.all().count()
    rand_entities = random.sample(range(num_entities), 10)
    sample_entities = Entity.objects.filter(eid__in=rand_entities)

    # Choose 10 random comments to show
    num_comments = Comment.objects.all().count()
    rand_comments = random.sample(range(num_comments), 10)
    sample_comments = Comment.objects.filter(cid__in=rand_comments)

    # Count records in each table
    comments = Comment.objects.all().count()
    entities = Entity.objects.all().count()
    types = Type.objects.all().count()

    # Add items to the http response
    context['comments'] = comments
    context['entities'] = entities
    context['types'] = types
    context['sampleComments'] = sample_comments
    context['sampleEntities'] = sample_entities

    return render(request, 'weiss/dashboard.html', context)


@login_required
def types(request, type_id):
    context = {}
    context['type_id'] = type_id

    if 'entity_search' in request.GET:
        search_terms = request.GET['entity_search']
        query = Q(tid=type_id, name__icontains=search_terms) | Q(tid=type_id, description__icontains=search_terms)
        all_entities = Entity.objects.filter(query)
    else:
        context['type'] = Type.objects.get(tid=type_id)
        all_entities = Entity.objects.filter(tid=type_id)

    context['all_entities'] = all_entities

    entities = Entity.objects.filter(tid=type_id).values('eid')
    comments = Comment.objects.filter(body__in=entities)

    lengthList = [0] * 50
    # Finds sentence lengths for all comments belonging to entity
    for comment in comments:
        text = comment.body
        sentences = text.split('.')
        for sentence in sentences:
            words = sentence.split(' ')
            wordCount = len(words)
            if wordCount < 50:
                lengthList[wordCount] += 1
    context['sentenceLength'] = lengthList

    # filePath = os.path.join(os.getcwd(), '/templates/weiss/data.csv')
    # with open('data.csv','wt') as csvfile:
    #   csvwriter = csv.writer(csvfile, delimiter=',')
    #   csvwriter.writerow(['Sentence Length','Frequency'])
    #   for i in range(len(lengthList)):
    #       csvwriter.writerow([i,lengthList[i]])

    return render(request, 'weiss/search.html', context)


@login_required
def entities(request, entity_id, type_id):
    context = {}

    all_reviews = Comment.objects.filter(eid=entity_id)
    context['all_reviews'] = all_reviews

    # Count positive, negative and neutral reviews
    pos_reviews = Comment.objects.filter(eid=entity_id, sentiment__gt=0)
    neg_reviews = Comment.objects.filter(eid=entity_id, sentiment__lt=0)
    neu_reviews = Comment.objects.filter(eid=entity_id, sentiment=0)

    context['pos_reviews'] = pos_reviews.count()
    context['neg_reviews'] = neg_reviews.count()
    context['neu_reviews'] = neu_reviews.count()

    return render(request, 'weiss/comments.html', context)


# @trasaction_atomic
@login_required
def evaluate(request, eval_type='0'):
    # Query set limit
    limit = 3

    # Get user's id
    user_id = User.objects.get(username=request.user).id

    # Default values
    eval_type = int(eval_type)
    context = {}
    context['eval'] = ""
    webpage = 'weiss/eval.html'

    # Evaluation Dashboard
    if eval_type == 0:
        rep_count = Evaluation.objects.filter(userid=user_id).values('eid').distinct().count()
        context['rep_count'] = rep_count
        context['rep_perc'] = str(rep_count * 100 / 30.0)[0:2]

    # Setup evaluation
    if eval_type > 0:
        user_evals = Evaluation.objects.filter(userid=user_id, mid__in=[0, 1, 2]).count()
        logger.debug(user_evals)

        entities = list(MiniEntity.objects.values_list('eid', flat=True))
        num_entities = len(entities)

        if user_evals > 0:
            last_eval = Evaluation.objects.filter(userid=user_id).order_by('evid').last().eid.eid
            # Checks to see if user has finished the list
            if int(last_eval) == int(entities[-1]):
                context['done'] = "You're finished!"
                return render(request, webpage, context)

            entity_index = entities.index(last_eval) + 1
        else:
            entity_index = 0

        this_eval = entities[entity_index]

        context['entity'] = Entity.objects.get(eid=this_eval)

        # Sets up eval framework for Text Summarization
        if eval_type == 1:
            pass

        if eval_type == 2:
            # Randomly choose positive (0) or negative (1) sentiment
            webpage = 'weiss/representative.html'
            posNeg = random.randint(0, 1)
            if posNeg == 0:
                query = Q(eid=this_eval, sentiment__gt=0)
                maxmin_sent = Comment.objects.filter(eid=this_eval).aggregate(Max('sentiment'))['sentiment__max']
            else:
                query = Q(eid=this_eval, sentiment__lt=0)
                maxmin_sent = Comment.objects.filter(eid=this_eval).aggregate(Min('sentiment'))['sentiment__min']
            sentiment_comment = Comment.objects.filter(eid=this_eval, sentiment=maxmin_sent)[0]
            comments = Comment.objects.filter(query)

            comment_list = []
            for comment in comments:
                comment_list.append(comment.body)

            if len(comment_list) > 0:
                # Randomly choose indexes for single baseline comment and sample comments
                num_sim_comments = len(comments)
                random_single = random.randint(0, num_sim_comments - 1)
                random_multiple = random.sample(range(num_sim_comments), limit)

                # Determines most representative comment
                index = pageRankComment(comment_list)

                # Matches the comment to the method which was used to select it
                sc = [sentiment_comment, 1]
                prc = [comments[index], 2]
                rc = [comments[random_single], 3]

                # Write info to context
                context['pagerank_choice'] = comments[index]
                context['random_choice'] = comments[random_single]
                context['sentiment_choice'] = sentiment_comment
                context['multiple_comments'] = [comments[i] for i in random_multiple]

                randomized_list = [rc, sc, prc]

                # loop through randomized list and grab each cid
                all_opt = []
                for comment in randomized_list:
                    all_opt.append([int(comment[0].cid), comment[1]])

                random.shuffle(randomized_list)
                context['randomized_list'] = randomized_list
                context['all_opt'] = all_opt
            else:
                context['commentChoice'] = 'no comments'

    return render(request, webpage, context)


@login_required
def rep_vote(request):
    context = {}
    webpage = 'weiss/representative.html'
    user = User.objects.get(username=request.user)

    if request.method == 'POST':
        # Extract id's from POST params
        method_id = request.POST['rep-mid']
        entity_id = request.POST['rep-eid']

        # List of comments matched with their methods
        all_opt = ast.literal_eval(request.POST['all_opt'])

        # Loop over the three methods
        for method in all_opt:
            comment_id = method[0]

            entity = Entity.objects.filter(id=entity_id).first()
            comment = Comment.objects.get(cid=comment_id)
            method_choice = Method.objects.get(mid=method[1])

            if int(method[1]) == int(method_id):
                score = 1
            else:
                score = 0
            new_eval = Evaluation(userid=user, eid=entity, mid=method_choice, cid=comment, score=score)
            new_eval.save()

    return redirect('/evaluate/2')


# API
@api_view(['GET'])
def init(request):
    if request.method == 'GET':
        dmgr = getDialogueManager()
        flow = dmgr.initFlow(request)
        return
