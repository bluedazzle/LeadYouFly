# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0007_auto_20150805_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pay_type',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
