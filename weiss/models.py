# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from enum import Enum

"""
Note: This file also contains enumerations for `Type`, `Actiion`, `State`
      To avoid conflict:
      previous database model `Type` has been rename to `Types`
      previous database model `Action` has been rename to `Actions`

"""
class Type(Enum):
    News = 1
    Restaurant = 2
    Movie = 3
    Unknown = 10

class Action(Enum):
    """
    Enum for actions.
    Note:
        wherever referred to as aid, referred to this enum
        To get a int representation, use aid.value
        To get a str representation, use aid.name
    """
    NextRandomComment = 1
    NextOppositeComment = 2
    NextPositiveComment = 3
    NextNegativeComment = 4
    NextRandomEntity = 5
    SentimentStats = 6
    EntitySelection = 7
    TypeSelection = 8
    Greeting = 9
    UnknownAction = 10
    EntityConfirmation = 11


class State(Enum):
    """
    wherever referred as sid, referred this enum
    To get the actual int representation, use sid.value
    To get str representation, use sid.name
    """
    SystemInitiative = 0
    TypeSelected = 1
    EntitySelected = 2
    CommentSelected = 3
    RangeSelected = 4

class Step(Enum):
    """
    sub state in RangeSelected state
    """
    RangeInitiative = 1
    TypeSelected = 2

class API(Enum):
    Init = 1
    Query = 2
    Close = 3




class Comment(models.Model):
    cid = models.BigIntegerField(primary_key=True)
    eid = models.ForeignKey('Entity', db_column='eid')
    body = models.TextField()
    rating = models.FloatField()
    author = models.TextField()
    title = models.TextField()
    time = models.DateField()
    sentiment = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'comment'


class Entity(models.Model):
    eid = models.BigIntegerField(primary_key=True)
    id = models.TextField()
    source = models.TextField()
    description = models.TextField()
    url = models.TextField()
    tid = models.ForeignKey('Types', db_column='tid')
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'entity'


class Types(models.Model):
    tid = models.AutoField(primary_key=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'type'


class Evaluation(models.Model):
    evid = models.IntegerField(primary_key=True)
    userid = models.ForeignKey(User, db_column='userid')
    eid = models.ForeignKey(Entity, db_column='eid')
    mid = models.ForeignKey('Method', db_column='mid')
    cid = models.ForeignKey(Comment, db_column='cid')
    score = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'evaluation'


class Method(models.Model):
    mid = models.AutoField(primary_key=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'method'


class MiniEntity(models.Model):
    eid = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'mini_entity'


class Summary(models.Model):
    cid = models.ForeignKey(Comment, db_column='cid')
    mid = models.ForeignKey(Method, db_column='mid')
    body = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'summary'
        unique_together = (('cid', 'mid'),)

class Actions(models.Model):
    aid = models.AutoField(primary_key=True)
    name = models.TextField()
    method = models.TextField()

    class Meta:
        managed = False
        db_table = 'action'

class History(models.Model):
    hid = models.BigIntegerField(primary_key=True)
    userid = models.IntegerField()
    query = models.TextField()
    response = models.TextField()
    time = models.DateTimeField()
    aid = models.ForeignKey(Actions, db_column='aid', blank=True, null=True)
    desired_aid = models.IntegerField(blank=True, null=True)
    eid = models.ForeignKey(Entity, db_column='eid', blank=True, null=True)
    feedback = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'history'


class Summary(models.Model):
    sbid = models.BigIntegerField(primary_key=True)
    cid = models.ForeignKey(Comment, db_column='cid')
    rank = models.IntegerField()
    mid = models.ForeignKey(Method, db_column='mid')
    body = models.TextField()

    class Meta:
        managed = False
        db_table = 'summary'


