# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-26 09:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dialogue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('greeting', models.CharField(max_length=300)),
                ('if_pos', models.CharField(max_length=300)),
                ('if_neg', models.CharField(max_length=300)),
            ],
        ),
    ]
