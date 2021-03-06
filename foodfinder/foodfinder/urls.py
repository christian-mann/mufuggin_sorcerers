from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'website.views.home', name='home'),
    url(r'^event/add/$', 'website.views.add_event', name='add_event'),
    url(r'^event/(?P<event_id>\d*)/$', 'website.views.manage_event', name='manage_event'),
    url(r'^event/leaderboard/$', 'website.views.leaderboard', name='leaderboard'),
    url(r'^vote/save/$', 'website.views.save_vote', name='save_vote'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^channel/', 'website.views.channel'),
    url(r'^event/new', 'website.views.create_event'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
