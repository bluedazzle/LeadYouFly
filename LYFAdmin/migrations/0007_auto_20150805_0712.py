# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0006_auto_20150805_0614'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexadmin',
            name='index_pic1',
            field=models.CharField(default=b' ', max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indexadmin',
            name='index_pic2',
            field=models.CharField(default=b' ', max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indexadmin',
            name='index_pic3',
            field=models.CharField(default=b' ', max_length=100),
            preserve_default=True,
        ),
    ]
