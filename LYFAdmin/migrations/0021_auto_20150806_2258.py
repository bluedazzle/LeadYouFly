# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0020_phoneverify'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexadmin',
            name='index_pic1',
            field=models.CharField(default=b' ', max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='indexadmin',
            name='index_pic2',
            field=models.CharField(default=b' ', max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='indexadmin',
            name='index_pic3',
            field=models.CharField(default=b' ', max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='indexadmin',
            name='index_video',
            field=models.CharField(default=b'', max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='indexadmin',
            name='video_poster',
            field=models.CharField(default=b'', max_length=500),
            preserve_default=True,
        ),
    ]
