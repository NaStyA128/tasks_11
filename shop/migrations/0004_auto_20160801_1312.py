# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-01 13:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20160801_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(blank=True, max_length=255, upload_to='photos/'),
        ),
    ]