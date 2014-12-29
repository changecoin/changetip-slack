from django.db import models


class SlackUser(models.Model):

    name = models.CharField(max_length=50, db_index=True)
    user_id = models.CharField(max_length=10, unique=True)
    team_id = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("team_id", "name")
