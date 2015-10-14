from django.conf.urls import patterns, include, url

from chat.views import show_contact_list, check_username, send_message, show_chat, send_message_api

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'quests.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^contact_list/$', show_contact_list, name='contact_list'),
    url(r'^check_username/$', check_username, name='check_username'),
    url(r'^chat/(?P<id>\d+)/$', show_chat, name='chat'),
    url(r'^send_message/$', send_message, name='send_message'),
    url(r'^send_message_api/$', send_message_api, name='send_message_api'),
    )
