from django.conf.urls import patterns, include, url
from django.contrib import admin

from web.views import registration, index, restore_password, logout_view, login_view, EventView, confirm_join_event, \
    create_team, join_team, join_event, PlayerView, OrganizerView, show_my_profile, create_event, add_task, delete_task, \
    edit_task, delete_event, delete_team, leave_team, unregister_event, upload_photos, delete_photo, play_event, \
    start_task, task_answer, complete_event, show_my_organizer_profile, EventsListView, AllEventsListView, \
    search_events_view, PlayersListView, search_players_view, OrganizerListView, search_organizers_view

from pages.urls import urlpatterns as pages_url

from filebrowser.sites import site

from quests.settings import MEDIA_ROOT

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'quests.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', index, name='index'),
    url(r'^event/(?P<pk>\d+)/$', EventView.as_view(), name='event'),
    url(r'^player/(?P<pk>\d+)/$', PlayerView.as_view(), name='player'),
    url(r'^organizer/(?P<pk>\d+)/$', OrganizerView.as_view(), name='organizer'),
    url(r'^my_profile/$', show_my_profile, name='player_profile'),
    url(r'^my_organizer_profile/$', show_my_organizer_profile, name='organizer_profile'),
    url(r'^confirm_join/(?P<pk>\d+)/$', confirm_join_event, name='confirm_join'),
    url(r'^join/(?P<flag>\w+)/$', join_event, name='join_event'),
    url(r'^unregister_event/$', unregister_event, name='unregister_event'),
    url(r'^create_team/$', create_team, name='create_team'),
    url(r'^create_event/$', create_event, name='create_event'),
    url(r'^create_event/(?P<pk>\d+)/$', create_event, name='edit_event'),
    url(r'^add_task/$', add_task, name='add_task'),
    url(r'^delete_task/$', delete_task, name='delete_task'),
    url(r'^edit_task/$', edit_task, name='edit_task'),
    url(r'^delete_event/$', delete_event, name='delete_event'),
    url(r'^join_team', join_team, name='join_team'),
    url(r'^create_team/(?P<event_pk>\d+)/$', create_team, name='create_and_register_team'),
    url(r'^delete_team/$', delete_team, name='delete_team'),
    url(r'^leave_team/$', leave_team, name='leave_team'),
    url(r'^upload_photo/$', upload_photos, name='upload_photos'),
    url(r'^delete_photo/$', delete_photo, name='delete_photo'),
    url(r'^play_event/(?P<pk>\d+)/$', play_event, name='play_event'),
    url(r'^start_task/$', start_task, name='start_task'),
    url(r'^task_answer/$', task_answer, name='task_answer'),
    url(r'^complete_event/$', complete_event, name='complete_event'),
    url(r'^register/$', registration, name='register'),
    url(r'^restore/$', restore_password, name='restore'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^events/$', EventsListView.as_view(), name='events'),
    url(r'^events/all/$', AllEventsListView.as_view(), name='all_events'),
    url(r'^events/search/$', search_events_view, name='search_events'),
    url(r'^players/$', PlayersListView.as_view(), name='players'),
    url(r'^players/search/$', search_players_view, name='search_players'),
    url(r'^organizers/$', OrganizerListView.as_view(), name='organizers'),
    url(r'^organizers/search/$', search_organizers_view, name='search_organizers'),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    url(r'^messages/', include('chat.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^pages/', include(pages_url)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)
