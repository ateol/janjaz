# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-09 07:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcomment',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 9, 7, 45, 43, 244042, tzinfo=utc), null=True),
        ),
    ]
