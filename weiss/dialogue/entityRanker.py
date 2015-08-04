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


