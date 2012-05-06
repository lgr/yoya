from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^$', edit, name='profile_edit'),
    url(r'^(?P<user_id>\d+)/$', show, name='profile_show'),
)
