from switch import switch
from weiss.models import Comment, Entity, Type


def entitySelector(entities, tid):
    for case in switch(tid):
        if case(1):
            # Articles
            return selectByNumOfReview(entities)
        if case(2):
            # Restaurants
            return selectByNumOfReview(entities)
        if case(3):
            # Movies
            return selectMovieByReleaseYear(entities)
        if case():
            # #$%^&*
            return entities[0]


def selectByNumOfreview(entities):
    '''
    select a list of entities based on # of reviews
    '''
    entities = map(lambda e: (e, Comment.objects.filter(eid=e.eid).count()), entities)
    entities.sort(key=lambda x: x[1], reverse=True)
    return entities[0][0]


def selectMovieByReleaseYear(entities):
    '''
    select a entity from a list of entities based on the release year
    Assume that the entities are all film
    '''
    entities = map(lambda e: (e, getYearFromDesc(e.description)), entities)
    entities.sort(key=lambda x: x[1], reverse=True)
    return entities[0][0]

def getYearFromDesc(desc):
    '''
    return release year as int from the description of a film
    '''
    start = desc.find("Title:")
    year = desc.find("(", start)
    return int(desc[year+1:year+5])
