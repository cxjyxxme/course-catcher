# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0015_task_selected'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='add_code_times',
            field=models.IntegerField(default=0),
        ),
    ]
