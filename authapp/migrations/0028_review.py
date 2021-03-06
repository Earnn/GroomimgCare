# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-05-08 12:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0027_remove_person_picperson'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('user_name', models.CharField(max_length=100)),
                ('comment', models.CharField(max_length=200)),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('wine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authapp.Person')),
            ],
        ),
    ]
