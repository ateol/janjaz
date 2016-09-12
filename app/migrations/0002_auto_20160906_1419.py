# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-06 14:19
from __future__ import unicode_literals

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prominentplace',
            name='Image',
            field=models.FileField(blank=True, upload_to=app.models.prominent_place_picture_destination),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to=app.models.profile_picture_destination),
        ),
    ]
