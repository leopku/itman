from django.conf.urls.defaults import *

from itman.teamstream import views

urlpatterns = patterns('',
    url(r'^$', views.main, name="main"),
    url(r'^close-active-period/$', views.close_active_period, name="close_active_period"),
    url(r'^resume-work/(?P<id>[0-9]+)/$', views.resume_work, name="resume_work"),
    url(r'^delete-plan/(?P<id>[0-9]+)/$', views.delete_plan, name="delete_plan"),
    url(r'^delete-period/(?P<id>[0-9]+)/$', views.delete_period, name="delete_period"),
    
    url(r'^ajax-delete-plan/$', views.ajax_delete_plan, name="ajax_delete_plan"),
    url(r'^ajax-delay-plan/$', views.ajax_delay_plan, name="ajax_delay_plan"),
    url(r'^resume-plan/(?P<id>[0-9]+)/$', views.resume_plan, name="resume_plan"),
    
    url(r'^ajax-show-plans/$', views.ajax_show_plans, name="ajax_show_plans"),
)
