from django.conf.urls import patterns, url

from archer.uploader import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^upload$', views.upload, name='upload'),
                       # ex: /packages/5/
                       url(r'^(?P<package_id>\d+)/$', views.show, name='show'),
                       # # ex: /packages/5/results/
                       # url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
                       # # ex: /packages/5/vote/
                       # url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)