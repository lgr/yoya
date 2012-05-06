from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^$', show_random, {}, name='publication_show'),
    url(r'^random/$', show_random, {}, name='publication_random'),
    url(r'^new/$', add_new, {}, name='publication_new'),
    url(r'^(?P<pub_id>\d+)/$', show,
        {'with_context': True}, name='publication_show'),
    url(r'^(?P<pub_id>\d+)/preview/$', show,
        {}, name='publication_show_alone'),
    url(r'^(?P<pub_id>\d+)/plus/$', vote,
        {'positive': True}, name='publication_plus'),
    url(r'^(?P<pub_id>\d+)/minus/$', vote,
        {'positive': False}, name='publication_minus'),
    url(r'^(?P<pub_id>\d+)/accept/$', moderate,
        {'accept': True}, name='publication_accept'),
    url(r'^(?P<pub_id>\d+)/reject/$', moderate,
        {'accept': False}, name='publication_reject'),
    url(r'^(?P<pub_id>\d+)/front_page/$', moderate,
        {'front_page': True}, name='publication_front_page')
)
