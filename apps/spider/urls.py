from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from views import *

SITES = '|'.join(ACTIVE_SITES)

urlpatterns = patterns('',
    url(r'^$', direct_to_template,
        {'template': 'spider/list_sites.html',
         'extra_context': {'active': 'spider'}}, name='spider'),
    url(r'^(?P<site_id>' + SITES + ')/$', start, name='spider_select'),
    url(r'^all/$', start, {'site_id': 'all', }, name='spider_select_all'),
    url(r'^add/$', add_remote, name='spider_add'),
)
