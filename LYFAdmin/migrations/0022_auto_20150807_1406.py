# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0021_auto_20150806_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneverify',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 7, 6, 6, 5, 472188, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='phoneverify',
            name='modify_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 7, 6, 6, 14, 143854, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
