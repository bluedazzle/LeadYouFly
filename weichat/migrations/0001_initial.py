# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default=b'', max_length=256)),
                ('scene', models.CharField(unique=True, max_length=60)),
                ('ticket', models.CharField(default=b'', max_length=512)),
                ('welcome_text', models.CharField(default=b'', max_length=2000)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('open_id', models.CharField(unique=True, max_length=128)),
                ('nick', models.CharField(default=b'', max_length=512)),
                ('cancel', models.BooleanField(default=False)),
                ('channel', models.ForeignKey(related_name='cnl_pros', blank=True, to='weichat.Channel', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WeChatAdmin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_id', models.CharField(default=b'', max_length=128)),
                ('app_secret', models.CharField(default=b'', max_length=128)),
                ('access_token', models.CharField(default=b'', max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
