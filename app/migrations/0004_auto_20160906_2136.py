# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-06 21:36
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20160906_1421'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='event',
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]