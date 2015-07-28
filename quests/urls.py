from django.conf.urls import patterns, include, url
from django.contrib import admin

from web.views import registration, index, restore_password, logout_view, login_view, EventView

from quests.settings import MEDIA_ROOT

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'quests.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', index, name='index'),
    url(r'^event/(?P<pk>\d+)/$', EventView.as_view(), name='event'),
    url(r'^register/$', registration, name='register'),
    url(r'^restore/$', restore_password, name='restore'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
)
