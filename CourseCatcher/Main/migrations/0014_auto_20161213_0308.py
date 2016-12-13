# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0013_auto_20161213_0307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcodelist',
            name='last_ask_time',
            field=models.DateTimeField(),
        ),
    ]
