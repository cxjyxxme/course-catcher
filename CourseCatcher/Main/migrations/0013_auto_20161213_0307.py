# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0012_auto_20161213_0301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcodelist',
            name='last_ask_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 13, 3, 7, 41, 998517, tzinfo=utc)),
        ),
    ]
