# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-18 11:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20160718_0437'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.CharField(blank=True, max_length=50)),
                ('company_name', models.CharField(blank=True, max_length=50)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('organisers_website', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventWebsite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_website', models.URLField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='address',
        ),
        migrations.RemoveField(
            model_name='event',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='event',
            name='contact_name',
        ),
        migrations.RemoveField(
            model_name='event',
            name='email',
        ),
        migrations.RemoveField(
            model_name='event',
            name='organisers_website',
        ),
        migrations.RemoveField(
            model_name='event',
            name='phone_number',
        ),
        migrations.AlterField(
            model_name='event',
            name='event_website',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.EventWebsite'),
        ),
        migrations.AddField(
            model_name='event',
            name='event_organizer',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.EventDetails'),
        ),
    ]