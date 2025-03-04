from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static


from transportal.transporterDatabase import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = [
 # Example:
    # url(r'^transportal/', 'transportal.foo.urls'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # url(r'^admin/doc/', 'django.contrib.admindocs.urls'),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', admin.site.urls),

    url(r'^transporters/(?P<transporter_id>\w+)/$', views.transporter),
    url('^index/$', views.index),
    url(r'^about/$', views.about),
    url(r'^contact/$', views.contact),
    url(r'^links/$', views.links),
    url(r'^glossary/$', views.glossary),
    url(r'^organs/liver/$', views.liver),
    url(r'^organs/kidney/$', views.kidney),
    url(r'^organs/(?P<organ_id>(\w+-)*\w+)/$', views.organ),
    url(r'^samples/(?P<organ_id>(\w+-)*\w+)/$', views.sample),
    url(r'^samples/(?P<organ_id>(\w+-)*\w+)/(?P<transporter_id>(\w+-)*\w+)/$', views.sampleT),
    url(r'^compounds/(?P<compound_id>[\w\+\(\)-]+)/$', views.compound),
    url(r'^ddi-info/(?P<ddi_id>\w+)/$', views.ddi),
    url(r'^testticbase/(?P<transporter_id>\w+)/$', views.testticbase),
    url(r'^testticbase1/(?P<transporter_id>\w+)/$', views.testticbase1),
    url(r'^testticbase2/(?P<transporter_id>\w+)/$', views.testticbase2),
    url(r'^search$', views.search),
    url(r'^sitemap.xml$', views.sitemap),
    url(r'^$', views.home),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#### Outdated Django 1.6 code

# urlpatterns = patterns('',
#     # Example:
#     # (r'^transportal/', include('transportal.foo.urls')),
#
#     # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
#     # to INSTALLED_APPS to enable admin documentation:
#     # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
#
#     # Uncomment the next line to enable the admin:
#     (r'^admin/', include(admin.site.urls)),
#
#     (r'^transporters/(?P<transporter_id>\w+)/$', 'transportal.transporterDatabase.views.transporter'),
#     (r'^index/$', 'transportal.transporterDatabase.views.index'),
#     (r'^about/$', 'transportal.transporterDatabase.views.about'),
#     (r'^contact/$', 'transportal.transporterDatabase.views.contact'),
#     (r'^links/$', 'transportal.transporterDatabase.views.links'),
#     (r'^glossary/$', 'transportal.transporterDatabase.views.glossary'),
#     (r'^organs/liver/$', 'transportal.transporterDatabase.views.liver'),
#     (r'^organs/kidney/$', 'transportal.transporterDatabase.views.kidney'),
#     (r'^organs/(?P<organ_id>(\w+-)*\w+)/$', 'transportal.transporterDatabase.views.organ'),
#     (r'^samples/(?P<organ_id>(\w+-)*\w+)/$', 'transportal.transporterDatabase.views.sample'),
#     (r'^samples/(?P<organ_id>(\w+-)*\w+)/(?P<transporter_id>(\w+-)*\w+)/$', 'transportal.transporterDatabase.views.sampleT'),
#     (r'^compounds/(?P<compound_id>[\w\+\(\)-]+)/$', 'transportal.transporterDatabase.views.compound'),
#     (r'^ddi-info/(?P<ddi_id>\w+)/$', 'transportal.transporterDatabase.views.ddi'),
#     (r'^test/$', 'transportal.transporterDatabase.views.test'),
#     (r'^search$', 'transportal.transporterDatabase.views.search'),
#     (r'^sitemap.xml$', 'transportal.transporterDatabase.views.sitemap'),
#     (r'^$', 'transportal.transporterDatabase.views.home'),
# )
