# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0023_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='token',
            field=models.CharField(default=1, unique=True, max_length=64),
            preserve_default=False,
        ),
    ]
