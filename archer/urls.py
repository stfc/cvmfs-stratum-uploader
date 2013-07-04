from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'archer.views.home', name='home'),
                       # url(r'^archer/', include('archer.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       # url(r'^grappelli/', include('grappelli.urls')),
                       url(r'^$', include('uploader.urls')),
                       url(r'^uploader/', include('uploader.urls', namespace='uploader')),
                       url(r'^admin/', include(admin.site.urls)),
)
