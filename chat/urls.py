from django.conf.urls import patterns, include, url

from chat.views import show_contact_list, new_message, check_username

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'quests.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^contact_list/$', show_contact_list, name='contact_list'),
    url(r'^new_message/$', new_message, name='new_message'),
    url(r'^check_username/$', check_username, name='check_username'),
    )
