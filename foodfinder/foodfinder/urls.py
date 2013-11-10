from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'website.views.home', name='home'),

    url(r'^event/(?P<event_id>\d*)/$', 'website.views.manage_event', name='manage_event'),
    
    url(r'accounts/', include('allauth.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^facebook/', 'website.views.facebook'),
    url(r'^channel/', 'website.views.channel'),
)
