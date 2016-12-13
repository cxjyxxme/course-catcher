# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0007_auto_20161211_0504'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Test',
        ),
    ]
