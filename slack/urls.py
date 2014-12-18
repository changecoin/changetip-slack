from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^slack/command-webhook$', 'slack.views.command_webhook'),
    url(r'^$', 'slack.views.home'),
)
