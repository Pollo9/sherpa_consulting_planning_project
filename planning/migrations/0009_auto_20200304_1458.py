# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2020-03-04 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0008_auto_20200304_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bdd_missions',
            name='date',
            field=models.CharField(default=' ', max_length=400),
        ),
    ]
