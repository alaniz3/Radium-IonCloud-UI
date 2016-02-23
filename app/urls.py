from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<doc_id>[0-9]+)/$', views.details, name='details'),
    url(r'^settings/$', views.configuration, name='settings')    
]