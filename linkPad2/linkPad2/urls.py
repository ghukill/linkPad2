from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'linkPad2.views.index', name='index'),
    url(r'^add/$', 'linkPad2.views.addLink', name='addLink'),
    url(r'^search/$', 'linkPad2.views.search', name='search'),
)
