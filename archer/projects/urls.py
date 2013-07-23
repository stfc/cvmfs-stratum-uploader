from django.conf.urls import patterns, url

from archer.projects import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^(?P<project_id>\d+)/$', views.show, name='show'),
                       url(r'^(?P<project_id>\d+)/upload$', views.UploadView.as_view(), name='upload'),
)