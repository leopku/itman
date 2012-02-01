from django.conf.urls.defaults import *

from apps.teamstream import views

urlpatterns = patterns('',
    url(r'^$', views.report, name='report'),    
)