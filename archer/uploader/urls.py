from django.conf.urls import patterns, url

from archer.uploader import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^projects/(?P<project_id>\d+)/$', views.show_project, name='show_project'),
                       url(r'^projects/(?P<project_id>\d+)/upload$', views.UploadView.as_view(), name='upload'),
                       # url(r'^upload$', views.UploadView.as_view(), name='upload'),
                       # ex: /packages/5/
                       url(r'^(?P<package_id>\d+)/$', views.show_package, name='show'),
                       url(r'^(?P<package_id>\d+)/deploy$', views.deploy, name='deploy'),
                       url(r'^(?P<package_id>\d+)/remove$', views.remove, name='remove'),
                       # # ex: /packages/5/results/
                       # url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
                       # # ex: /packages/5/vote/
                       # url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)