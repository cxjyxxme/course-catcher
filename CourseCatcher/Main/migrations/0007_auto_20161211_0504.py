# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0006_verificationcodelist_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verificationcodelist',
            name='name',
        ),
        migrations.AddField(
            model_name='task',
            name='course_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='course_id2',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='verificationcodelist',
            name='code',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='verificationcodelist',
            name='md5',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
