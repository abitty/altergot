# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-11 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sets', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'verbose_name': 'Коллекция', 'verbose_name_plural': 'Коллекции'},
        ),
        migrations.RenameField(
            model_name='collection',
            old_name='name',
            new_name='cname',
        ),
        migrations.AlterField(
            model_name='collection',
            name='kind',
            field=models.CharField(choices=[('CN', 'Монеты'), ('BN', 'Купюры')], default='CN', max_length=2, verbose_name='Тип'),
        ),
    ]
