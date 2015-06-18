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
    tid = models.ForeignKey('Type', db_column='tid')
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'entity'


class Type(models.Model):
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

class Action(models.Model):
    aid = models.AutoField(primary_key=True)
    name = models.TextField()
    method = models.TextField()

    class Meta:
        managed = False
        db_table = 'action'

class History(models.Model):
    hid = models.BigIntegerField(primary_key=True)
    userid = models.ForeignKey(User, db_column='userid')
    query = models.TextField()
    response = models.TextField()
    time = models.DateTimeField()
    aid = models.ForeignKey(Action, db_column='aid', blank=True, null=True)
    desired_aid = models.IntegerField(blank=True, null=True)
    eid = models.ForeignKey(Entity, db_column='eid', blank=True, null=True)
    feedback = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'history'


class SummaryBody(models.Model):
    sbid = models.BigIntegerField(primary_key=True)
    cid = models.ForeignKey(Comment, db_column='cid')
    mid = models.ForeignKey(Method, db_column='mid')
    body = models.TextField()

    class Meta:
        managed = False
        db_table = 'summary_body'


class SummarySource(models.Model):
    ssid = models.BigIntegerField(primary_key=True)
    sbid = models.ForeignKey(SummaryBody, db_column='sbid')
    cid = models.ForeignKey(Comment, db_column='cid')

    class Meta:
        managed = False
        db_table = 'summary_source'


