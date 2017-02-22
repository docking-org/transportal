from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^fdadjango/', include('fdadjango.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^transporters/(?P<transporter_id>\w+)/$', 'fdadjango.transporterDatabase.views.transporter'),
    (r'^index/$', 'fdadjango.transporterDatabase.views.index'),
    (r'^about/$', 'fdadjango.transporterDatabase.views.about'),
    (r'^contact/$', 'fdadjango.transporterDatabase.views.contact'),
    (r'^links/$', 'fdadjango.transporterDatabase.views.links'),
    (r'^glossary/$', 'fdadjango.transporterDatabase.views.glossary'),
    (r'^organs/liver/$', 'fdadjango.transporterDatabase.views.liver'),
    (r'^organs/kidney/$', 'fdadjango.transporterDatabase.views.kidney'),
    (r'^organs/(?P<organ_id>(\w+-)*\w+)/$', 'fdadjango.transporterDatabase.views.organ'),
    (r'^samples/(?P<organ_id>(\w+-)*\w+)/$', 'fdadjango.transporterDatabase.views.sample'),
    (r'^samples/(?P<organ_id>(\w+-)*\w+)/(?P<transporter_id>(\w+-)*\w+)/$', 'fdadjango.transporterDatabase.views.sampleT'),
    (r'^compounds/(?P<compound_id>[\w\+\(\)-]+)/$', 'fdadjango.transporterDatabase.views.compound'),
    (r'^ddi-info/(?P<ddi_id>\w+)/$', 'fdadjango.transporterDatabase.views.ddi'),
    (r'^test/$', 'fdadjango.transporterDatabase.views.test'),
    (r'^search$', 'fdadjango.transporterDatabase.views.search'),
    (r'^sitemap.xml$', 'fdadjango.transporterDatabase.views.sitemap'),
    (r'^$', 'fdadjango.transporterDatabase.views.home'),
)
