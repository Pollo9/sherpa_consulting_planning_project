# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2020-03-08 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0020_auto_20200308_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='bdd_client',
            name='archive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bdd_consultants',
            name='archive',
            field=models.BooleanField(default=False),
        ),
    ]
