from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('website.views',
   url(r'^$',                'loginfun'),
   url(r'^home/$',           'home'),
   url(r'^horaire/$',        'horaire'),
   url(r'^dossier/$',        'dossier'),
   url(r'^compte/$',         'compte'),
   url(r'^logout/$',         'user_logout'),
   url(r'^accounts/login/$', 'loginfun'),
)
