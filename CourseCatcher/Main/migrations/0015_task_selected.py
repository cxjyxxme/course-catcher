# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0014_auto_20161213_0308'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='selected',
            field=models.BooleanField(default=False),
        ),
    ]
