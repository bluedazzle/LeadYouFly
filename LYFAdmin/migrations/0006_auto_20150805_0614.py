# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0005_auto_20150805_0600'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='cash_income',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mentor',
            name='iden_income',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mentor',
            name='mark',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mentor',
            name='total_income',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
