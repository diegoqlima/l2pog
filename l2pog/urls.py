from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    (r'^$', 'l2pog.views.login', None, 'login'),

    (r'^logged/$', 'l2pog.views.index', None, 'index'),
    (r'^logout/$', 'l2pog.views.logout', None, 'logout'),
    (r'^register/$', 'l2pog.views.register', None, 'register'),

    (r'^download/$', 'l2pog.views.download', None, 'download'),
    (r'^rates/$', 'l2pog.views.rates', None, 'rates'),
    (r'^contact/$', 'l2pog.views.contato', None, 'contato'),
    (r'^announce/$', 'l2pog.views.anuncios', None, 'anuncios'),
    (r'^partner/$', 'l2pog.views.socio', None, 'socio'),
    (r'^vote/$', 'l2pog.views.vote', None, 'vote'),
    (r'^countVote/$', 'l2pog.views.countVote', None, 'countVote'),
    (r'^cleanVote/$', 'l2pog.views.cleanVote', None, 'cleanVote'),




)