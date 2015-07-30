# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0002_indexadmin_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='id_picture',
            field=models.CharField(default=b'', max_length=100),
            preserve_default=True,
        ),
    ]
