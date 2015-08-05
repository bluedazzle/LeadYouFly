# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0014_chargerecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneyrecord',
            name='record_id',
            field=models.CharField(default=1, unique=True, max_length=30),
            preserve_default=False,
        ),
    ]
