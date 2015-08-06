# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0018_cashrecord_agree'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexadmin',
            name='index_video',
            field=models.CharField(default=b'', max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indexadmin',
            name='video_poster',
            field=models.CharField(default=b'', max_length=100),
            preserve_default=True,
        ),
    ]
