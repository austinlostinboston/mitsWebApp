from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

## Points to the urls.py in the weiss
urlpatterns = patterns('',
	url(r'', include('weiss.urls'))
)
