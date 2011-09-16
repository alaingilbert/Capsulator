from django.conf.urls.defaults import *
from settings import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s/templates/css/' % PROJECT_ROOT}),
   url(r'^', include('website.urls')),
   (r'^admin/doc/', include('django.contrib.admindocs.urls')),
   (r'^admin/', include(admin.site.urls)),
)
