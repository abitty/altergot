# Generated by Django 3.2.7 on 2021-09-05 10:33

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
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('CN', 'Монеты'), ('BN', 'Купюры')], default='CN', max_length=2, verbose_name='Тип')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('public', models.BooleanField(default=True, verbose_name='Показывать')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Коллекция',
                'verbose_name_plural': 'Коллекции',
            },
        ),
    ]
