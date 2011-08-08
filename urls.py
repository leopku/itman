from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.contrib import databrowse

from itman.services.models import Server, Switch, Service
from itman.services.views import server_list, server_detail

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

databrowse.site.register(Server)
databrowse.site.register(Switch)
databrowse.site.register(Service)

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'django.views.generic.simple.redirect_to', {'url':'/db/',}),
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^db/(.*)', login_required(databrowse.site.root)),
    url(r'^server/$', server_list),
    url(r'^server/(?P<server_id>\d+)/$', server_detail),

    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^accounts/login/$',  'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}),
    
    url(r'^comments/', include('django.contrib.comments.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
