# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0009_auto_20161211_0750'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='try_times',
            field=models.IntegerField(default=0),
        ),
    ]
