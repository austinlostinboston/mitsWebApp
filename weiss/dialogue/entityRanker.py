"""
A number of plugable methods for ranking a list of entities

The main entry is ranked method

Author: Ming Fang
"""
from weiss.models import Comment, Type
from weiss.utils.switch import switch


def ranked(entities, tid):
    """
    Public main entry of this module.
    Args:
        entities: a list of entities to be ranked
        tid: the type of these entities
    Return:
        a single entity selected
    """
    for case in switch(tid):
        if case(Type.News):
            # Articles
            return _ranked_by_num_reviews(entities)

        elif case(Type.Restaurant):
            # Restaurants
            return _ranked_by_num_reviews(entities)

        elif case(Type.Movie):
            # Movies
            return _ranked_by_num_reviews(entities)

        elif case():
            # #$%^&*
            return entities


def _ranked_by_num_reviews(entities):
    """
    select from a list of entities based on # of reviews
    """
    return sorted(entities, key=_get_num_of_reviews, reverse=True)

def _get_num_of_reviews(entity):
    return Comment.objects.filter(eid=entity.eid).count()


