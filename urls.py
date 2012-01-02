from django.conf.urls.defaults import patterns, include, url
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'L2POG.views.home', name='home'),
    # url(r'^L2POG/', include('L2POG.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/l2pog/'}),
    (r'^l2pog/', include('l2pog.urls')),




    (r'^media/(.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'media/').replace('\\','/')}),

)
