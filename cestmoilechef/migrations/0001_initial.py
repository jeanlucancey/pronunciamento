# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('nom', models.CharField(max_length=30, unique=True)),
                ('slug', models.SlugField(help_text="ben... c'est une categorie, quoi !", max_length=30, unique=True)),
            ],
            options={
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('nomComplet', models.CharField(max_length=80)),
                ('nomAbrege', models.CharField(max_length=30)),
                ('categorie', models.ForeignKey(to='cestmoilechef.Categorie')),
            ],
            options={
                'ordering': ['nomComplet'],
            },
        ),
    ]
