# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0016_cashrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashrecord',
            name='manage',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
