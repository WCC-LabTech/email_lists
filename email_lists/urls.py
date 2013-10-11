from django.conf.urls import patterns, include, url
from email_lists.views import *

urlpatterns = patterns('',
    url(r'^send_email/$', send_email, name='send_email'),
)
