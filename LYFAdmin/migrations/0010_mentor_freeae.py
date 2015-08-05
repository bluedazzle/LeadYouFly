# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0009_student_money'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='freeae',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
