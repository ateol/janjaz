# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-03 18:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2016, 9, 3, 18, 10, 43, 190961, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='firstName',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lastName',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
