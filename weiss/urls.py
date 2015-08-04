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

This file defines the concrete control flow logic
"""
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'weiss.views.homepage'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'weiss/login.html'}),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^(?P<type_id>\d+)$','weiss.views.types'),
    url(r'^(?P<type_id>\d+)/(?P<entity_id>\d+)$','weiss.views.entities'),
    url(r'^types$', 'weiss.views.types'),
    url(r'^dashboard$', 'weiss.views.dashboard'),
    url(r'^confirmaction-(?P<aid>\d+)$', 'weiss.views.confirmaction'),
    url(r'^verbalresponse$', 'weiss.views.verbalresponse'),
    url(r'^actionboard$', 'weiss.views.actionboard'),
    url(r'^actionboard/(?P<action_id>\d+)$', 'weiss.views.actionboard'),
    url(r'^evaluate$', 'weiss.views.evaluate'),
    url(r'^evaluate/(?P<eval_type>\d+)$', 'weiss.views.evaluate'),
    url(r'^evaluate/rep_vote$', 'weiss.views.rep_vote'),
    url(r'^register', 'weiss.views.register'),
    url(r'^api/init$', 'weiss.views.init'),
    url(r'^api/inquire$', 'weiss.views.inquire'),
    url(r'^api/close$', 'weiss.views.close'),
)
