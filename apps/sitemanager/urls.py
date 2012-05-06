from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

from views import *
from feeds import LatestEntriesFeed, DlvritFeed


LANGUAGES = '|'.join([a for (a, b) in settings.LANGUAGES])


urlpatterns = patterns('',
    url(r'^feed/$', LatestEntriesFeed(), name='rss_feed'),
    url(r'^dlvrit_feed/$', DlvritFeed(), name='rss_dlvrit_feed'),
    url(r'^advert/$', contact, {'type': 'ADV'}, name='advertisement'),
    url(r'^contact/$', contact, {'type': 'CNT'}, name='contact'),
    url(r'^rules/$', direct_to_template,
        {'template': 'regulations.html'}, name='regulations'),
    url(r'^disclaimer/$', direct_to_template,
        {'template': 'disclaimer.html'}, name='disclaimer'),
    url(r'^faq/$', direct_to_template, {'template': 'faq.html'}, name='faq'),
    url(r'^fb_channel/$', direct_to_template,
        {'template': 'fb_channel.html'}, name='fb_channel'),
    url(r'^taringa/$', taringa, name='taringa'),
    url(r'^taringa/(?P<num>\d+)/$', taringa, name='taringa'),
    url(r'^language/(?P<lang_code>' + LANGUAGES + ')$',
        set_language, name='change_language'),
)
