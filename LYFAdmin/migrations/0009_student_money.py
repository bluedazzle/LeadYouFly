# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0008_order_pay_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='money',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
