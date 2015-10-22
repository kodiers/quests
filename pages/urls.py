from django.conf.urls import patterns, url

from pages.views import FAQListView, PagesDetailView, ContactsDetailView, send_email_message

urlpatterns = patterns('',
                       url(r'^faq/$', FAQListView.as_view(), name='faq'),
                       url(r'^page/(?P<url>\w+)/$', PagesDetailView.as_view(), name='pages'),
                       url(r'^contacts/(?P<url>\w+)/$', ContactsDetailView.as_view(), name='contacts'),
                       url(r'^send_email/$', send_email_message, name='send_email'),
                       )
