# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-22 13:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_articleinfo_post_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articleinfo',
            options={'verbose_name': '文章', 'verbose_name_plural': '文章列表'},
        ),
        migrations.RemoveField(
            model_name='articleinfo',
            name='post_type',
        ),
    ]