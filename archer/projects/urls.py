from django.conf.urls import patterns, url

from archer.projects import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^(?P<project_id>\d+)/$', views.show, name='show'),
                       url(r'^(?P<project_id>\d+)/upload/$', views.UploadView.as_view(), name='upload'),


                       url(r'^(?P<project_id>\d+)/mkdir/$', views.mkdir, name='mkdir'),
                       url(r'^(?P<project_id>\d+)/rmdir=(?P<path>\S+)$', views.rmdir, name='rmdir'),
                       url(r'^(?P<project_id>\d+)/rm=(?P<path>\S+)$', views.rmdir, name='rm'),
)