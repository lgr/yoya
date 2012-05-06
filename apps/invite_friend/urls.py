from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^$', invitation, {}, name='invite_friend'),
    url(r'^ade/$', send_random, {}, name='invitation_seed'),
)
