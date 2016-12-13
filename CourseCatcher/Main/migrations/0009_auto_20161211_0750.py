# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0008_delete_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='course_id',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='course_id2',
            field=models.TextField(),
        ),
    ]
