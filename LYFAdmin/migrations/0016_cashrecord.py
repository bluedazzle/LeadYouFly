# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0015_moneyrecord_record_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('record_id', models.CharField(unique=True, max_length=30)),
                ('money', models.FloatField(default=0.0)),
                ('bank_id', models.CharField(default=b'', max_length=50)),
                ('belong', models.ForeignKey(related_name='men_cash_recs', to='LYFAdmin.Mentor')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
