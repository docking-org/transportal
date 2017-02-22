from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^transportal/', include('transportal.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^transporters/(?P<transporter_id>\w+)/$', 'transportal.transporterDatabase.views.transporter'),
    (r'^index/$', 'transportal.transporterDatabase.views.index'),
    (r'^about/$', 'transportal.transporterDatabase.views.about'),
    (r'^contact/$', 'transportal.transporterDatabase.views.contact'),
    (r'^links/$', 'transportal.transporterDatabase.views.links'),
    (r'^glossary/$', 'transportal.transporterDatabase.views.glossary'),
    (r'^organs/liver/$', 'transportal.transporterDatabase.views.liver'),
    (r'^organs/kidney/$', 'transportal.transporterDatabase.views.kidney'),
    (r'^organs/(?P<organ_id>(\w+-)*\w+)/$', 'transportal.transporterDatabase.views.organ'),
    (r'^samples/(?P<organ_id>(\w+-)*\w+)/$', 'transportal.transporterDatabase.views.sample'),
    (r'^samples/(?P<organ_id>(\w+-)*\w+)/(?P<transporter_id>(\w+-)*\w+)/$', 'transportal.transporterDatabase.views.sampleT'),
    (r'^compounds/(?P<compound_id>[\w\+\(\)-]+)/$', 'transportal.transporterDatabase.views.compound'),
    (r'^ddi-info/(?P<ddi_id>\w+)/$', 'transportal.transporterDatabase.views.ddi'),
    (r'^test/$', 'transportal.transporterDatabase.views.test'),
    (r'^search$', 'transportal.transporterDatabase.views.search'),
    (r'^sitemap.xml$', 'transportal.transporterDatabase.views.sitemap'),
    (r'^$', 'transportal.transporterDatabase.views.home'),
)
