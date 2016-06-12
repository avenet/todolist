# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-12 05:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Up to 60 characters for a short name for the task', max_length=60)),
                ('description', models.TextField(help_text='A text which describes further details on what should be done with the task')),
                ('status', models.IntegerField(choices=[(1, 'Pending'), (2, 'Solved')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='The date when this task was created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='The date when this task was last updated')),
                ('owner', models.ForeignKey(help_text='The user who created this task', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
