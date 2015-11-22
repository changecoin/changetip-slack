from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^slack/command-webhook$', 'slack.views.command_webhook'),
    url(r'^slack/__status', 'slack.views.home'),
    url(r'^slack/auth$', 'slack.views.slack_oauth'),
)
