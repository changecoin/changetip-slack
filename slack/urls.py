from django.conf.urls import patterns, url
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^command-webhook$', 'slack.views.command_webhook'),

    # Everything else, redirect
    url(r'', RedirectView.as_view(url="https://github.com/changecoin/changetip-slack")),
)
