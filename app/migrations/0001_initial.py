# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-16 13:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('living_in_turkey', models.CharField(max_length=3)),
                ('country_of_origin', models.CharField(max_length=50)),
                ('city_living', models.CharField(max_length=50)),
                ('profile_picture', models.FileField(null=True, upload_to='Profile_pictures/%Y/%m/%d')),
                ('gender', models.CharField(max_length=6)),
                ('status', models.CharField(max_length=50)),
                ('about_yourself', models.CharField(max_length=500)),
                ('interests', models.CharField(max_length=500)),
                ('languages', models.CharField(max_length=500)),
                ('occupation', models.CharField(max_length=20)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]