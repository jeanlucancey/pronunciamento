# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newslink',
            name='pub_date',
            field=models.DateField(verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='startup',
            name='founded_date',
            field=models.DateField(verbose_name='date founded'),
        ),
    ]
