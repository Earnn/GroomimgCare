# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-05-14 02:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0041_auto_20170513_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='carNumber',
            field=models.CharField(default='', max_length=10),
        ),
    ]
