# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dvd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('titre', models.CharField(max_length=80)),
                ('slug', models.SlugField(max_length=31, unique=True, help_text='Un slug pour les DVD.')),
                ('actClair', models.CharField(max_length=120)),
                ('reaClair', models.CharField(max_length=80)),
                ('genre', models.CharField(max_length=40)),
                ('place', models.CharField(max_length=40)),
                ('obs', models.CharField(max_length=160)),
            ],
            options={
                'ordering': ['titre'],
            },
        ),
    ]
