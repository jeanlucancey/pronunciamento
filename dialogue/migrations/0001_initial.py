# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ElementDialogue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nom', models.CharField(unique=True, max_length=30)),
                ('param1', models.CharField(max_length=80)),
                ('param2', models.CharField(max_length=80)),
                ('param3', models.CharField(max_length=80)),
            ],
            options={
                'ordering': ['nom'],
            },
        ),
    ]
