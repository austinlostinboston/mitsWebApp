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

A number of plugable methods for select desirable entity
from a list of entities.

The main entry is entitySelector, which is the only one needs to
be imported elsewhere

Author: Ming Fang
"""
from weiss.models import Comment, Type
from weiss.utils.switch import switch


def entitySelector(entities, tid):
    """
    Public main entry of this module.
    Args:
        entities: a list of entities to be selected from
        tid: the type of these entities
    Return:
        a single entity selected
    """
    for case in switch(tid):
        if case(Type.News):
            # Articles
            return _selectByNumOfReview(entities)

        if case(Type.Restaurant):
            # Restaurants
            return _selectByNumOfReview(entities)

        if case(Type.Movie):
            # Movies
            return _selectMovieByReleaseYear(entities)

        if case():
            # #$%^&*
            return entities[0]


def _selectByTitle(entities, query):
    """
    Select entities from a list of entities such that the name
    of the entity fully contain the query
    """
    entities = filter(lambda entity: query in entity.name, entities)
    return entities


def _selectByNumOfReview(entities):
    """
    select from a list of entities based on # of reviews
    """
    entities = map(lambda e: (e, Comment.objects.filter(eid=e.eid).count()), entities)
    entities.sort(key=lambda x: x[1], reverse=True)
    return entities[0][0]


def _selectMovieByReleaseYear(entities):
    """
    select a entity from a list of entities based on the release year
    Assume that the entities are all film
    """
    entities = map(lambda e: (e, _getYearFromDesc(e.description)), entities)
    entities.sort(key=lambda x: x[1], reverse=True)
    return entities[0][0]


def _getYearFromDesc(desc):
    """
    return release year as int from the description of a film
    """
    year = desc.split("\n")[2]
    return int(year[-5:-1])
