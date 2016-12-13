# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0011_auto_20161213_0259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='last_ask_time',
        ),
        migrations.AddField(
            model_name='verificationcodelist',
            name='last_ask_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 13, 3, 1, 6, 738095, tzinfo=utc)),
        ),
    ]
