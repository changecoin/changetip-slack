# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SlackTip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sender', models.CharField(help_text=b'username in team', max_length=191)),
                ('receiver', models.CharField(help_text=b'username in team', max_length=191, db_index=True)),
                ('message', models.TextField(null=True)),
                ('context_uid', models.CharField(help_text=b'unique identifier of the content on channel', max_length=191)),
                ('meta_json', jsonfield.fields.JSONField(default={}, help_text=b'JSON meta data', verbose_name=b'Meta Data')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SlackUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, db_index=True)),
                ('user_id', models.CharField(unique=True, max_length=10)),
                ('team_id', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='slackuser',
            unique_together=set([('team_id', 'name')]),
        ),
    ]
