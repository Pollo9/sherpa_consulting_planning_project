# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2020-03-05 13:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0009_auto_20200304_1458'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bdd_missions',
            options={'ordering': ['date'], 'verbose_name': 'Mission'},
        ),
    ]