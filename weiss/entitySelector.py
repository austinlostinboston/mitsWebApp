from switch import switch
from weiss.models import Comment, Entity, Type


def entitySelector(entities, tid, query):
    '''
    Public main entry of this module.
    Args:
        entities: a list of entities to be selected from
        tid: the type of these entities
        query: user's query
    Return:
        a single entity selected
    '''
    for case in switch(tid):
        if case(1):
            # Articles
            selected = _selectByTitle(entities, query)
            if len(selected) > 0:
                return _selectByNumOfReview(selected)
            else:
                return _selectByNumOfReview(entities)
        if case(2):
            # Restaurants
            selected = _selectByTitle(entities, query)
            if len(selected) > 0:
                return _selectByNumOfReview(selected)
            else:
                return _selectByNumOfReview(entities)
        if case(3):
            # Movies
            selected = _selectByTitle(entities, query)
            if len(selected) > 0:
                return _selectByNumOfReview(selected)
            else:
                return _selectByNumOfReview(entities)
        if case():
            # #$%^&*
            return entities[0]


def _selectByTitle(entities, query):
    '''
    Select entities from a list of entities such that the name
    of the entity fully contain the query
    '''
    entities = filter(lambda entity: query in entity.name, entities)
    return entities

def _selectByNumOfreview(entities):
    '''
    select from a list of entities based on # of reviews
    '''
    entities = map(lambda e: (e, Comment.objects.filter(eid=e.eid).count()), entities)
    entities.sort(key=lambda x: x[1], reverse=True)
    return entities[0][0]


def _selectMovieByReleaseYear(entities):
    '''
    select a entity from a list of entities based on the release year
    Assume that the entities are all film
    '''
    entities = map(lambda e: (e, _getYearFromDesc(e.description)), entities)
    entities.sort(key=lambda x: x[1], reverse=True)
    return entities[0][0]

def _getYearFromDesc(desc):
    '''
    return release year as int from the description of a film
    '''
    start = desc.find("Title:")
    year = desc.find("(", start)
    return int(desc[year+1:year+5])
