# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-22 08:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20160721_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcomment',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 22, 8, 48, 34, 65070, tzinfo=utc), null=True),
        ),
    ]