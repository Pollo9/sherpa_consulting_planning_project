# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2020-03-06 13:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0016_auto_20200306_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bdd_client',
            name='mission_type',
        ),
    ]