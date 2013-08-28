from django.conf.urls import patterns, url

from archer.appsetup import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^admin/$', views.admin, name='admin'),
                       url(r'^filesystems/$', views.filesystems, name='filesystems'),
)