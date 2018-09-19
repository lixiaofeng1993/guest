# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-09-07 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request_parameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=50)),
                ('method', models.CharField(max_length=11)),
                ('params', models.TextField()),
                ('body', models.TextField()),
                ('header', models.TextField()),
                ('verify', models.TextField()),
            ],
            options={
                'db_table': 'request_parameter',
            },
        ),
    ]