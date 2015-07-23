## Weiss

Weiss, named after the German verb "to know", is a dialogue system aimed at answering subjective questions, as opposed to fact based systems like Siri, Evi, and Echo. Weiss is equipped to talk about three well defined domains; news, restaurants, and movies. Trained off of news article comments, restaurant reviews, and movie critiques, Weiss aims to understand user’s requests as well as generalize popular views within these categories. Using concepts from machine learning (classification, feature engineering), natural language processing (text summarization, named entity recognition, and parsing), and dialogue system (system-initiative and plan-based), Weiss is able to parse and understand questions, efficiently search and filter possible results, and return answers in small, intelligible segments.

## Dependencies

To install dependencies, type `sudo pip install -r requirements.txt`

> - **django**
> - **MySQLdb** 
> - **numpy** 
> - **sklearn**
> - **nltk**
> - **python-igraph**
> - **liblinear**
> - **termcolor**

## Installation 

### liblinear

> 1. extract liblinear-1.96.zip
> 2. cd liblinear-1.96
> 3. make
> 4. cd python;make
> 5. after step4, a file called liblinear.so.2 will be created under the directory that you just extracted
> 6. copy/replace that file into mitsWebApp/weiss/

## Testing
### Test cases format and state id:
    0. SystemInitiative
    1. TypeSelected
    2. EntitySelected
    3. CommentSelected
  
  `ID#Query#Current State ID#expected action id`
  
  Example:
  
  `1#Let's talk about movie#0#8`

  To stop Django from capturing `stdout`, add `NOSE_ARGS = ['--nocapture', '--nologcapture',]` to `settings.py`. 

  To run test without creating test db, add `TEST_RUNNER = 'weiss.tests.testUtils.NoDbTestRunner'` to `settings.py`.

  To run test, simply use the following:

  `python manage.py test`


## API
    ### Initilize a dialogue
    
    url: `/api/init`
    
    Request requirement:
        method GET
    The response format:
    `{`
    `   "fid" : fid`
    `}`
    
    ### Send a query
    
    url: `/api/inquire`
    
    Request requirement
        method POST
    The request format:
    `{`
    `   "fid" : fid,`
    `    "query" : query`
    `}`
    
    The response format:
    `{`
    `   "response" : response`
    `}`

    ### End a dialogue
    
    url: `/api/close`
    
    Request requirement
        method POST
    The request format:
    `{`
    `   "fid" : fid`
    `}`
