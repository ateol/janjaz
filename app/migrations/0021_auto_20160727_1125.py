# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-27 11:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20160727_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcomment',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 27, 11, 25, 30, 645760, tzinfo=utc), null=True),
        ),
    ]