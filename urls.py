from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.template import RequestContext
from django.views.generic.simple import direct_to_template
from sitemap import sitemaps

from apps.sitemanager.views import start

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^registration/', include('registration.backends.default.urls')),
    url(r'^social/', include('socialregistration.urls',
                             namespace='socialregistration')),
    url(r'^$', start, {'active': 'index'}, name='index'),
    url(r'^(?P<page>\d+)/$', start, {'active': 'index'}, name='index'),
    url(r'^waiting/$', start, {'active': 'waiting_room'}, name='waiting_room'),
    url(r'^waiting/(?P<page>\d+)/$', start,
        {'active': 'waiting_room'}, name='waiting_room'),
    url(r'^top/$', start, {'active': 'top'}, name='top'),
    url(r'^top/(?P<page>\d+)/$', start, {'active': 'top'}, name='top'),
    url(r'^moderate/$', start, {'active': 'moderate'}, name='moderate'),
    url(r'^moderate/(?P<page>\d+)/$', start,
        {'active': 'moderate'}, name='moderate'),
    url(r'^login/$', 'apps.profiles.views.login_wrapper', name="login"),
    url(r'^logout/$', logout,
        {'template_name': 'registration/logout.html'}, name='logout'),
    url(r'^site/', include('apps.sitemanager.urls')),
    url(r'^pub/', include('apps.publications.urls')),
    url(r'^my_secret_admin_panel/', include(admin.site.urls)),
    url(r'^profile/', include('apps.profiles.urls')),
    url(r'^spider/', include('apps.spider.urls')),
    url(r'^inv/', include('apps.invite_friend.urls')),
    url(r'^sitemap\.xml$',
        'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^robots\.txt$', direct_to_template,
        {'template': 'robots.txt', 'mimetype': 'text/plain'})
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
    urlpatterns += staticfiles_urlpatterns()
