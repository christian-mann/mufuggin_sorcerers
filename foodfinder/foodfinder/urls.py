from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'website.views.home', name='home'),
    url(r'^event/add/$', 'website.views.add_event', name='add_event'),
    url(r'^event/(?P<event_id>\d*)/$', 'website.views.manage_event', name='manage_event'),

    url(r'^admin/', include(admin.site.urls)),
)
