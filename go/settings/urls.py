"""
settings/urls.py

The URLs of the project and their associated view that requests are routed to.
"""
# Django Imports
import django.contrib.auth.views
from django.conf.urls import url
from django.contrib import admin
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

# App Imports
import go.views

# This function attempts to import an admin module in each installed
# application. Such modules are expected to register models with the admin.
admin.autodiscover()

urlpatterns = [
    # / - Homepage url. Cached for 1 second (this is the page you see after
    # logging in, so having it show as not logged in is strange)
    url(r'^$', cache_page(1)(go.views.index), name='index'),

    # /view/<short> - View URL data. Cached for 15 minutes
    url(r'^view/(?P<short>[-\w]+)$', cache_page(60 * 15)(go.views.view), name='view'),

    # /about - About page. Cached for 15 minutes
    url(r'^about/?$',cache_page(60 * 15)(TemplateView.as_view(template_name='core/about.html')), name='about'),

    # /signup - Signup page for access. Cached for 15 minutes
    url(r'^signup/?$', cache_page(60 * 15)(go.views.signup), name='signup'),

    # /new - Create a new Go Link
    url(r'^new/?$', go.views.new_link, name='new_link'),

    # /my - My-Links page, view and review links.
    url(r'^my/?$', go.views.my_links, name='my_links'),

    # /edit/<short> - Edit link form
    url(r'^edit/(?P<short>[-\w]+)$', go.views.edit, name='edit'),

    # /delete/<short> - Delete a link, no content display.
    url(r'^delete/(?P<short>[-\w]+)$', go.views.delete, name='delete'),

    # /registered - registration complete page. Cached for 15 minutes
    url(r'^registered/?$', cache_page(60 * 15)(TemplateView.as_view(template_name='registered.html')), name='registered'),

    # /admin - Administrator interface.
    url(r'^admin/?', admin.site.urls, name='go_admin'),

    # /manage - user approval interface
    url(r'^manage/?$', go.views.useradmin, name='useradmin'),

    # Authentication URLs
    url(r'^login$', django.contrib.auth.views.login, name='go_login'),
    url(r'^logout$', django.contrib.auth.views.logout, {'next_page': '/'}, name='go_logout'),

    # Redirection regex.
    url(r'^(?P<short>[-\w]+)$', go.views.redirection, name='redirection'),
]
