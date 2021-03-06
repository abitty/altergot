# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-06 16:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

	initial = True

	dependencies = [
		migrations.swappable_dependency(settings.AUTH_USER_MODEL),
	]

	operations = [
		migrations.CreateModel(
			name='Coin',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('country', models.CharField(max_length=128)),
				('value', models.CharField(max_length=128)),
				('year', models.CharField(max_length=4)),
				('specific', models.CharField(max_length=255)),
				('inuse', models.BooleanField(default=False)),
				('haveit', models.BooleanField(default=True)),
				('condition', models.CharField(choices=[('MN', 'mint'), ('VG', 'good'), ('BD', 'bad')], default='VG', max_length=2)),
				('avers', models.ImageField(upload_to='uploads/')),
				('revers', models.ImageField(upload_to='uploads/')),
				('comment', models.CharField(max_length=255)),
				('created_date', models.DateTimeField(default=django.utils.timezone.now)),
				('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
			],
		),
	]