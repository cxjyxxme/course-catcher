# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0010_task_try_times'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='last_ask_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 13, 2, 59, 37, 396643, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='verificationcodelist',
            name='code',
            field=models.TextField(default=b''),
        ),
    ]
