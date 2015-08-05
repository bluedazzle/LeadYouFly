# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0011_auto_20150805_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='freezse',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
