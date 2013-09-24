from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from archer.projects import views

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'archer.views.home', name='home'),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       url(r'^$', include('archer.projects.urls'), name='index'),
                       url(r'^pages/', include('django.contrib.flatpages.urls', namespace='pages')),
                       url(r'^setup/', include('archer.appsetup.urls', namespace='appsetup')),
                       url(r'^projects/', include('archer.projects.urls', namespace='projects')),
                       url(r'^packages/', include('archer.packages.urls', namespace='packages')),
                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls), name='admin'),
                       url(r'^unauthenticated$', views.unauthenticated, name='unauthenticated')
)
urlpatterns += patterns('django.contrib.flatpages.views',
                        url(r'^getting-started/$', 'flatpage', {'url': '/getting-started/'}, name='getting-started'),
)