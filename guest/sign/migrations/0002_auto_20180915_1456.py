# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-09-15 06:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='limit',
            field=models.IntegerField(),
        ),
    ]
