from django.conf.urls import url, patterns
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<doc_id>[0-9]+)/$', views.details, name='details'),
    url(r'^settings/$', views.configuration, name='settings')    
]

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'files/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))