from django.db import models
from jsonfield import JSONField


class SlackUser(models.Model):

    name = models.CharField(max_length=50, db_index=True)
    user_id = models.CharField(max_length=10, unique=True)
    team_id = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("team_id", "name")


class SlackTip(models.Model):

    sender = models.CharField(max_length=191, help_text="username in team")
    receiver = models.CharField(max_length=191, db_index=True, help_text="username in team")
    message = models.TextField(null=True)
    context_uid = models.CharField(max_length=191, help_text="unique identifier of the content on channel")
    meta_json = JSONField(default={}, help_text="JSON meta data", verbose_name="Meta Data")
