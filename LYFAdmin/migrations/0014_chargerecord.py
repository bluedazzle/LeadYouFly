# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0013_remove_mentor_freezse'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChargeRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('record_id', models.CharField(unique=True, max_length=30)),
                ('charge_number', models.FloatField(default=0.0)),
                ('note', models.CharField(default=b'', max_length=200)),
                ('belong', models.ForeignKey(related_name='stu_charge_recs', to='LYFAdmin.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
