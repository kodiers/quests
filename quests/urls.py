from django.conf.urls import patterns, include, url
from django.contrib import admin

from web.views import registration, index, restore_password, logout_view, login_view, EventView, confirm_join_event, \
    create_team, join_team, join_event, PlayerView, OrganizerView, show_my_profile, create_event, add_task, delete_task
    #join_event_as_player, join_as_team

from quests.settings import MEDIA_ROOT

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'quests.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', index, name='index'),
    url(r'^event/(?P<pk>\d+)/$', EventView.as_view(), name='event'),
    url(r'^player/(?P<pk>\d+)/$', PlayerView.as_view(), name='player'),
    url(r'^organizer/(?P<pk>\d+)/$', OrganizerView.as_view(), name='organizer'),
    url(r'^my_profile/(?P<pk>\d+)/$', show_my_profile, name='player_profile'),
    url(r'^confirm_join/(?P<pk>\d+)/$', confirm_join_event, name='confirm_join'),
    url(r'^join/(?P<flag>\w+)/$', join_event, name='join_event'),
    url(r'^create_team/$', create_team, name='create_team'),
    url(r'^create_event/$', create_event, name='create_event'),
    url(r'^create_event/(?P<pk>\d+)/$', create_event, name='edit_event'),
    url(r'^add_task/$', add_task, name='add_task'),
    url(r'^delete_task/$', delete_task, name='delete_task'),
    url(r'^join_team', join_team, name='join_team'),
    url(r'^create_team/(?P<event_pk>\d+)/$', create_team, name='create_and_register_team'),
    url(r'^register/$', registration, name='register'),
    url(r'^restore/$', restore_password, name='restore'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
)
