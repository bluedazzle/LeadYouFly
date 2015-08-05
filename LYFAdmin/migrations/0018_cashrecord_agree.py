# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0017_cashrecord_manage'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashrecord',
            name='agree',
            field=models.NullBooleanField(default=None),
            preserve_default=True,
        ),
    ]
