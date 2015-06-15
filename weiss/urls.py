from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'weiss.views.homepage'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'weiss/login.html'}),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^(?P<type_id>\d+)$','weiss.views.types'),
    url(r'^(?P<type_id>\d+)/(?P<entity_id>\d+)$','weiss.views.entities'),
    url(r'^types$', 'weiss.views.types'),
    url(r'^dashboard$', 'weiss.views.dashboard'),
    url(r'^actionboard$', 'weiss.views.actionboard'),
    url(r'^actionboard/(?P<action_id>\d+)$', 'weiss.views.actionboard'),
    url(r'^evaluate$', 'weiss.views.evaluate'),
    url(r'^evaluate/(?P<eval_type>\d+)$', 'weiss.views.evaluate'),
    url(r'^evaluate/rep_vote$', 'weiss.views.rep_vote'),
)
